import numpy as np
import cv2

cap = cv2.VideoCapture("videos/vid_1.mp4")

while True:
    _, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    #blur = cv2.GaussianBlur(gray, (5, 5), 100)

    alpha = 3.9  # Contrast control (1.0-3.0)
    beta = 0  # Brightness control (0-100)

    contrast = cv2.convertScaleAbs(gray, alpha=alpha, beta=beta)

    canny = cv2.Canny(contrast, 200, 220)

    kernel = np.ones((7, 7), np.uint8)
    dil = cv2.dilate(canny, kernel, iterations=1)

    matrix = np.copy(dil).astype('uint8')

    k = 18

    while k < 1909:
        area_1 = matrix[100][k] > 0 or matrix[99][k] > 0 or matrix[98][k] > 0
        area_2 = matrix[97][k] > 0 or matrix[96][k] > 0 or matrix[95][k] > 0
        area_3 = matrix[94][k] > 0 or matrix[93][k] > 0 or matrix[92][k] > 0
        if area_1 or area_2 or area_3:
            cv2.circle(matrix, (k, 100), 20, (255, 0, 0), -1)
        k += 37

    k = 18
    while k < 1909:
        cv2.circle(matrix, (k, 100), 1, (255, 0, 0), -1)
        k += 37



    cv2.imshow('res', matrix)

    if cv2.waitKey(50) & 0xFF == ord('q'):
        break
