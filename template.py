import matplotlib.pyplot as plt
from pyavlib.pltutil import plt_clf_subplots
import cv2
import numpy as np

def main():
    image = cv2.imread('image.png', cv2.IMREAD_GRAYSCALE)

    ax = plt_clf_subplots(3, 3)
    ax[0].imshow(image).axes.set_title('image')

if __name__ == '__main__':
    main()