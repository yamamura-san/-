import cv2
import os
import datetime
import numpy as np
import glob

def ave(dir):
    #指定したディレクトリの画像を抽出
    imgs = dir+"/*jpg"
    imgs_list = glob.glob(imgs)

    #平均値を計算するための空のndarrayを作成
    img = cv2.imread(imgs_list[0],cv2.IMREAD_GRAYSCALE)
    h,w=img.shape[:2]
    base=np.zeros((h,w),np.uint8)

    #平均化処理
    for i in imgs_list:
        img = cv2.imread(i,cv2.IMREAD_GRAYSCALE)
        base += img
    base = base/(len(imgs_list)/20)
    cv2.imwrite("ave.jpg", base)

    #二値化。平均化した後の画像だと何も見えない
    threshold = 2
    ret, ave_binary = cv2.threshold(base, threshold, 255, cv2.THRESH_BINARY)

    cv2.imwrite("ave_binary.jpg", ave_binary)


if __name__ == "__main__":
    ave("result_split")
