import cv2
import numpy as np


def blur_masks(img_path):

    dilation = cv2.dilate(img_path, kernel, iterations=3)
    blur = cv2.GaussianBlur(dilation, (13, 13), 5)
    return blur


input_path = r'\\asaf_pc\d$\Masks'
output_path = r'\\asaf_pc\d$\RenderMasks'

kernel = np.ones((7, 7), np.uint8)

for cam in range(1, 38 + 1):
    Masks = cv2.imread(near_layer_input_path + r'\%04d.jpg' % cam)
    Render = blur_masks(Masks)
    cv2.imwrite(RenderMasks + r'\%04d.jpg' % cam, Render)
    print 'Saving Blurred Dilated Image of camera {} \n to {} \n' .format(cam, RenderMasks)

