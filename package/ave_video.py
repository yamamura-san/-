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
    base=np.zeros((h,w),np.uint32)

    #平均化処理
    for i in imgs_list:
        img = cv2.imread(i,cv2.IMREAD_GRAYSCALE)
        base += img
    base = base/(len(imgs_list))
    base=base.astype(np.uint8)
    cv2.imwrite(dir + "/ave.jpg", base)

    #Jet画像
    base_color = cv2.applyColorMap(base, cv2.COLORMAP_JET)
    cv2.imwrite(dir + "/ave_color.jpg", base_color)

if __name__ == "__main__":
    ave("result_split")
