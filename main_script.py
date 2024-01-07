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

        # Рисуем центры всех клавиш
        for i in range(0, len(piano.centers)):
            for p in range(0, 1000):
                cv2.circle(img, (piano.centers[i], img.shape[0]-90-p), 1, (0, 255, 0), -1)

        cv2.imshow('res', img)

        if cv2.waitKey(50) & 0xFF == ord('q'):
            break
