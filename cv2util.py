from __future__ import (absolute_import, division, print_function, unicode_literals)
from builtins import *
import numpy as np
import cv2


def cv2_upscale(image, factor=2):
    dsize = (int(image.shape[1] * factor), int(image.shape[0] * factor))
    return cv2.resize(image, dsize=dsize, interpolation=cv2.INTER_NEAREST)

def cv2_pad(image, top=0, bottom=0, left=0, right=0, value=0):
    borderType = cv2.BORDER_CONSTANT
    return cv2.copyMakeBorder(image, top, bottom, left, right, borderType, None, value)


def cv2_downscale(image, factor=2):
    return cv2_upscale(image, factor=1.0 / float(factor))


def cv2_normalize(image, max=None):
    if max is None:
        return image * 255.0 / np.max(image)
    else:
        return np.clip(image * 255.0 / max, 0.0, 255.0)


def cv2_normalize_to_255(image):
    return (image - np.min(image)) / (np.max(image) - np.min(image)) * 255.0


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


def cv2_putText(img, text, org, color=255, fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1.0, thickness=2, lineType=None, bottomLeftOrigin=None):
    """like cv2.putText, but with reasonable defaults"""
    cv2.putText(img, text, org, fontFace, fontScale, color, thickness, lineType, bottomLeftOrigin)

def cv2_gray2rgb(image):
    return cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)

def cv2_rgb2gray(image):
    return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)