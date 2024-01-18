from ultralytics import YOLO
import cv2
import numpy as np
import torch


def kmeans_color(image, label):
    # Загрузка цветного изображения

    # Преобразование изображения в одномерный массив
    data = image.reshape((-1, 3))

    # Преобразование в тип данных с плавающей запятой
    data = np.float32(data)

    # Определение критериев останова для алгоритма к-средних
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)

    # Применение алгоритма к-средних для четырех регионов
    _, labels4, centers4 = cv2.kmeans(data, 7, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    # Конвертация центров кластеров обратно в тип данных с плавающей запятой
    centers4 = np.uint8(centers4)

    # Преобразование меток обратно в изображение

    segmented_image4 = centers4[labels4.flatten()]
    segmented_image4 = segmented_image4.reshape(image.shape)

    # cv2.imwrite(f"dataset/image{label}.png", segmented_image4)
    return segmented_image4


if __name__ == '__main__':

    label = 111
    model = YOLO("weights/best.pt")
    photo = cv2.imread("7.png")
    gray = cv2.cvtColor(photo, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 100)
    print(kmeans_color(blur, label).shape)
    # model.predict(kmeans_color(blur, label), save=True, imgsz=(1912, 273))
