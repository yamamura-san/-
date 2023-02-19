import cv2
import datetime
import os

def split(file):
    video = cv2.VideoCapture(file)#動画の読み込み
    fps = int(video.get(cv2.CAP_PROP_FPS)) #fpsを整数へ変換

    #フォルダ作成処理
    #実行時に生成するフォルダ名の作成
    output = "result_split"
    os.makedirs(output, exist_ok=True)#引数をtrueにすると同じパス名でも上書きでフォルダが作れる
    #処理内容、時刻情報を残す処理
    #現在時刻
    now = datetime.datetime.now()
    current_time = now.strftime("%Y-%m-%d-%H-%M")
    f = open(output+'/process_info.txt', 'w')
    f.write(str(current_time)+"に実行")
    f.close()

    #分割処理
    i=0
    while True:
        ret, frame = video.read() #第一戻り数はTrue かFalse。動画が読み込めてたらTrue。第二戻り値は画像情報
        #fps分だけ分割
        if i < fps:
            gray_frame=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.imwrite(output+'/img_'+str(i).zfill(3)+'.jpg', gray_frame)
            i +=1
        #動画が読み込めなくなったらループ終了
        if ret == False:
            break

if __name__ == "__main__":
    split("output.mp4")
