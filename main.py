from package import cap_video as cv
from package import split_video as sv
from package import camera_setting as cs
from package import ave_video as av

print("処理中です")

#GUI上でカメラの設定値登録
videotime, exposuretime, fps, gain, x_min, x_max, y_min, y_max = cs.setting()
print("設定完了")

#指定したパラメータで撮影実行
video, folder = cv.cap(videotime, exposuretime, fps, gain, x_min, x_max, y_min, y_max)
print("撮影完了")

#分割処理
image_dir = sv.split(video, folder, 100)
print("分割完了")

#平均化処理
av.ave(image_dir)
print("平均化完了")

print("処理完了")