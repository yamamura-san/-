import PySimpleGUI as sg
import configparser
from pypylon import pylon
import cv2
import time

def main():
    #GUI上でカメラの設定値登録
    videotime, exposuretime, fps, gain, x_min, x_max, y_min, y_max = setting()

    #指定したパラメータで撮影実行
    cap(videotime, exposuretime, fps, gain, x_min, x_max, y_min, y_max)


# call back fun1
def value1(x):
    print("露光時間は{0} umに設定しています".format(x))

# call back fun1
def value2(y):
    print("ゲインは{0}に設定しています".format(y))

def setting():

    # iniファイル読み込み
    config = configparser.ConfigParser()
    config.read("package/config.ini")
    cfg_read_1 = config["Data"]["videotime"]
    cfg_read_2 = config["Data"]["exposuretime"]
    cfg_read_3 = config["Data"]["fps"]
    cfg_read_4 = config["Data"]["gain"]
    cfg_read_5 = config["Data"]["x_min"]
    cfg_read_6 = config["Data"]["x_max"]
    cfg_read_7 = config["Data"]["y_min"]
    cfg_read_8 = config["Data"]["y_max"]   

    # GUI設定
    sg.theme('Dark Blue 3')
    layout = [
        [sg.Text('撮影設定を入力してください')],
        [sg.Text('撮影時間 [s]', size=(20, 1)), sg.InputText(cfg_read_1)],      
        [sg.Text('露光時間(19 um≧) [us]', size=(20, 1)), sg.InputText(cfg_read_2)],
        [sg.Text('フレームレート [fps]', size=(20, 1)), sg.InputText(cfg_read_3)],
        [sg.Text('ゲイン(≦48 dB) [dB]', size=(20, 1)), sg.InputText(cfg_read_4)],
        [sg.Text('トリムx_min [pix]', size=(20, 1)), sg.InputText(cfg_read_5)],      
        [sg.Text('トリムx_max [pix]', size=(20, 1)), sg.InputText(cfg_read_6)],
        [sg.Text('トリムy_min [pix]', size=(20, 1)), sg.InputText(cfg_read_7)],
        [sg.Text('トリムy_max [pix]', size=(20, 1)), sg.InputText(cfg_read_8)],
        [sg.Submit(button_text='設定完了')]
        ]

    window = sg.Window('撮影条件設定', layout)

    while True:
        event, values = window.read()
        if event is None:
            print('exit')
            break

        if event == '設定完了':
            show_message = "撮影時間は{0} [s]\n".format(values[0])
            show_message += "露光時間は{0} [us]\n".format(values[1])
            show_message += "フレームレートは{0} [fps]\n".format(values[2])
            show_message += "ゲインは{0} [dB]\n".format(values[3])
            val0, val1, val2, val3, val4, val5, val6, val7= int(values[0]), int(values[1]) ,int(values[2]),int(values[3]), int(values[4]), int(values[5]) ,int(values[6]),int(values[7])
            sg.popup(show_message)
            break

    # configの各項目に上書き
    config["Data"]["videotime"] = values[0]
    config["Data"]["exposuretime"]= values[1]
    config["Data"]["fps"] = values[2]
    config["Data"]["gain"] = values[3]
    config["Data"]["x_min"] = values[4]
    config["Data"]["x_max"]= values[5]
    config["Data"]["y_min"] = values[6]
    config["Data"]["y_max"] = values[7]

    # config.iniファイルに上書き
    with open("package/config.ini", "w") as f:
        config.write(f)


    window.close()
    return val0, val1, val2, val3, val4, val5, val6, val7


def cap(videotime, exposuretime, fps, gain, x_min, x_max, y_min, y_max):
    # コーデック（fourcc）の設定
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')

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

    # トラックバー作成
    cv2.namedWindow("title",cv2.WINDOW_NORMAL)
    cv2.createTrackbar("Expotime", "title", exposuretime, 10000, value1)
    cv2.createTrackbar("Gain", "title", gain, 40, value1)

    i=0
    while camera.IsGrabbing():
        grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

        if grabResult.GrabSucceeded():
            # Access the image data

            expo_act = cv2.getTrackbarPos("Expotime", "title")
            camera.ExposureTime.SetValue(expo_act)

            gain_act = cv2.getTrackbarPos("Gain", "title")
            camera.Gain.SetValue(gain_act)

            image = converter.Convert(grabResult)
            img = image.GetArray()
            gray_frame_trim= img[y_min : y_max, x_min : x_max]
            ret, gray_frame_trim_binary = cv2.threshold(gray_frame_trim, 50, 255, cv2.THRESH_BINARY)
            cv2.imshow('title', gray_frame_trim_binary)
            k = cv2.waitKey(1)
            if k == 27:
                break
        grabResult.Release()

    # Releasing the resource
    camera.StopGrabbing()
    cv2.destroyAllWindows()

    print("露光時間は{0}, ゲインは{1}です".format(expo_act, gain_act))

if __name__ == "__main__":
    main()
