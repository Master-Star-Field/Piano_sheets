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
        print(img.shape)
        gray = cv2.cvtColor(img[:][:600], cv2.COLOR_RGB2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 100)

        alpha = 1.5  # Contrast control (1.0-3.0)
        beta = 0  # Brightness control (0-100)

        contrast = cv2.convertScaleAbs(blur, alpha=alpha, beta=beta)

        canny = cv2.Canny(contrast, 230, 255)
        kernel = np.ones((7, 7), np.uint8)
        erode = cv2.erode(canny, kernel, iterations=1)

        for i in range(0, len(piano.centers)):
            area_1 = canny[100][piano.centers[i]] > 0 or canny[99][piano.centers[i]] > 0 or canny[98][piano.centers[i]] > 0
            area_2 = canny[97][piano.centers[i]] > 0 or canny[96][piano.centers[i]] > 0 or canny[95][piano.centers[i]] > 0
            area_3 = canny[94][piano.centers[i]] > 0 or canny[93][piano.centers[i]] > 0 or canny[92][piano.centers[i]] > 0
            if area_1 or area_2 or area_3:
                cv2.circle(img, (piano.centers[i], 100), 20, (255, 0, 0), -1)

        for i in range(0, len(piano.centers)):
            cv2.circle(img, (piano.centers[i], 100), 1, (255, 0, 0), -1)

        # Рисуем центры всех клавиш
        for i in range(0, len(piano.centers)):
            for p in range(0, 1000):
                cv2.circle(img, (piano.centers[i], img.shape[0]-90-p), 1, (255, 255, 255), -1)

        cv2.imshow('res', img)

        if cv2.waitKey(50) & 0xFF == ord('q'):
            break
