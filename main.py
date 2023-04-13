import cv2
import numpy as np
import find_pupils_class

# загрузить видеофайл
cap = cv2.VideoCapture('videoplayback.mp4')

# проверить, открыт ли файл успешно
if not cap.isOpened():
    print("Не удалось открыть видеофайл")

coordinates_arr = np.array([[0,0,0,0,0]]) # № кадра, x1, y1, x2, y2
i = 0 # № кадра

# установить позицию кадра
cap.set(cv2.CAP_PROP_POS_FRAMES, 1255) # пример для чтения 50-го кадра

# прочитать первый кадр из видео
ret, img = cap.read()

#while ret:
while i < 30:
    # поиск зрачков
    # кадр в черно-белое изображение для облегчения поиска контуров
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('images/gray.jpg', gray)  


    # бинаризовать изображение с помощью порогового значения
    thresh = cv2.threshold(gray,85, 255, cv2.THRESH_BINARY)[1]
    cv2.imwrite('images/thresh.jpg', thresh)  

    # удалить шум на изображении с помощью медианного фильтра
    thresh = cv2.medianBlur(thresh, 5)

    # найти закрашенные круги на изображении
    circles = cv2.HoughCircles(thresh, cv2.HOUGH_GRADIENT_ALT, dp=1, minDist=5, param1=30, param2=0, minRadius=17, maxRadius=22)

    # нарисовать найденные круги на изображении
    x1 = x2 = y1 = y2 = 0
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
                cv2.circle(img, (x, y), r, (0, 255, 0), 2)

        filename = 'images/test/circles_{}.jpg'.format(i)
        # сохранить изображение с нарисованными кругами
        cv2.imwrite(filename, img)        
        new_row = np.array([[i,x1,y1,x2,y2]])
        coordinates_arr = np.append(coordinates_arr, new_row, axis=0)

    i += 1
    ret, img = cap.read()

# освободить ресурсы
cap.release()
