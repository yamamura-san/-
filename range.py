import cv2
import numpy as np
import os 
import sys
import glob
from natsort import natsorted
import pandas as pd

def center_detect(min_index, max_index, folder):

    # 指定フォルダの画像を読み込み
    imgs_list = glob.glob(folder + "/*png")
    imgs_list = natsorted(imgs_list)

    # 画像に閾値を設けて、ピンぼけノイズ処理を指定したフォルダ画像丸ごと行う
    # 処理後の画像格納先フォルダ作成
    result_folder = folder +"/thresh_imgs"
    os.makedirs(result_folder, exist_ok= True)

    # 指定した閾値以下の画素値は0に置換して保存する
    for i in imgs_list:
        thresh = 20
        img = cv2.imread(i, cv2.IMREAD_GRAYSCALE)
        dst = np.where(img < thresh, 0, img)
        name = os.path.basename(i)
        cv2.imwrite(result_folder + "/thresh_" + name, dst)

    # 指定した範囲の分布の重心計算と重心位置にマーキング処理を行う
    # 指定フォルダの画像を読み込み
    imgs_list_thresh = glob.glob(result_folder + "/*png")
    imgs_list_thresh = natsorted(imgs_list_thresh)

    # 指定した範囲だけの画像のリストに変換
    # 重心位置をプロットした画像を保存するフォルダを準備
    result_folder_center = folder + "/center_imgs"
    os.makedirs(result_folder_center, exist_ok= True)
    # ノズル下端から20 pix下がった位置から処理を行う。ノズルぎりぎりだと外れ値を含む恐れがあるので
    min_index = min_index + 2
    # 計算に使う範囲をスライス
    imgs_list_thresh = imgs_list_thresh[min_index: max_index]
    # 各画像の重心位置x, yの値を格納するリストの定義
    cen_x, cen_y = [], []
    #各画像で2値画像にし重心を求める。多値での重心を計算すると光源側に偏った分布になりそうなので、二値で計算する。
    for j in imgs_list_thresh:
        img = cv2.imread(j, cv2.IMREAD_GRAYSCALE)
        mu = cv2.moments(img, True) #Falseとすると多値での計算となる。
        # 画像によってはthreshの値によって画素がない場合もある？　その際は重心を(0,0)として挙げる
        if mu["m00"] == 0:
            x, y = 0, 0
        else:
            x, y= int(mu["m10"]/mu["m00"]) , int(mu["m01"]/mu["m00"])
            cv2.drawMarker(img, (x, y),(255, 255, 255), markerType=cv2.MARKER_STAR, markerSize=5)  
        name = os.path.basename(j)
        cv2.imwrite(result_folder_center + "/center_" +name, img)
        cen_x.append(x)
        cen_y.append(y)
    
    # 各画像の重心データをcsvに保存する処理。重心位置がきちんと計算できているのかを確認するために利用。きちんとできていないと変な値が出てくるはずなので
    data = [cen_x, cen_y]
    df = pd.DataFrame(data).T
    df.to_csv(folder + "/center_result.csv")

    # 重心の平均を計算する処理
    # 値が0の要素をNANに変換
    df_dst = df[df[:]!=0]
    center_x , center_y = df_dst.mean()

    return int(center_x), int(center_y)

if __name__ == "__main__":
    print(center_detect(2, 9, "source"))