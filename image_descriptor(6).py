import cv2
import matplotlib.pyplot as plt
import numpy as np


def image_read(FileIm):
    image = cv2.imread(FileIm)
    plt.imshow(image)
    plt.title(f'Початкове зображення {FileIm}')
    plt.show()

    return image


def image_processing(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # Define range of color to highlight (in HSV)
    lower_color = np.array([87, 70, 20])
    upper_color = np.array([100, 255, 65])
    # Create a mask
    mask = cv2.inRange(hsv, lower_color, upper_color)
    # Apply the mask to the original image
    highlighted_img = cv2.bitwise_and(image, image, mask=mask)
    cv2.imshow('Highlighted image', highlighted_img)

    image_segments = image.copy()
    image_segments[mask > 0] = (0, 0, 255)
    cv2.imshow('Image segments', image_segments)

    return mask, highlighted_img


def image_processing2(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # Define range of color to highlight (in HSV)
    lower_color = np.array([63, 20, 25])
    upper_color = np.array([130, 140, 50])
    # Create a mask
    mask = cv2.inRange(hsv, lower_color, upper_color)
    # Apply the mask to the original image
    highlighted_img = cv2.bitwise_and(image, image, mask=mask)
    cv2.imshow('Highlighted image', highlighted_img)

    image_segments = image.copy()
    image_segments[mask > 0] = (0, 0, 255)
    cv2.imshow('Image segments', image_segments)

    return mask, highlighted_img


def image_contours(image_entrance):
    cnts = cv2.findContours(image_entrance.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

    return cnts


def image_recognition(image_entr, image_cont, file_name):
    # image_entr = cv2.cvtColor(image_entr, cv2.COLOR_BGR2GRAY)
    total = 0
    for c in image_cont:
        area = cv2.contourArea(c)
        if area >= 70:
            cv2.drawContours(image_entr, [c], -1, (255, 255, 0), 4)
            total += 1

    print("Знайдено {0} озер".format(total))
    cv2.imwrite(file_name, image_entr)
    plt.imshow(image_entr)
    plt.title(f"Об'єкти ідентифікації {file_name}")
    plt.show()

    return


def sift_feature_matching(filename_1, filename_2):
    # Завантаження зображень
    img1 = cv2.imread(filename_1)  # Перше зображення
    img2 = cv2.imread(filename_2)  # Друге зображення

    # Зміна розміру зображень
    img1 = cv2.resize(img1, dsize=(950, 600), interpolation=cv2.INTER_CUBIC)
    img2 = cv2.resize(img2, dsize=(950, 600), interpolation=cv2.INTER_CUBIC)

    # Ініціалізація детектора SIFT
    sift = cv2.SIFT_create()

    # Знаходження ключових точок та дескрипторів
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)

    # Параметри FLANN
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=7)
    search_params = dict(checks=20)
    flann = cv2.FlannBasedMatcher(index_params, search_params)

    # Знаходження співпадінь з використанням knnMatch
    matches = flann.knnMatch(des1, des2, k=2)
    print(f'Загальна кількість співпадінь: {len(matches)}')

    # Створення маски для добрих співпадінь
    matchesMask = [[0, 0] for i in range(len(matches))]

    # Тест на співвідношення за методом Лове
    good_matches = 0
    for i, (m, n) in enumerate(matches):
        if m.distance < 0.75 * n.distance:
            matchesMask[i] = [1, 0]
            good_matches += 1

    # Параметри малювання
    draw_params = dict(matchColor=(0, 255, 0),
                       singlePointColor=(255, 0, 0),
                       matchesMask=matchesMask,
                       flags=cv2.DrawMatchesFlags_DEFAULT)

    # Малювання співпадінь
    img3 = cv2.drawMatchesKnn(img1, kp1, img2, kp2, matches, None, **draw_params)

    # Відображення результату
    cv2.imshow('sift_feature_matching', img3)
    if cv2.waitKey(0) & 0xff == 27:
        cv2.destroyAllWindows()

    # Ймовірність ідентифікації
    if len(matches) > 0:
        match_prob = good_matches / len(matches)
    else:
        match_prob = 0.0

    return good_matches, match_prob


if __name__ == '__main__':
    image_entrance = image_read("google maps.jpg")
    image_exit, highlighted_image = image_processing(image_entrance)
    image_cont = image_contours(image_exit)
    image_recognition(image_entrance, image_cont, "image_recognition_1.jpg")

    image_entrance2 = image_read("sentinel hub.jpg")
    image_exit2, highlighted_image2 = image_processing2(image_entrance2)
    image_cont2 = image_contours(image_exit2)
    image_recognition(image_entrance2, image_cont2, "image_recognition_2.jpg")

    image_recognition(highlighted_image, image_cont, "image_recognition_1.jpg")
    image_recognition(highlighted_image2, image_cont2, "image_recognition_2.jpg")
    good_matches, match_probability = sift_feature_matching("image_recognition_1.jpg", "image_recognition_2.jpg")
    print(f"Кількість гарних збігів: {good_matches}\nЙмовірність ідентифікації озер: {match_probability:.2f}")
