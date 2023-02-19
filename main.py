from package import cap_video as cv
from package import split_video as sv
from package import ave_video as av

print("処理中です")

#カメラ起動、動画撮影処理
cv.cap()
#分割処理
sv.split("output.mp4")
#平均化処理
av.ave("result_split")

print("処理完了")
