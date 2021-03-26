import numpy as np
import math

def image_grid(images, cols=None, pad=0):
    width = images[0].shape[0] + pad
    height = images[0].shape[1] + pad
    n_images = len(images)
    if cols is None:
        cols = math.ceil(math.sqrt(n_images))
    rows = n_images // cols + (n_images % cols > 0)
    combined_image = np.zeros(shape=(rows * width, cols * height)+images[0].shape[2:])
    for index, image in enumerate(images):
        row = index // cols
        col = index % cols
        combined_image[height*row:height*(row+1)-pad, width*col:width*(col+1)-pad] = image

    return combined_image

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import string
    import cv2

    images = []
    for letter in string.ascii_lowercase:
        # print(f'letter={letter}')
        image = np.zeros(shape=(32, 32, 3), dtype=np.float) + 0.2
        cv2.putText(image, letter, (8, 24), cv2.FONT_HERSHEY_SIMPLEX, 1, 1.0, 2, cv2.LINE_AA)
        image[3, 3] = 0.0
        images.append(image)

    plt.imshow(image_grid(images, cols=6, pad=2))



