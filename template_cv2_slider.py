import cv2
import numpy as np
import os


def main():
    window_name = os.path.basename(__file__)

    def on_change(value):
        print(value)
        img = np.zeros(shape=(256, 512, 3), dtype=np.uint8)
        cv2.imshow(window_name, img)

    cv2.namedWindow(window_name)
    cv2.createTrackbar('slider', window_name, 0, 100, on_change)
    on_change(0)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()