from graphics import *
import time
import numpy as np
import math as mt

# ----------------              І. Переміщення              ------------------------
# ---------------- формування та відображення статичного трикутника ------------------------

xw = 600; yw = 600; st = 50                         # розміри графічного вікна та параметри перетворень
win = GraphWin("2-D проекції в библіотеці graphics", xw, yw)
win.setBackground('white')
# розміри трикутника (прямокутний)
dx = 50; dy = 60
# координати трикутника
x1 = st; y1 = yw - st
x2 = st; y2 = yw - st - dy
x3 = st+dx; y3 = yw - st

obj = Polygon(Point(x1, y1), Point(x2, y2), Point(x3, y3))
obj.draw(win)
win.getMouse()
win.close()

# -------------------------Циклічне переміщення типу "РУХ" матричними операціями-----------------
win = GraphWin("2-D проекції в библиотеці graphics ПЕРЕНОС З РУХОМ матрицями", xw, yw)
win.setBackground('white')

# -------------------------блок матричних перетворень типу ПЕРЕМІЩЕННЯ----------------------------
a = np.array([[x1, y1, 1]])
f = np.array([[1, 0, dx], [0, 1, -dy], [0, 0, 1]])    # матриця фігури по строках
ft = f.T                                                  # транспонована матриця
total = a.dot(ft)                                       # множення для перетворень 1 точки
x11 = total[0, 0];  y11 = total[0, 1]
a2 = np.array([[x2, y2, 1]])
f2 = np.array([[1, 0, dx], [0, 1, -dy], [0, 0, 1]])
ft2 = f2.T
total2 = a2.dot(ft2)
x22 = total2[0, 0];  y22 = total2[0, 1]                     # множення для перетворень 2 точки
a3 = np.array([[x3, y3, 1]])
f3 = np.array([[1, 0, dx], [0, 1, -dy], [0, 0, 1]])
ft3 = f3.T
total3 = a3.dot(ft3)
x33 = total3[0, 0];  y33 = total3[0, 1]                     # множення для перетворень 3 точки

# ----------------------------- малювання першого трикутника -----------------------------------
obj = Polygon(Point(x1, y1), Point(x2, y2), Point(x3, y3))
obj.draw(win)

stop = xw/dx
stop = float(stop)
ii = int(stop)

for i in range(ii):
    time.sleep(0.2)                               # затримка зображення на екрані
    # obj.setOutline("white")                       # замальовування попереднього трикутника під фон
    obj = Polygon(Point(x11, y11), Point(x22, y22), Point(x33, y33))
    obj.draw(win)
    # ---------------------циклічний блок матричних перетворень типу ПЕРЕМІЩЕННЯ------------------
    a = np.array([[x11, y11, 1]])
    f = np.array([[1, 0, dx], [0, 1, -dy], [0, 0, 1]])
    ft = f.T
    total = a.dot(ft)
    x11 = total[0, 0]
    y11 = total[0, 1]
    a2 = np.array([[x22, y22, 1]])
    f2 = np.array([[1, 0, dx], [0, 1, -dy], [0, 0, 1]])
    ft2 = f2.T
    total2 = a2.dot(ft2)
    x22 = total2[0, 0]
    y22 = total2[0, 1]
    a3 = np.array([[x33, y33, 1]])
    f3 = np.array([[1, 0, dx], [0, 1, -dy], [0, 0, 1]])
    ft3 = f3.T
    total3 = a3.dot(ft3)
    x33 = total3[0, 0]
    y33 = total3[0, 1]

win.getMouse()
win.close()


# --------------------------------------------------------------------------------------------
# ----------------              ІІ. ПЕРЕМІЩЕННЯ + обертання              ----------------

win = GraphWin("2-D проекція в библіотеці graphics ПЕРЕНОС обертання З РУХОМ матрицями", xw, yw)
win.setBackground('white')
dx = 50; dy = 50

# формування трикутника 3 точкам
x1 = st; y1 = yw - st
x2 = st; y2 = yw - st - dy
x3 = st+dx; y3 = yw - st

# -------------------------блок матричних перетворень типу ПЕРЕМІЩЕННЯ----------------------------
a = np.array([[x1, y1, 1]])
f = np.array([[1, 0, dx], [0, 1, -dy], [0, 0, 1]])    # матриця фігури по строках
ft = f.T                                                  # транспонована матриця
total = a.dot(ft)                                       # множення для перетворень 1 точки
x11 = total[0, 0];  y11 = total[0, 1]
a2 = np.array([[x2, y2, 1]])
f2 = np.array([[1, 0, dx], [0, 1, -dy], [0, 0, 1]])
ft2 = f2.T
total2 = a2.dot(ft2)
x22 = total2[0, 0];  y22 = total2[0, 1]                     # множення для перетворень 2 точки
a3 = np.array([[x3, y3, 1]])
f3 = np.array([[1, 0, dx], [0, 1, -dy], [0, 0, 1]])
ft3 = f3.T
total3 = a3.dot(ft3)
x33 = total3[0, 0];  y33 = total3[0, 1]                     # множення для перетворень 3 точки

# -------------------------блок матричних перетворень типу ОБЕРТАННЯ --------------------------
TetaG = 45; TetaR = (3/14*TetaG)/180

ap = np.array([[x11, y11, 1]])
fp = np.array([[mt.cos(TetaR), -mt.sin(TetaR), 0], [mt.sin(TetaR), mt.cos(TetaR), 0], [0, 0, 1]])
ftp = fp.T
totalp = ap.dot(ftp)
x11 = totalp[0, 0];  y11 = totalp[0, 1]

a2p = np.array([[x22, y22, 1]])
fp2 = np.array([[mt.cos(TetaR), -mt.sin(TetaR), 0], [mt.sin(TetaR), mt.cos(TetaR), 0], [0, 0, 1]])
ft2p = fp2.T
total2p = a2p.dot(ft2p)
x22 = total2p[0, 0];  y22 = total2p[0, 1]

a3p = np.array([[x33, y33, 1]])
fp3 = np.array([[mt.cos(TetaR), -mt.sin(TetaR), 0], [mt.sin(TetaR), mt.cos(TetaR), 0], [0, 0, 1]])
ft3p = fp3.T
total3p = a3p.dot(ft3p)
x33 = total3p[0, 0];  y33 = total3p[0, 1]

obj.draw(win)
obj.setOutline("white")
obj = Polygon(Point(x1, y1), Point(x2, y2), Point(x3, y3))

stop = xw/dx*3
stop = float(stop)
ii = int(stop)

obj.draw(win)
obj.setOutline("white")
obj = Polygon(Point(x11, y11), Point(x22, y22), Point(x33, y33))

# ----------------------------- Анімація переміщення та обертання ------------------------------

for i in range(ii):
    time.sleep(0.2)
    # obj.setOutline("white")        # якщо закоментувати, буде траєкторія

    # ---------------------циклічний блок матричних перетворень типу ПЕРЕМІЩЕННЯ------------------
    a = np.array([[x11, y11, 1]])
    f = np.array([[1, 0, dx], [0, 1, -dy], [0, 0, 1]])
    ft = f.T
    total = a.dot(ft)
    x11 = total[0, 0]
    y11 = total[0, 1]

    a2 = np.array([[x22, y22, 1]])
    f2 = np.array([[1, 0, dx], [0, 1, -dy], [0, 0, 1]])
    ft2 = f2.T
    total2 = a2.dot(ft2)
    x22 = total2[0, 0]
    y22 = total2[0, 1]

    a3 = np.array([[x33, y33, 1]])
    f3 = np.array([[1, 0, dx], [0, 1, -dy], [0, 0, 1]])
    ft3 = f3.T
    total3 = a3.dot(ft3)
    x33 = total3[0, 0]
    y33 = total3[0, 1]

# -------------------------------циклічний поворот на TetaR-------------------------------------------

    DTetaR = (3 / 14 * ((xw/dx)*0.65)) / 180
    TetaR = TetaR+DTetaR
    ap = np.array([[x11, y11, 1]])
    fp = np.array([[mt.cos(TetaR), -mt.sin(TetaR), 0], [mt.sin(TetaR), mt.cos(TetaR), 0], [0, 0, 1]])
    ftp = fp.T
    totalp = ap.dot(ftp)
    x11 = totalp[0, 0]
    y11 = totalp[0, 1]

    a2p = np.array([[x22, y22, 1]])
    fp2 = np.array([[mt.cos(TetaR), -mt.sin(TetaR), 0], [mt.sin(TetaR), mt.cos(TetaR), 0], [0, 0, 1]])
    ft2p = fp2.T
    total2p = a2p.dot(ft2p)
    x22 = total2p[0, 0]
    y22 = total2p[0, 1]

    a3p = np.array([[x33, y33, 1]])
    fp3 = np.array([[mt.cos(TetaR), -mt.sin(TetaR), 0], [mt.sin(TetaR), mt.cos(TetaR), 0], [0, 0, 1]])
    ft3p = fp3.T
    total3p = a3p.dot(ft3p)
    x33 = total3p[0, 0]
    y33 = total3p[0, 1]

    obj = Polygon(Point(x11, y11), Point(x22, y22), Point(x33, y33))
    obj.draw(win)

    # -----------------------------------------------------------------------------------------------

win.getMouse()
win.close()

# --------------------------------------------------------------------------------------------
# ----------------              І. ПЕРЕМІЩЕННЯ + масштабування              ----------------

win = GraphWin("2-D проекція в библіотеці graphics ПЕРЕНОС обертання З РУХОМ матрицями", xw, yw)
win.setBackground('white')
dx = 50; dy = 50
sf = 1.1

# формування трикутника 3 точкам
x1 = st; y1 = yw/1.3 - st
x2 = st; y2 = yw/1.3 - st - dy
x3 = st+dx; y3 = yw/1.3 - st

# -------------------------блок матричних перетворень типу ПЕРЕМІЩЕННЯ + МАСШТАБУВАННЯ----------------------------
a = np.array([[x1, y1, 1]])
f = np.array([[sf, 0, dx], [0, sf, -dy], [0, 0, 1]])    # матриця фігури по строках
ft = f.T                                                  # транспонована матриця
total = a.dot(ft)                                       # множення для перетворень 1 точки
x11 = total[0, 0];  y11 = total[0, 1]
a2 = np.array([[x2, y2, 1]])
f2 = np.array([[sf, 0, dx], [0, sf, -dy], [0, 0, 1]])
ft2 = f2.T
total2 = a2.dot(ft2)
x22 = total2[0, 0];  y22 = total2[0, 1]                     # множення для перетворень 2 точки
a3 = np.array([[x3, y3, 1]])
f3 = np.array([[sf, 0, dx], [0, sf, -dy], [0, 0, 1]])
ft3 = f3.T
total3 = a3.dot(ft3)
x33 = total3[0, 0];  y33 = total3[0, 1]                     # множення для перетворень 3 точки

obj.draw(win)
obj.setOutline("white")
obj = Polygon(Point(x1, y1), Point(x2, y2), Point(x3, y3))
obj.draw(win)

stop = xw/dx
stop = float(stop)
ii = int(stop)

# ----------------------------- Анімація переміщення та масштабування ------------------------------

for i in range(ii):
    time.sleep(0.2)

    # obj.setOutline("white")
    obj = Polygon(Point(x11, y11), Point(x22, y22), Point(x33, y33))
    obj.draw(win)
    # ---------------------циклічний блок матричних перетворень типу ПЕРЕМІЩЕННЯ + МАСШТАБУВАННЯ------------------
    a = np.array([[x11, y11, 1]])
    f = np.array([[sf, 0, dx], [0, sf, -dy], [0, 0, 1]])
    ft = f.T
    total = a.dot(ft)
    x11 = total[0, 0]
    y11 = total[0, 1]

    a2 = np.array([[x22, y22, 1]])
    f2 = np.array([[sf, 0, dx], [0, sf, -dy], [0, 0, 1]])
    ft2 = f2.T
    total2 = a2.dot(ft2)
    x22 = total2[0, 0]
    y22 = total2[0, 1]

    a3 = np.array([[x33, y33, 1]])
    f3 = np.array([[sf, 0, dx], [0, sf, -dy], [0, 0, 1]])
    ft3 = f3.T
    total3 = a3.dot(ft3)
    x33 = total3[0, 0]
    y33 = total3[0, 1]

    # -----------------------------------------------------------------------------------------------

win.getMouse()
win.close()
