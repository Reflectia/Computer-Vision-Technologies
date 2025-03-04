import matplotlib.colors as colors
from PIL import Image, ImageDraw
from matplotlib import pyplot as plt


# --------------------- зчитування файлу зображення ----------------------
def image_read(file_name: str):
    image = Image.open(file_name)  # відкриття файлу зображення
    draw = ImageDraw.Draw(image)  # створення інструменту для малювання
    width = image.size[0]   # визначення ширини картинки
    height = image.size[1]  # визначення висоти картинки
    pix = image.load()  # отримання значень пікселей для картинки
    print("Initial_im", "red=", pix[1, 1][0], "green=", pix[1, 1][1], "blue=", pix[1, 1][2])
    plt.xlim(width)
    plt.ylim(height)
    plt.imshow(image)
    plt.show()
    image_info = {"image_file": image, "image_draw": draw, "image_width": width, "image_height": height, "image_pix": pix}

    return image_info


# ----------------------- негатив --------------------------
def negative(file_name_start, file_name_stop, grad=False):
    image_info = image_read(file_name_start)
    image = image_info["image_file"]
    draw = image_info["image_draw"]
    width = image_info["image_width"]
    height = image_info["image_height"]
    pix = image_info["image_pix"]

    result_matrix = generate_matrix(width, height)

    print('------- триває перетворення --------------')
    for i in range(width):
        for j in range(height):
            a = pix[i, j][0]
            b = pix[i, j][1]
            c = pix[i, j][2]
            if grad:
                # від кожного пікселя віднімається 255 - макс. значення для кольору + градієнт
                a = 255 - a - result_matrix[i][j]
                b = 255 - b - result_matrix[i][j]
                c = 255 - c - result_matrix[i][j]
            else:
                a = 255 - a
                b = 255 - b
                c = 255 - c
            # перетворення RGB в шістнадцятирічний код з пакету matplotlib
            red = a/255
            red_n = 1 if red > 1 else (0 if red < 0 else red)
            green = b/255
            green_n = 1 if green > 1 else (0 if green < 0 else green)
            blue = c/255
            blue_n = 1 if blue > 1 else (0 if blue < 0 else blue)
            col16 = colors.rgb2hex((red_n, green_n, blue_n))
            # інтеграція змінної до поля строки: конкатенація рядків
            draw.point((i, j), ''+col16)

    plt.imshow(image)
    plt.show()
    print("Result_im", "red=", pix[1, 1][0], "green=", pix[1, 1][1], "blue=", pix[1, 1][2])
    image.save(file_name_stop, "JPEG")
    del draw
    print('------- перетворення збережене до файлу stop.jpg --------------')

    return


# ---------------------- зміна яскравості  --------------------
def brightness_change(file_name_start, file_name_stop, grad=False):

    image_info = image_read(file_name_start)
    image = image_info["image_file"]
    draw = image_info["image_draw"]
    width = image_info["image_width"]
    height = image_info["image_height"]
    pix = image_info["image_pix"]

    print('введіть діапазон зміни яскравості: -100, +100')
    factor = int(input('factor:'))  # наприклад в діапазоні +100, -100

    result_matrix = generate_matrix(width, height)

    print('------- триває перетворення --------------')
    for i in range(width):
        for j in range(height):
            if grad:
                # додавання яскравості + градієнт
                a = pix[i, j][0] + factor + result_matrix[i][j]
                b = pix[i, j][1] + factor + result_matrix[i][j]
                c = pix[i, j][2] + factor + result_matrix[i][j]
            else:
                a = pix[i, j][0] + factor
                b = pix[i, j][1] + factor
                c = pix[i, j][2] + factor
            # перетворення RGB в шістнадцятирічний код з пакету matplotlib
            red = a / 255
            red_n = 1 if red > 1 else (0 if red < 0 else red)
            green = b / 255
            green_n = 1 if green > 1 else (0 if green < 0 else green)
            blue = c / 255
            blue_n = 1 if blue > 1 else (0 if blue < 0 else blue)
            col16 = colors.rgb2hex((red_n, green_n, blue_n))
            # інтеграція змінної до поля строки: конкатенація строк
            draw.point((i, j), '' + col16)

    plt.imshow(image)
    plt.show()
    print("Result_im", "red=", pix[1, 1][0], "green=", pix[1, 1][1], "blue=", pix[1, 1][2])
    image.save(file_name_stop, "JPEG")
    del draw
    print('------- перетворення збережене до файлу stop.jpg --------------')

    return


# матриця зі збільшенням значень від верхнього лівого кута до правого нижнього
def generate_matrix(rows, cols):

    matrix = [[0] * cols for _ in range(rows)]

    increment_x = -50

    for i in range(rows):
        increment_y = -50
        for j in range(cols):
            matrix[i][j] = increment_x + increment_y
            increment_y += 0.1
        increment_x += 0.1

    return matrix


# ---------------------------------- головні виклики  --------------------------------
if __name__ == "__main__":

    print('Приклад матриці з градієнтом')
    result_matrix = generate_matrix(10, 8)
    for row in result_matrix:
        print(row)

    file_name_start = 'Himalayas.jpg'
    # file_name_start = "Iceland Mountains.jpg"
    file_name_stop = "file_stop.jpg"

    print('Вітаю! Оберіть тип перетворення)')
    print('1 - негатив')
    print('2 - зміна яскравості')
    mode = int(input('mode:'))
    if mode == 1:
        negative(file_name_start, file_name_stop, grad=True)
    elif mode == 2:
        brightness_change(file_name_start, file_name_stop, grad=True)
