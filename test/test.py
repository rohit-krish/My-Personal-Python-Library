from mylib.show import stackIt

import numpy as np
import cv2

img = cv2.imread('./lenna.png')
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img_blur = cv2.GaussianBlur(img, (5, 5), 1)
img_canny = cv2.Canny(img_blur, 50, 100)
img_dilate = cv2.dilate(img_canny, np.ones((3, 3)), iterations=3)
img_erode = cv2.erode(img_dilate, np.ones((3, 3)), iterations=2)

images = [
    [img, img_gray, img_blur],
    [img_canny, img_dilate, img_erode],
]
labels = [
    ['img', 'img_gray', 'img_blur'],
    ['img_canny', 'img_dilate', 'img_erode']
]

cv2.imshow(
    'result', stackIt(
        images, labels, .5, 25, fontFace=cv2.FONT_HERSHEY_PLAIN,
        fontScale=1, color=(255, 0, 0), thickness=1
    )
)
cv2.waitKey(0)
