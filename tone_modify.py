import cv2
import numpy as np
import math

#transrate input image into the other image with different tone
class ToneColor:
    def tone(self, image, ganma):
        img = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
        self.img = image
        self.ganma = math.floor(ganma * 10) / 10
        
        # tone curve function
        x =  np.arange(256)
        y =  (x/255)**ganma * 255
        dst = cv2.LUT(img, y)
        cv2.imwrite(self.img +"_ganma_{0}.jpg".format(self.ganma), dst)

        dst = dst.astype(np.uint8)
        dst_color = cv2.applyColorMap(dst, cv2.COLORMAP_JET)
        cv2.imwrite("ave_color_ganma_{0}.jpg".format(self.ganma), dst_color)

if __name__ == "__main__":
    img_tone = ToneColor()
    img_tone.tone("ave.jpg", 2)

