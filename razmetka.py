import numpy as np
import cv2


cords_white_buttons = {}
cords = []

image = cv2.imread("7.png")


""" ---------------------------- Подготовка изображения ---------------------------"""
gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
# gray = cv2.GaussianBlur(gray, (3, 3), 10)
alpha = 2.5  # Contrast control (1.0-3.0)
beta = 10  # Brightness control (0-100)

contrast = cv2.convertScaleAbs(gray, alpha=alpha, beta=beta)

print(gray.shape)
canny = cv2.Canny(contrast, 0, contrast.max()-150)

kernel = np.ones((5, 5), np.uint8)
dil = cv2.dilate(canny, kernel, iterations=1)
canny = dil

""" -------------------------------- заполнение дыр --------------------------------"""
num = 1
Y, X = canny.shape
nearest_neigbours = [[
    np.argmax(
        np.bincount(
            canny[max(i - num, 0):min(i + num, Y), max(j - num, 0):min(j + num, X)].ravel()))
    for j in range(X)] for i in range(Y)]
canny = np.array(nearest_neigbours, dtype=np.uint8)

""" ----------------------------- 1й уровень обработки -----------------------------"""
j = 0
while j < image.shape[1]:
    if canny[image.shape[0]-323][j] > 0:
        j_val = j
        while canny[image.shape[0]-323][j] > 0 and j < image.shape[1]:
            j += 1
        j_val = j_val + int((j - j_val) / 2)
        cords.append(j_val-1)
    j += 1


"""------------ 2й уровень обработки (алгоритм) доработаю завтра нужно сделать пару моментов -------------"""
print(cords)
l1 = cords[1] - cords[0]
l2 = cords[2] - cords[1]

area_1 = (cords[0]/(cords[1]-cords[0]) > 1.2) and (cords[0]/(cords[1]-cords[0]) < 2.2)
area_2 = (cords[0]/(cords[1]-cords[0]) >= 2.2) and (cords[0]/(cords[1]-cords[0]) < 3.1)

if area_1:
    cords.append(cords[0] - int(cords[1] - cords[0]))
    cords.sort()
if area_2:
    cords.append(cords[0] - int(cords[1] - cords[0]))
    cords.sort()
    cords.append(cords[0] - int(cords[1] - cords[0]))
    cords.sort()

l_etal = l1
for i in range(1, len(cords)):
    if ((cords[i] - cords[i-1])/l_etal > 1.5) and ((cords[i] - cords[i-1])/l_etal < 2.7):
        cords.append(cords[i] - int((cords[i]-cords[i-1])/2))
        cords.sort()
    elif (cords[i] - cords[i-1])/l_etal >= 2.7:
        cords.append(cords[i] - int((cords[i]-cords[i-1])/2))
        cords.sort()
        cords.append(cords[i] - int((cords[i]-cords[i-1])/2))
        cords.sort()


# Словарь для прорезей
score = 2
cords_white_buttons.update([(1, [0, cords[0]])])
for i in range(1, len(cords)):
    cords_white_buttons.update([(score, [cords[i-1], cords[i]])])
    score += 1


# Рисуем прорези для белых клавиш
i = 1
j = 0
while i <= len(cords_white_buttons):
    while j < 2:
        for k in range(int(image.shape[0]/1.5), image.shape[0]):
            cv2.circle(image, (cords_white_buttons[i][1], k), 1, (255, 0, 0), -1)

        j += 1
    i += 1
    j = 0


""" ------------------------ Алгоритм для разметки чёрных клавиш -----------------------"""
black_cords = {}
score = 0

for i in range(1, len(cords_white_buttons)):
    if i in [2, 5, 9, 12, 16, 19, 23, 26, 30, 33, 37, 40, 44, 47, 51]:
        pass

    elif i in [1, 4, 8, 11, 15, 18, 22, 25, 29, 32, 36, 39, 43, 46, 50]:
        score += 1

        if i == 1:
            l_black = cords_white_buttons[i][1] - int(
                (cords_white_buttons[i + 1][1] - cords_white_buttons[i + 1][0]) * 3 / 15)
            r_black = cords_white_buttons[i][1] + int(
                (cords_white_buttons[i + 1][1] - cords_white_buttons[i + 1][0]) * 6 / 15)
            black_cords.update([(score, [l_black, r_black])])

        else:
            l_black = cords_white_buttons[i][1] - int(
                (cords_white_buttons[i][1] - cords_white_buttons[i][0]) * 3 / 15)
            r_black = cords_white_buttons[i][1] + int(
                (cords_white_buttons[i + 1][1] - cords_white_buttons[i + 1][0]) * 6 / 15)
            black_cords.update([(score, [l_black, r_black])])

    elif i in [3, 6, 10, 13, 17, 20, 24, 27, 31, 34, 38, 41, 45, 48]:
        score += 1

        l_black = cords_white_buttons[i][1] - int(
            (cords_white_buttons[i][1] - cords_white_buttons[i][0]) * 6 / 15)
        r_black = cords_white_buttons[i][1] + int(
            (cords_white_buttons[i + 1][1] - cords_white_buttons[i + 1][0]) * 3 / 15)
        black_cords.update([(score, [l_black, r_black])])

    elif i in [7, 14, 21, 28, 35, 42, 49]:
        score += 1

        l_black = cords_white_buttons[i][1] - int(
            (cords_white_buttons[i][1] - cords_white_buttons[i][0]) * 9 / 30)
        r_black = cords_white_buttons[i][1] + int(
            (cords_white_buttons[i + 1][1] - cords_white_buttons[i + 1][0]) * 9 / 30)
        black_cords.update([(score, [l_black, r_black])])


# Рисуем чёрные клавиши
i = 1
j = 0
while i <= len(black_cords):
    while j < 2:
        for k in range(0, int(image.shape[0]/1.5)):
            cv2.circle(image, (black_cords[i][0], k), 0, (0, 0, 255), -1)
            cv2.circle(image, (black_cords[i][1], k), 0, (0, 0, 255), -1)

        j += 1
    i += 1
    j = 0


print(len(cords_white_buttons))
print(cords_white_buttons)
print(black_cords)


cv2.imshow('res', image)
cv2.waitKey(0)
