import cv2
import mediapipe as mp

# Загрузка изображения из файла
image = cv2.imread('muz.jpg')
image = cv2.resize(image, None, fx=0.5, fy=0.5)
hands = mp.solutions.hands.Hands(max_num_hands=2) # Объект ИИ для определения ладони (установите max_num_hands=2)
draw = mp.solutions.drawing_utils # Для рисования ладони

imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # Конвертируем в RGB
results = hands.process(imageRGB) # Работа mediapipe

if results.multi_hand_landmarks:
    for handLms in results.multi_hand_landmarks:
        for id, lm in enumerate(handLms.landmark):
            h, w, c = image.shape
            cx, cy = int(lm.x * w), int(lm.y * h)

        draw.draw_landmarks(image, handLms, mp.solutions.hands.HAND_CONNECTIONS, draw.DrawingSpec(color=(0, 80, 255),  thickness=4, circle_radius=2)) # Рисуем ладонь с синими линиями

cv2.imshow("Hand", image) # Отображаем картинку
cv2.waitKey(0)
cv2.destroyAllWindows()
