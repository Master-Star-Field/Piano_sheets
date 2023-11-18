import numpy as np
import cv2


cords_white_buttons = {}
cords = []

image = cv2.imread("6.png")

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

"""--------- заполнение дыр ---------"""
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
    if canny[image.shape[0]-10][j] > 0:
        j_val = j
        while canny[image.shape[0]-10][j] > 0 and j < image.shape[1]:
            j += 1
        j_val = j_val + int((j - j_val) / 2)
        cords.append(j_val)
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


score = 1
for i in range(0, len(cords)):
    cords_white_buttons.update([(score, cords[i])])
    score += 1


print(cords)
print(len(cords))
print(cords_white_buttons)
print(len(cords_white_buttons))


i = 1
j = 0
while i <= len(cords_white_buttons):
    while j < 2:
        for k in range(0, image.shape[1]):
            cv2.circle(image, (cords_white_buttons[i], k), 1, (255, 0, 0), -1)

        j += 1
    i += 1
    j = 0


print(sorted(cords))
print(len(cords))

cv2.imshow('res', image)
cv2.waitKey(0)
