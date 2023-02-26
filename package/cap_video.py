from pypylon import pylon
import cv2
import os
import datetime
import time

def cap(videotime, exposuretime, fps, gain, x_min, x_max, y_min, y_max):
    # コーデック（fourcc）の設定
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    # フォルダ作成
    now = datetime.datetime.now()
    current_time = now.strftime("%Y-%m-%d-%H-%M")
    dir_output = "result_" + current_time
    os.makedirs(dir_output, exist_ok=True)
    # 動画ファイル設定（保存先、FPS、サイズ）
    video = cv2.VideoWriter(dir_output+'/output_'+current_time+'.mp4', fourcc, fps, (x_max-x_min, y_max-y_min))
    print(y_max-y_min)
    print(x_max-x_min)
    # conecting to the first available camera
    camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

    # Grabing Continusely (video) with minimal delay
    camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

    # exposure time seting
    camera.ExposureTime.SetValue(exposuretime)
    # framerate
    camera.AcquisitionFrameRateEnable.SetValue(True)
    camera.AcquisitionFrameRate.SetValue(fps)
    # gain setting
    camera.Gain.SetValue(gain)

    converter = pylon.ImageFormatConverter()

    # converting to opencv bgr format
    converter.OutputPixelFormat = pylon.PixelType_BGR8packed
    converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

    # カメラの設定変更のためにdelayさせる
    time.sleep(1)
    i=0
    while i < videotime*fps:
        grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

        if grabResult.GrabSucceeded():
            # Access the image data
            image = converter.Convert(grabResult)
            img = image.GetArray()
            img= img[y_min : y_max, x_min : x_max]
            video.write(img)
            i +=1

    # Releasing the resource
    camera.StopGrabbing()
    cv2.destroyAllWindows()
    # 撮影条件をtxt化
    with open(dir_output+'/cap_info_'+current_time+'.txt', "w") as f:
        f.write("撮影時間は{} [s]です\n".format(videotime))
        f.write("露光時間は{} [us]です\n".format(exposuretime))
        f.write("フレームレートは{} [fps]です\n".format(fps))
        f.write("ゲインは{} [dB]です\n".format(gain))

    # 動画保存先、動画ファイル名を戻す
    return dir_output+'/output_'+current_time+'.mp4', dir_output

if __name__ == "__main__":
    print(cap(2,1000, 21, 23, 500, 900, 0, 1000))