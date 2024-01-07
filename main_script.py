import numpy as np
import cv2
import marking_buttons as mb


if __name__ == "__main__":

    image = cv2.imread("12.png")
    piano = mb.Piano(image)

    piano.prep()
    piano.holes()
    piano.first_level()
    piano.second_level()
    piano.black_marking()
    piano.marking_low_high()
    piano.center_marking()
    piano.final_marking()

    print(piano.final_cords)
    cap = cv2.VideoCapture("vid_test.mp4")

    while True:

        _, img = cap.read()

        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 100)

        alpha = 1.8  # Contrast control (1.0-3.0)
        beta = 0  # Brightness control (0-100)

        contrast = cv2.convertScaleAbs(blur, alpha=alpha, beta=beta)

        canny = cv2.Canny(contrast, 230, 255)

        kernel = np.ones((5, 5), np.uint8)
        dil = cv2.dilate(canny, kernel, iterations=3)
        er = cv2.erode(dil, kernel, iterations=3)

        matrix = np.copy(er).astype('uint8')

        for k in piano.centers:
            area_1 = matrix[100][k] > 0 or matrix[99][k] > 0 or matrix[98][k] > 0
            area_2 = matrix[97][k] > 0 or matrix[96][k] > 0 or matrix[95][k] > 0
            area_3 = matrix[94][k] > 0 or matrix[93][k] > 0 or matrix[92][k] > 0
            if area_1 or area_2 or area_3:
                cv2.circle(matrix, (k, 100), 20, (255, 0, 0), -1)

        for k in piano.centers:
            cv2.circle(matrix, (k, 100), 1, (255, 0, 0), -1)

        # Рисуем центры всех клавиш
        for i in range(0, len(piano.centers)):
            for p in range(0, 1000):
                cv2.circle(matrix, (piano.centers[i], img.shape[0]-90-p), 1, (255, 255, 255), -1)

        cv2.imshow('res', matrix)

        if cv2.waitKey(50) & 0xFF == ord('q'):
            break
