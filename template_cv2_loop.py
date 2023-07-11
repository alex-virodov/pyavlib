import cv2
import numpy as np
from pyavlib.keyboard_util import ExitOnKey


def main():
    try:
        window_name = __file__

        cv2.namedWindow(window_name)
        is_exit = ExitOnKey()

        img = np.zeros(shape=(256, 512, 3), dtype=np.uint8)

        while not is_exit:
            idx = np.random.uniform(0, 256, 2).astype(int)
            img[idx[0], idx[1]] = 255
            cv2.imshow(window_name, img)

            cv2.waitKey(1)
    finally:
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()