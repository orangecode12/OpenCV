import numpy as np
import cv2

def find_pupils(i, img, old_row):
# поиск зрачков
    # кадр в черно-белое изображение для облегчения поиска контуров
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # бинаризовать изображение с помощью порогового значения
    thresh = cv2.threshold(gray,85, 255, cv2.THRESH_BINARY)[1]

    # удалить шум на изображении с помощью медианного фильтра
    thresh = cv2.medianBlur(thresh, 5)

    # найти закрашенные круги на изображении
    circles = cv2.HoughCircles(thresh, cv2.HOUGH_GRADIENT_ALT, dp=1, minDist=5, param1=30, param2=0, minRadius=17, maxRadius=22)

    # нарисовать найденные круги на изображении
    a, x1, y1, x2, y2 = old_row[0]
   # x1 = x2 = y1 = y2 = 0
    if circles is not None:
        circles = circles[0, :].astype("int")
        for (x, y, r) in circles:
            if y > 150 and y < 190:
                if x < 200:
                    x1 = x
                    y1 = y
                else:
                    x2 = x
                    y2 = y
    new_row = np.array([[i,x1,y1,x2,y2]])
    return new_row
        