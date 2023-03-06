from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import glob
import cv2
from skimage import io

def stack(folder, step):

    # Extract images from a specified folder
    imgs = folder+"/*jpg"
    imgs_list = glob.glob(imgs)

    # Define number of stacks and create empty array
    i = len(imgs_list)
    size_image = Image.open(folder + '/img_0.jpg', 'r')
    stacked = np.ndarray(shape=(size_image.size[1], size_image.size[0], i), dtype= np.uint8)
    print("フォルダ内の画像は{}枚です".format(i))

    # Processing stacks of images
    s = 0
    for s in range(i):
        # Open image convertiung it to grayscale
        source = Image.open(folder + '/img_' + str(s) + '.jpg', 'r').convert('L')
        # Convert image to array
        m = np.array(source, dtype=np.uint8) 
        # Fill empty array with image
        stacked[:, :, s] = m
        s = s+1

    # Threshold processing and dimensions are unified in mm
    thresh = 50
    x, y, z= (np.where(stacked > thresh))
    x = x
    y = y
    z = z
    v = stacked[np.where(stacked> thresh)]

    fig = plt.figure()

    # カラーマップを生成
    cm = plt.cm.get_cmap('jet')
    ax = fig.add_subplot(111, projection='3d')
    map =ax.scatter(x,y,z,c = v, cmap=cm, s = 1)
    fig.colorbar(map, ax=ax)

    max_range = np.array([x.max()-x.min(), y.max()-y.min(), z.max()-z.min()]).max() * 0.5
    mid_x = (x.max()+x.min()) * 0.5
    mid_y = (y.max()+y.min()) * 0.5
    mid_z = (z.max()+z.min()) * 0.5
    ax.set_xlim(mid_x - max_range, mid_x + max_range)
    ax.set_ylim(mid_y - max_range, mid_y + max_range)
    ax.set_zlim(mid_z - max_range, mid_z + max_range)

    plt.show()

def stack_slice(folder):

    # Extract images from a specified folder
    imgs = folder+"/*jpg"
    imgs_list = glob.glob(imgs)

    # Define number of stacks and create empty array
    i = len(imgs_list)
    size_image = Image.open(folder + '/img_0.jpg', 'r')
    stacked = np.ndarray(shape=(size_image.size[1], size_image.size[0], 1200), dtype= np.uint8)
    print("フォルダ内の画像は{}枚です".format(i))

    # Processing stacks of images
    for s in range(1, i+1):
        # Open image convertiung it to grayscale
        source = Image.open(folder + '/img_' + str(s-1) + '.jpg', 'r').convert('L')
        # Convert image to array
        m = np.array(source, dtype=np.uint8) 
        # Fill empty array with image
        stacked[:, :, s*240] = m
        s = s+1

        # Change the direction of slicing

        img_tmp = np.empty((1920, 1200), dtype = int)
        for j in range(size_image.size[1]):
            img_tmp = stacked[j, :, :]
            io.imsave("result/img_" + str(j) + ".jpg", img_tmp)

            i += 1


if __name__ == "__main__":
    #stack("stack_source", 5)
    stack_slice("stack_source")
