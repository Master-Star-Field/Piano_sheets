import cv2
from time import sleep
import numpy as np

image = cv2.imread("1.png")


clahe = cv2.createCLAHE(clipLimit=92., tileGridSize=(1,1))

lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
l, a, b = cv2.split(lab)

l2 = clahe.apply(l)

lab = cv2.merge((l2, a, b))
img2 = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

thresh = 200 # порог

image3 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
ret,thresh_img = cv2.threshold(image3, thresh, 255, cv2.THRESH_BINARY) # становится бинарным

kernel = np.ones((3,3), np.uint8)
#closing = cv2.morphologyEx(thresh_img, cv2.MORPH_CLOSE, kernel)
opening = cv2.morphologyEx(thresh_img, cv2.MORPH_OPEN, kernel)

contours, hierarchy = cv2.findContours(thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


# for cnt in contours:
#     rect = cv2.minAreaRect(cnt)
#     box = cv2.boxPoints(rect)
#     box = np.int0(box)
#     cv2.drawContours(thresh_img, [box], 0, (255, 0, 0), 2)

img_contours = np.zeros(image.shape)
cv2.drawContours(img_contours, contours, -1, (255, 255, 255), 1)






cv2.imshow("frame1", thresh_img)
#cv2.imshow("frame", thresh_img)
cv2.waitKey(0)
cv2.destroyAllWindows()