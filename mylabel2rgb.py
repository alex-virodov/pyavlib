import numpy as np
import cv2

def mylabel2rgb(label_image):
    # http://godsnotwheregodsnot.blogspot.com/2012/09/color-distribution-methodology.html
    color_list = [
        # 0 0 0
        (1, 0, 103),
        (213, 255, 0),
        (255, 0, 86),
        (158,0,142),
        (14,76,161),
        (255,229,2),
        (0,95,57),
        (0,255,0),
        (149,0,58),
        (255,147,126),
        (164,36,0),
        # (0,21,68),
        (145,208,203),
        # (98,14,0),
        (107,104,130),
        #,0,0,255),
        (0,125,181),
        (106,130,108),
        (0,174,126),
        (194,140,159),
        (190,153,112),
        (0,143,156),
        (95,173,78),
        #,255,0,0),
        (255,0,246),
        (255,2,157),
        (104,61,59),
        (255,116,163),
        (150,138,232),
        (152,255,82),
        (167,87,64),
        (1,255,254),
        (255,238,232),
        (254,137,0),
        (189,198,255),
        (1,208,255),
        (187,136,0),
        (117,68,177),
        (165,255,210),
        (255,166,254),
        (119,77,0),
        (122,71,130),
        (38,52,0),
        (0,71,84),
        #(67,0,44),
        (181,0,255),
        (255,177,103),
        (255,219,102),
        (144,251,146),
        (126,45,210),
        (189,211,147),
        (229,111,254),
        (222,255,116),
        (0,255,120),
        (0,155,255),
        (0,100,1),
        (0,118,255),
        (133,169,0),
        (0,185,23),
        (120,130,49),
        (0,255,198),
        (255,110,65),
        (232,94,190),
    ]
    result = np.zeros(shape=(label_image.shape[0], label_image.shape[1], 3), dtype=np.uint8)
    # -1, 0, 1 have special colors: -1=Red, 0=Black, 1=Blue
    result[label_image == -1] = (0, 0, 255)
    result[label_image == 1] = (255, 0, 0)
    for i in range(2, np.max(label_image)+1):
        result[label_image == i] = color_list[i % len(color_list)]
    return result

if __name__ == "__main__":
    from pyavlib.cv2util import cv2_waitKey, cv2_upscale
    image = np.zeros(shape=(80, 80), dtype=np.int8)

    for i in range(64):
        x = i % 8
        y = i // 8
        image[y*10+2:y*10+6, x*10+2:x*10+6] = i - 1

    cv2.imshow(__file__, cv2_upscale(mylabel2rgb(image), 4))
    cv2_waitKey(__file__, 0)
    cv2.destroyAllWindows()
