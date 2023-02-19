from pypylon import pylon
import cv2
import datetime

def cap():
    # コーデック（fourcc）の設定
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    # 動画ファイルの設定（保存先、FPS、サイズ）
    video = cv2.VideoWriter('output.mp4', fourcc, 100.0, (1920,1200))
    # conecting to the first available camera
    camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

    # Grabing Continusely (video) with minimal delay
    camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

    #exposure time seting
    camera.ExposureTime.SetValue(1000)
    #framerate
    camera.AcquisitionFrameRateEnable.SetValue(True)
    camera.AcquisitionFrameRate.SetValue(100.0)
    #gain setting
    camera.Gain.SetValue(8)

    converter = pylon.ImageFormatConverter()

    # converting to opencv bgr format
    converter.OutputPixelFormat = pylon.PixelType_BGR8packed
    converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

    i=0
    while i < 200:
        grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

        if grabResult.GrabSucceeded():
            # Access the image data
            image = converter.Convert(grabResult)
            img = image.GetArray()
            cv2.namedWindow('title', cv2.WINDOW_NORMAL)
            cv2.imshow('title', img)
            # フレームの書き込み（保存）
            video.write(img)
            i +=1

    # Releasing the resource
    camera.StopGrabbing()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    cap()
