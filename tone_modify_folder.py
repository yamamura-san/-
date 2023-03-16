import numpy as np
import cv2
import glob
import math
import os

class ToneColerFolder:

    def __init__(self, folder, ganma):
        self.folder = folder
        self.ganma = math.floor(ganma * 10) / 10
        self.f1 = "source_tone_ganma{0}".format(self.ganma)
        self.f2 = "source_tone_ganma{0}_color".format(self.ganma)
        os.makedirs(self.f1, exist_ok=True)
        os.makedirs(self.f2, exist_ok=True)

    def tone_folder(self):
        imgs = self.folder+"/*jpg"
        imgs_list = glob.glob(imgs)
        print(len(imgs_list))

        x =  np.arange(256)
        y =  (x/255)**self.ganma * 255

        for i in imgs_list:
            img = cv2.imread(i,cv2.IMREAD_GRAYSCALE)
            dst = cv2.LUT(img, y)
            dst=dst.astype(np.uint8)
            dst_color = cv2.applyColorMap(dst, cv2.COLORMAP_JET)

            # 保存用にパス名からファイル名を抽出
            i = os.path.basename(i)
            cv2.imwrite(self.f1 + "/" + i, dst)
            cv2.imwrite(self.f2 + "/" + i, dst_color)
        
        print("ガンマ値{0}でトーン補正が完了しました".format(self.ganma))

if __name__ == "__main__":
    # フォルダ名、ガンマ補正値を引数に入れてあげればオブジェクト作成
    Tone = ToneColerFolder("source", 0.5)
    Tone.tone_folder()