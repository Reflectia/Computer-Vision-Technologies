import cv2
import time
import matplotlib.pyplot as plt
import numpy as np


def image_contours(image_entrance):
    cnts = cv2.findContours(image_entrance.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

    return cnts


def image_recognition(image_entrance, image_cont):
    total = 0
    for c in image_cont:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.015 * peri, True)
        if 10 <= len(approx) <= 13:
            cv2.drawContours(image_entrance, [approx], -1, (0, 255, 0), 3)
            total += 1

    print("Знайдено {0} контурів людей".format(total))

    cv2.imshow("recognition", image_entrance)

    return


# -------------------- завантаження відео з файлу ----------------------
cap = cv2.VideoCapture('istockphoto3.mp4')


# Get total number of frames in the video
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
middle_frame_index = total_frames // 2
# Set the frame position to the middle frame
cap.set(cv2.CAP_PROP_POS_FRAMES, middle_frame_index)
ret, frame = cap.read()

# ----------------- Гістограма  яскравості зображення ---------
frame_shape = frame.shape
imS = cv2.resize(frame, (int(frame_shape[1] / 1.5), int(frame_shape[0] / 1.5)))
# opencv uses BGR
cv2.imshow("img", imS)
plt.hist(frame.ravel(), 256, (0, 256))
plt.show()

# -------------------- Вирівнювання гістограми  --------------
# Convert the frame to grayscale
frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # після цього вже не буде кольоровою, тільки сірою
hist, bins = np.histogram(frame_gray.flatten(), 256, [0, 256])
cdf = hist.cumsum()
cdf_normalized = cdf * hist.max() / cdf.max()  # Визначення нормалізоуючої кривої
plt.plot(cdf_normalized, color='b')
plt.hist(frame_gray.flatten(), 256, (0, 256), color='r')
plt.xlim([0, 256])
plt.legend(('cdf', 'histogram'), loc='upper left')
plt.show()

equ = cv2.equalizeHist(frame_gray)
# з'єднання початкового зображення і результату
res = np.hstack((frame_gray, equ))
imS = cv2.resize(res, (800, 300))
plt.imshow(imS)
plt.show()

# convert to RGB (from 2 dimensions to 3) нема сенсу


cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

while True:
    ret, frame = cap.read()

    time.sleep(0.02)

    frame = cv2.resize(frame, (400, 250))

    # -------------------- Вирівнювання гістограми  --------------
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    hist, bins = np.histogram(frame_gray.flatten(), 256, [0, 256])
    cdf = hist.cumsum()
    cdf_normalized = cdf * hist.max() / cdf.max()  # Визначення нормалізуючої кривої

    equ = cv2.equalizeHist(frame_gray)  # вирівнення яскравості

    gray_normalized = cv2.normalize(equ, None, 20, 240, cv2.NORM_MINMAX)

    blur1 = cv2.GaussianBlur(gray_normalized, (11, 11), 0)
    blur2 = cv2.GaussianBlur(blur1, (9, 9), 0)
    blur3 = cv2.GaussianBlur(blur2, (5, 5), 0)

    cv2.imshow("blur1", blur3)

    kenny1 = cv2.Canny(blur3, 50, 140)  # сегментація за Кенні

    cv2.imshow("kenny1", kenny1)

    image_cont = image_contours(kenny1)
    image_recognition(frame, image_cont)

    # ------ відображення змін значень пікселей потокового відео - динамічних картинок
    # print(frame)
    # ------ умова завершення відображення відеопотоку за клавішею q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
