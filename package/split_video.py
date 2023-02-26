import cv2
import datetime
import os

# 分割する動画名、動画の格納先、分割フレーム数の指定
def split(file, folder, num):
    video = cv2.VideoCapture(file)
    fps = int(video.get(cv2.CAP_PROP_FPS))

    # フォルダ作成処理
    # 実行時に生成するフォルダ名の作成
    output = folder + "/result_split"
    os.makedirs(output, exist_ok=True)
    # 処理内容、時刻情報を残す処理
    now = datetime.datetime.now()
    current_time = now.strftime("%Y-%m-%d-%H-%M")
    with open(output+'/process_info.txt', 'w') as f:
        f.write(str(current_time)+"に実行")

    # 分割処理
    i=0
    while True:
        ret, frame = video.read() # 第一戻り数はTrue かFalse。動画が読み込めてたらTrue。第二戻り値は画像情報
        # fps分だけ分割
        if i < num:
            gray_frame=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            ret, gray_frame_binary = cv2.threshold(gray_frame, 50, 255, cv2.THRESH_BINARY)
            cv2.imwrite(output+'/img_'+str(i)+'.jpg', gray_frame_binary)
            i +=1
        # 動画が読み込めなくなったらループ終了
        else:
            print("動画読み込めないので終了")
            break

    return output

if __name__ == "__main__":
    split("output.mp4", "result_2023-02-27-11-49", 100)