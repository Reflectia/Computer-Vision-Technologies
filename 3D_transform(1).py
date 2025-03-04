from graphics import *
import numpy as np
import math as mt
import time


# ---------------------------------- координати паралелепіпеда ------------------------------------
xw = 600; yw = 600; st = 300
# розташування координат у строках: дальній чотирикутник - A B I M, ближній чотирикутник D C F E
Prlpd = np.array([[0, 0, 0, 1],
                  [st/2, 0, 0, 1],
                  [st/2, st/3, 0, 1],
                  [0, st/3, 0, 1],
                  [0, 0, st, 1],
                  [st/2, 0, st, 1],
                  [st/2, st/3, st, 1],
                  [0, st/3, st, 1]])    # по строках
print('Початкова матриця')
print(Prlpd)


# --------------------------------- функция проекції на xy, z=0 -------------------------------------
def ProjectXY(Figure):
    f = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 1]])    # по строках
    ft = f.T
    Prxy = Figure.dot(ft)
    print('проєкція на ху')
    print(Prxy)
    return Prxy


# -------------------------------------------- зміщення ----------------------------------------------
def ShiftXYZ(Figure, l, m, n):
    f = np.array([[1, 0, 0, l], [0, 1, 0, m], [0, 0, 1, n], [1, 0, 0, 1]])    # по строках
    ft = f.T
    Prxy = Figure.dot(ft)
    print('зміщення')
    print(Prxy)
    return Prxy


# -------------------------------------------- обертання коло х----------------------------------------
def insertX(Figure, TetaG):
    TetaR = (3/14*TetaG)/180
    f = np.array([[1, 0, 0, 0], [0, mt.cos(TetaR), mt.sin(TetaR), 0],
                  [0, -mt.sin(TetaR),  mt.cos(TetaR), 0], [0, 0, 0, 1]])
    ft = f.T
    Prxy = Figure.dot(ft)
    print('обертання коло х')
    print(Prxy)
    return Prxy


# -------------------------------------------- обертання коло y----------------------------------------
def insertY(Figure, TetaG):
    TetaR = (3/14*TetaG)/180
    f = np.array([[mt.cos(TetaR), 0, -mt.sin(TetaR), 0], [0, 1, 0, 0],
                  [mt.sin(TetaR), 0,  mt.cos(TetaR), 0], [0, 0, 0, 1]])
    ft = f.T
    Prxy = Figure.dot(ft)
    print('обертання коло y')
    print(Prxy)
    return Prxy


# -------------------------------------------- аксонометрія ----------------------------------------------
def dimetri(Figure, TetaG1, TetaG2):
    TetaR1 = (3/14*TetaG1)/180; TetaR2 = (3/14*TetaG2)/180
    f1 = np.array([[mt.cos(TetaR1), 0, -mt.sin(TetaR1), 0], [0, 1, 0, 0],
                   [mt.sin(TetaR1), 0, mt.cos(TetaR1), 1], [0, 0, 0, 0]])
    ft1 = f1.T
    Prxy1 = Figure.dot(ft1)
    f2 = np.array([[1, 0, 0, 0], [0, mt.cos(TetaR2), mt.sin(TetaR2), 0],
                   [0, -mt.sin(TetaR2),  mt.cos(TetaR2), 0], [0, 0, 0, 1]])
    ft2 = f2.T
    Prxy2 = Prxy1.dot(ft2)
    print('dimetri')
    print(Prxy2)
    return Prxy2


# -------------------------------------- функція побудови паралелепіпеда -----------------------------
def PrlpdWiz(Prxy, color='black'):
    Ax = Prxy[0, 0];  Ay = Prxy[0, 1]
    Bx = Prxy[1, 0];  By = Prxy[1, 1]
    Ix = Prxy[2, 0];  Iy = Prxy[2, 1]
    Mx = Prxy[3, 0];  My = Prxy[3, 1]

    Dx = Prxy[4, 0];  Dy = Prxy[4, 1]
    Cx = Prxy[5, 0];  Cy = Prxy[5, 1]
    Fx = Prxy[6, 0];  Fy = Prxy[6, 1]
    Ex = Prxy[7, 0];  Ey = Prxy[7, 1]

    obj = Polygon(Point(Ax, Ay), Point(Bx, By), Point(Ix, Iy), Point(Mx, My))
    obj.setOutline(color)  # Встановлення кольору контуру
    obj.draw(win)

    obj = Polygon(Point(Dx, Dy), Point(Cx, Cy), Point(Fx, Fy), Point(Ex, Ey))
    obj.setOutline(color)  # Встановлення кольору контуру
    obj.draw(win)

    obj = Polygon(Point(Ax, Ay), Point(Bx, By), Point(Cx, Cy), Point(Dx, Dy))
    obj.setOutline(color)  # Встановлення кольору контуру
    obj.draw(win)

    obj = Polygon(Point(Mx, My), Point(Ix, Iy), Point(Fx, Fy), Point(Ex, Ey))
    obj.setOutline(color)  # Встановлення кольору контуру
    obj.draw(win)

    return PrlpdWiz


colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'black', 'white']  # Список кольорів

# -------------------------------------------- побудова паралелепіпеда -----------------------------
win = GraphWin("3-D модель паралелепіпеда, аксонометрична проекція на ХУ", xw, yw)
win.setBackground('white')
xw = 600; yw = 600; st = 50; TetaG1 = 0
l = (xw/3)-st; m = (yw/3)-st; n = m
Prlpd1 = ShiftXYZ(Prlpd, l, m, n)
Prlpd2 = insertX(Prlpd1, TetaG1)
Prxy3 = ProjectXY(Prlpd2)

for i in range(8):
    time.sleep(0.3)
    PrlpdWiz(Prxy3, color=colors[i % len(colors)])  # Вибір кольору зі списку

win.getMouse()
win.close()

win = GraphWin("3-D модель паралелепіпеда, оберт коло Х, аксонометрична проекція на ХУ", xw, yw)
win.setBackground('white')
xw = 600; yw = 600; st = 50; TetaG1 = 180
l = (xw/3)-st; m = (yw/3)-st; n = m
Prlpd1 = ShiftXYZ(Prlpd, l, m, n)
Prlpd2 = insertX(Prlpd1, TetaG1)
Prxy3 = ProjectXY(Prlpd2)

for i in range(8):
    time.sleep(0.3)
    PrlpdWiz(Prxy3, color=colors[i % len(colors)])  # Вибір кольору зі списку

win.getMouse()
win.close()

win = GraphWin("3-D паралелепіпед, діметричний оберт навколо Х та У, аксонометрична проекція на ХУ", xw, yw)
win.setBackground('white')
xw = 600; yw = 600; st = 50; TetaG1 = 180; TetaG2 = -90
l = (xw/2)-st; m = (yw/2)-st; n = m
Prlpd1 = ShiftXYZ(Prlpd, l, m, n)
Prlpd2 = dimetri(Prlpd1, TetaG1, TetaG2)
Prxy3 = ProjectXY(Prlpd2)

for i in range(24):
    time.sleep(0.1)
    PrlpdWiz(Prxy3, color=colors[i % len(colors)])  # Вибір кольору зі списку

win.getMouse()
win.close()


win = GraphWin("3-D паралелепіпед, анімація обертання навколо вісі Y у діметричній проєкції", xw, yw)
win.setBackground('white')
xw = 600; yw = 600; st = 50; TetaG1 = 180; TetaG2 = -90
l = (xw/2)-st; m = (yw/2)-st; n = m

Prlpd1 = ShiftXYZ(Prlpd, l, m, n)
Prlpd2 = dimetri(Prlpd1, TetaG1, TetaG2)

for i in range(15):
    time.sleep(0.3)
    Prlpd3 = insertY(Prlpd2, TetaG2)
    Prxy3 = ProjectXY(Prlpd3)

    for i in range(7):
        time.sleep(0.05)
        PrlpdWiz(Prxy3, color=colors[i % len(colors)])  # Вибір кольору зі списку

    TetaG2 += 20

win.getMouse()
win.close()
