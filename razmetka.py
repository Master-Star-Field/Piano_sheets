import numpy as np
import cv2


cords_white_buttons = {}
cords = []

image = cv2.imread("5.png")


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
level = 323
while j < image.shape[1]:
    if canny[image.shape[0]-level][j] > 0:
        j_val = j
        while canny[image.shape[0]-level][j] > 0 and j < image.shape[1]:
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

print(cords_white_buttons)
low_black_button = 0
low_high_cords = {}
n_button = 1
# разметка нижней границы чёрных клавиш
for n in range(1, len(cords_white_buttons)+1):
    if n in [1, 4, 7, 11, 14, 18, 21, 25, 28, 32, 35, 39, 42, 46, 49, 52]:
        pass

    else:

        if n in [2, 5, 8, 9, 12, 15, 16, 19, 22, 23, 26, 29, 30, 33, 36, 37, 40, 43, 44, 47, 50, 51]:
            print(n)
            j = cords_white_buttons[n][0] + int((cords_white_buttons[n][1] - cords_white_buttons[n][0])/3)

        if n in [3, 6, 10, 13, 17, 20, 24, 27, 31, 34, 38, 41, 45, 48]:
            print(n)
            j = cords_white_buttons[n][0] + int((cords_white_buttons[n][1] - cords_white_buttons[n][0])/1.5)

        i = 0
        while canny[image.shape[0]-level+i][j] < 1:
            i = i - 1
            if i < -image.shape[0]:
                i = low_black_button
                break
        low_black_button = i + image.shape[0] - level

        # разметка верхней границы чёрных клавиш
        a1 = cords_white_buttons[2][1] - cords_white_buttons[2][0]
        high_black_button = low_black_button - a1*4 - 10

        low_high_cords.update([(n_button, [low_black_button, high_black_button])])
        n_button += 1

print(low_high_cords)

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

# Рисуем чёрные клавиши
i = 1
j = 0
while i <= len(black_cords):
    while j < 2:
        for k in range(low_high_cords[i][1], low_high_cords[i][0]):
            cv2.circle(image, (black_cords[i][0], k), 0, (0, 0, 255), -1)
            cv2.circle(image, (black_cords[i][1], k), 0, (0, 0, 255), -1)

        j += 1
    i += 1
    j = 0


a = 1
while a <= len(black_cords):
    i = black_cords[a][0]
    while i <= black_cords[a][1]:
        cv2.circle(image, (i, low_high_cords[a][0]), 0, (0, 0, 255), -1)
        cv2.circle(image, (i, low_high_cords[a][1]), 0, (0, 0, 255), -1)
        i += 1
    a += 1


print(len(canny[0]))
print(cords_white_buttons)
print(black_cords)
print(low_high_cords)


cv2.imshow('res', image)
cv2.waitKey(0)
