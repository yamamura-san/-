import numpy as np
import glob
import cv2

def stack_slice(folder):

    # Extract images from a specified folder
    imgs = folder+"/*bmp"
    imgs_list = glob.glob(imgs)

    # Define number of stacks and create empty array
    size = cv2.imread(folder + '/img_0.bmp', cv2.IMREAD_GRAYSCALE).shape
    stacked = np.ndarray(shape=(size[0], size[1], 100), dtype= np.uint8)


    # Processing stacks of images
    for s in range(len(imgs_list)):
        # Open image convertiung it to grayscale
        tmp = cv2.imread(folder + '/img_' + str(s) + '.bmp', cv2.IMREAD_GRAYSCALE)
        tmp = np.array(tmp, dtype=np.uint8)
        print(tmp.shape)
        # Fill empty array with image
        # 余白を0行目に持ってくるためS+1とした。
        stacked[:, :, s+10] = tmp
        s = s+1

    # Change the direction of slicing

    img_tmp = np.empty((size[0], 100), dtype = np.uint8)

    for j in range(size[1]):
        img_tmp = stacked[j, :, :]
        img_tmp = cv2.rotate(img_tmp, cv2.ROTATE_90_COUNTERCLOCKWISE)

        # define agnification
        m = 100/40 #100 is image taking pitch, 40 is pixel resolution
        img_tmp_rezise = cv2.resize(img_tmp, dsize = (img_tmp.shape[1], int(img_tmp.shape[0]*m)), interpolation= cv2.INTER_CUBIC)

        cv2.imwrite("result/img_" + str(j) + ".bmp", img_tmp_rezise)

        j += 1

if __name__ == "__main__":
    stack_slice("src")