from __future__ import (absolute_import, division, print_function, unicode_literals)
from builtins import *
import numpy as np
import cv2


def cv2_waitKey(window, delay):
    """Like cv2.waitKey, but also unblocks if window is closed"""
    waited = 0
    while waited < delay or delay == 0:
        key = cv2.waitKeyEx(10)
        waited += 1
        if key != -1:
            return key
        if cv2.getWindowProperty(window, 0) < 0:
            return -2
    return -1


def cv2_putText(img, text, org,
                fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1,
                color=255, thickness=1, lineType=cv2.LINE_AA):
    """Like cv2.putText() but with defaults especially for font. """
    cv2.putText(img, text, org, fontFace, fontScale, color, thickness, lineType)


def cv2_upscale(image, factor=2):
    dsize = (int(image.shape[1] * factor), int(image.shape[0] * factor))
    return cv2.resize(image, dsize=dsize, interpolation=cv2.INTER_NEAREST)


def cv2_downscale(image, factor=2):
    return cv2_upscale(image, factor=1.0 / float(factor))


def cv2_normalize(image, max=None):
    if max is None:
        return image * 255.0 / np.max(image)
    else:
        return np.clip(image * 255.0 / max, 0.0, 255.0)


def cv2_pyramid(image, levels):
    pyramid = [image] + [None] * (levels - 1)
    for i in range(1, levels):
        pyramid[i] = cv2.pyrDown(pyramid[i - 1])
    return pyramid


def cv2_pyramid_show(pyramid, canvas, column):
    for i in range(1, len(pyramid)):
        canvas.imshow(column, i, cv2_normalize(pyramid[i]), upscale=max(1, i - 1))


def cv2_width(image):
    return image.shape[1]


def cv2_height(image):
    return image.shape[0]
