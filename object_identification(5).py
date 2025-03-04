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
    highlighted_image = cv2.bitwise_and(image, image, mask=mask)
    cv2.imshow('Highlighted image', highlighted_image)

    image_segments = image.copy()
    image_segments[mask > 0] = (0, 0, 255)
    cv2.imshow('Image segments', image_segments)

    return mask


def image_processing2(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # Define range of color to highlight (in HSV)
    lower_color = np.array([63, 20, 25])
    upper_color = np.array([130, 140, 50])
    # Create a mask
    mask = cv2.inRange(hsv, lower_color, upper_color)
    # Apply the mask to the original image
    highlighted_image = cv2.bitwise_and(image, image, mask=mask)
    cv2.imshow('Highlighted image', highlighted_image)

    image_segments = image.copy()
    image_segments[mask > 0] = (0, 0, 255)
    cv2.imshow('Image segments', image_segments)

    return mask


def image_contours(image_entrance):
    cnts = cv2.findContours(image_entrance.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

    return cnts


def image_recognition(image_entrance, image_cont, file_name):
    total = 0
    for c in image_cont:
        area = cv2.contourArea(c)
        if area >= 70:
            cv2.drawContours(image_entrance, [c], -1, (255, 255, 0), 4)
            total += 1

    print("Знайдено {0} озер".format(total))
    cv2.imwrite(file_name, image_entrance)
    plt.imshow(image_entrance)
    plt.title(f"Об'єкти ідентифікації {file_name}")
    plt.show()

    return


if __name__ == '__main__':

    image_entrance = image_read("google maps.jpg")
    image_exit = image_processing(image_entrance)
    image_cont = image_contours(image_exit)
    image_recognition(image_entrance, image_cont, "image_recognition_1.jpg")

    image_entrance = image_read("sentinel hub.jpg")
    image_exit = image_processing2(image_entrance)
    image_cont = image_contours(image_exit)
    image_recognition(image_entrance, image_cont, "image_recognition_2.jpg")
