from graphics import *
import numpy as np
import math as mt
import matplotlib.pyplot as plt


#  --------------------------------- функція проєкції на xy, z=0 -------------------------------------
def ProjectXY(Figure):
    f = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 1]])  # по строках
    ft = f.T
    Prxy = Figure.dot(ft)
    print('Проєкція на ху')
    print(Prxy)

    return Prxy


#  -------------------------------------------- зміщення ----------------------------------------------
def ShiftXYZ(Figure, l, m, n):
    f = np.array([[1, 0, 0, l], [0, 1, 0, m], [0, 0, 1, n], [1, 0, 0, 1]])  # по строках
    ft = f.T
    Prxy = Figure.dot(ft)
    print('Зміщення')
    print(Prxy)

    return Prxy


# -------------------------------------------- аксонометрія ----------------------------------------------
def dimetri(Figure, TetaG1, TetaG2):
    TetaR1 = (3 / 14 * TetaG1) / 180
    TetaR2 = (3 / 14 * TetaG2) / 180
    f1 = np.array(
        [[mt.cos(TetaR1), 0, -mt.sin(TetaR1), 0], [0, 1, 0, 0], [mt.sin(TetaR1), 0, mt.cos(TetaR1), 1], [0, 0, 0, 0], ])
    ft1 = f1.T
    Prxy1 = Figure.dot(ft1)
    f2 = np.array(
        [[1, 0, 0, 0], [0, mt.cos(TetaR2), mt.sin(TetaR2), 0], [0, -mt.sin(TetaR2), mt.cos(TetaR2), 0], [0, 0, 0, 1]])
    ft2 = f2.T
    Prxy2 = Prxy1.dot(ft2)
    print('Діметрична проєкція')
    print(Prxy2)

    return Prxy2


def LagrangeInter(Prxy):
    Ax = Prxy[0, 0]; Ay = Prxy[0, 1]
    Bx = Prxy[1, 0]; By = Prxy[1, 1]
    Ix = Prxy[2, 0]; Iy = Prxy[2, 1]
    Mx = Prxy[3, 0]; My = Prxy[3, 1]

    Dx = Prxy[4, 0]; Dy = Prxy[4, 1]
    Cx = Prxy[5, 0]; Cy = Prxy[5, 1]
    Fx = Prxy[6, 0]; Fy = Prxy[6, 1]
    Ex = Prxy[7, 0]; Ey = Prxy[7, 1]

    # List of coordinate pairs
    coordinate_list = [[[Ax, Bx], [Ay, By]],
                       [[Bx, Cx], [By, Cy]],
                       [[Cx, Dx], [Cy, Dy]],
                       [[Dx, Ax], [Dy, Ay]],
                       [[Ax + 1, Mx], [Ay, My]],
                       [[Bx + 1, Ix], [By, Iy]],
                       [[Cx + 1, Fx], [Cy, Fy]],
                       [[Dx + 1, Ex], [Dy, Ey]],
                       [[Mx, Ix], [My, Iy]],
                       [[Ix, Fx], [Iy, Fy]],
                       [[Fx, Ex], [Fy, Ey]],
                       [[Ex, Mx], [Ey, My]]]

    # Loop over each coordinate pair
    for coordinates in coordinate_list:
        x = np.array(coordinates[0], float)
        y = np.array(coordinates[1], float)

        xplt = np.linspace(x[0], x[-1], 100)
        yplt = np.array([], float)

        for xp in xplt:
            yp = 0

            for xi, yi in zip(x, y):
                yp += yi * np.prod((xp - x[x != xi]) / (xi - x[x != xi]))
            yplt = np.append(yplt, yp)

        plt.plot(x, y, 'ro', xplt, yplt, 'b-')

    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()


# ------------------------- алгоритм Брезенхема для растрофікації ліній ----------------------------------
def draw_line_pixel(x1, y1, x2, y2):

    dx = x2 - x1; dy = y2 - y1
    sign_x = 1 if dx > 0 else -1 if dx < 0 else 0
    sign_y = 1 if dy > 0 else -1 if dy < 0 else 0
    if dx < 0:
        dx = -dx
    if dy < 0:
        dy = -dy
    if dx > dy:
        pdx, pdy = sign_x, 0
        es, el = dy, dx
    else:
        pdx, pdy = 0, sign_y
        es, el = dx, dy
    x, y = x1, y1
    error, t = el / 2, 0

    obj = Point(x, y)
    obj.setFill('blue')
    obj.draw(win)

    while t < el:
        error -= es
        if error < 0:
            error += el
            x += sign_x
            y += sign_y
        else:
            x += pdx
            y += pdy
        t += 1
        obj = Point(x, y)
        obj.setFill('blue')
        obj.draw(win)

    return draw_line_pixel


# ------------------- функція побудови растрового паралелепіпеда -----------------------
def PrlpdWiz_Pixel(Prxy3):
    # ----------- дальня грань - (в проекції ліва) -------------------------------------
    Ax1 = Prxy3[0, 0]
    Ay1 = Prxy3[0, 1]
    Bx1 = Prxy3[1, 0]
    By1 = Prxy3[1, 1]
    Ix1 = Prxy3[2, 0]
    Iy1 = Prxy3[2, 1]
    Mx1 = Prxy3[3, 0]
    My1 = Prxy3[3, 1]
    # ----------- ближня грань - (в проекції права) -------------------------------------
    Dx1 = Prxy3[4, 0]
    Dy1 = Prxy3[4, 1]
    Cx1 = Prxy3[5, 0]
    Cy1 = Prxy3[5, 1]
    Fx1 = Prxy3[6, 0]
    Fy1 = Prxy3[6, 1]
    Ex1 = Prxy3[7, 0]
    Ey1 = Prxy3[7, 1]

    # ----------- дальня грань - (в проекції ліва) -------------------------------------
    draw_line_pixel(Ax1, Ay1, Bx1, By1)
    draw_line_pixel(Bx1, By1, Ix1, Iy1)
    draw_line_pixel(Ix1, Iy1, Mx1, My1)
    draw_line_pixel(Mx1, My1, Ax1, Ay1)
    # ----------- ближча грань - (в проекції права) -------------------------------------
    draw_line_pixel(Dx1, Dy1, Cx1, Cy1)
    draw_line_pixel(Cx1, Cy1, Fx1, Fy1)
    draw_line_pixel(Fx1, Fy1, Ex1, Ey1)
    draw_line_pixel(Ex1, Ey1, Dx1, Dy1)
    # ----------- верхеня грань - (в проекції верхня) -------------------------------------
    draw_line_pixel(Ax1, Ay1, Bx1, By1)
    draw_line_pixel(Bx1, By1, Cx1, Cy1)
    draw_line_pixel(Cx1, Cy1, Dx1, Dy1)
    draw_line_pixel(Dx1, Dy1, Ax1, Ay1)
    # ----------- верхеня грань - (в проекції верхня) -------------------------------------
    draw_line_pixel(Mx1, My1, Ix1, Iy1)
    draw_line_pixel(Ix1, Iy1, Fx1, Fy1)
    draw_line_pixel(Fx1, Fy1, Ex1, Ey1)
    draw_line_pixel(Ex1, Ey1, Mx1, My1)
    # ----------- ліва грань - (в проекції ближня) ----------------------------------------
    draw_line_pixel(Ax1, Ay1, Mx1, My1)
    draw_line_pixel(Mx1, My1, Ex1, Ey1)
    draw_line_pixel(Ex1, Ey1, Dx1, Dy1)
    draw_line_pixel(Dx1, Dy1, Ax1, Ay1)
    # ----------- права грань - (в проекції дальня) ----------------------------------------
    draw_line_pixel(Bx1, By1, Ix1, Iy1)
    draw_line_pixel(Ix1, Iy1, Fx1, Fy1)
    draw_line_pixel(Fx1, Fy1, Cx1, Cy1)
    draw_line_pixel(Cx1, Cy1, Bx1, By1)
    return PrlpdWiz_Pixel


# --------- функція побудови векторного паралелепіпеда з видаленням невидимих граней ------------
def PrlpdWizReal_G(PrxyDIM, Prxy, Xmax, Ymax, Zmax):
    # ----------- Алгоритм плаваючого обрію --------------------------------------
    # ----------- аксонометрична матриця без проекції -------------------------------

    AAx = PrxyDIM[0, 0]; AAy = PrxyDIM[0, 1]; AAz = PrxyDIM[0, 2]
    BBx = PrxyDIM[1, 0]; BBy = PrxyDIM[1, 1]; BBz = PrxyDIM[1, 2]
    IIx = PrxyDIM[2, 0]; IIy = PrxyDIM[2, 1]; IIz = PrxyDIM[2, 2]
    MMx = PrxyDIM[3, 0]; MMy = PrxyDIM[3, 1]; MMz = PrxyDIM[3, 2]

    DDx = PrxyDIM[4, 0]; DDy = PrxyDIM[4, 1]; DDz = PrxyDIM[4, 2]
    CCx = PrxyDIM[5, 0]; CCy = PrxyDIM[5, 1]; CCz = PrxyDIM[5, 2]
    FFx = PrxyDIM[6, 0]; FFy = PrxyDIM[6, 1]; FFz = PrxyDIM[6, 2]
    EEx = PrxyDIM[7, 0]; EEy = PrxyDIM[7, 1]; EEz = PrxyDIM[7, 2]

    # -------------------------------------F-T--------------------------------------
    if (abs(AAz - Zmax) > abs(DDz - Zmax)) and (abs(BBz - Zmax) > abs(CCz - Zmax)) \
            and (abs(IIz - Zmax) > abs(FFz - Zmax)) and (abs(MMz - Zmax) > abs(EEz - Zmax)):
        FlagF = 1
    else:
        FlagF = 2
    print('FlagF=', FlagF)
    # -------------------------------------L-R--------------------------------------
    if (abs(DDx - Xmax) > abs(CCx - Xmax)) and (abs(AAx - Xmax) > abs(BBx - Xmax)) \
            and (abs(MMx - Xmax) > abs(IIx - Xmax)) and (abs(EEx - Xmax) > abs(FFx - Xmax)):
        FlagR = 1
    else:
        FlagR = 2
    print('FlagR=', FlagR)
    # -------------------------------------P-D--------------------------------------
    if (abs(AAy - Ymax) > abs(MMy - Ymax)) and (abs(BBy - Ymax) > abs(IIy - Ymax)) \
            and (abs(CCy - Ymax) > abs(FFy - Ymax)) and (abs(DDy - Ymax) > abs(EEy - Ymax)):
        FlagP = 1
    else:
        FlagP = 2
    print('FlagP=', FlagP)
    # -------------------------------------------------------------------------------
    Ax = Prxy[0, 0]; Ay = Prxy[0, 1]
    Bx = Prxy[1, 0]; By = Prxy[1, 1]
    Ix = Prxy[2, 0]; Iy = Prxy[2, 1]
    Mx = Prxy[3, 0]; My = Prxy[3, 1]

    Dx = Prxy[4, 0]; Dy = Prxy[4, 1]
    Cx = Prxy[5, 0]; Cy = Prxy[5, 1]
    Fx = Prxy[6, 0]; Fy = Prxy[6, 1]
    Ex = Prxy[7, 0]; Ey = Prxy[7, 1]

    # ----------- Ліва грань ----------------------------------------------------
    obj = Polygon(Point(Ax, Ay), Point(Mx, My), Point(Ex, Ey), Point(Dx, Dy))
    if FlagR == 2:
        obj.setFill('indigo')
        obj.draw(win)
    # ----------- Права грань ----------------------------------------------------
    obj = Polygon(Point(Bx, By), Point(Ix, Iy), Point(Fx, Fy), Point(Cx, Cy))
    if FlagR == 1:
        obj.setFill('indigo')
        obj.draw(win)
    # ----------- Верхня грань ----------------------------------------------------
    obj = Polygon(Point(Ax, Ay), Point(Bx, By), Point(Cx, Cy), Point(Dx, Dy))
    if FlagP == 1:
        obj.setFill('violet')
        obj.draw(win)
    # ----------- Нижня грань ----------------------------------------------------
    obj = Polygon(Point(Mx, My), Point(Ix, Iy), Point(Fx, Fy), Point(Ex, Ey))
    if FlagP == 2:
        obj.setFill('orange')
        obj.draw(win)
    # ----------- Тильна грань ----------------------------------------------------
    obj = Polygon(Point(Ax, Ay), Point(Bx, By), Point(Ix, Iy), Point(Mx, My))
    if FlagF == 2:
        obj.setFill('blue')
        obj.draw(win)
    # ----------- Фронтальна грань ------------------------------------------------
    obj = Polygon(Point(Dx, Dy), Point(Cx, Cy), Point(Fx, Fy), Point(Ex, Ey))
    if FlagF == 1:
        obj.setFill('green')
        obj.draw(win)

    return PrlpdWizReal_G


# ----------------------------------------- головні виклики --------------------------------

if __name__ == '__main__':
    # ---------------------------------- координати паралелепіпеда ------------------------------------
    xw = 600
    yw = 600
    st = 300
    # розташування координат у строках: дальній чотирикутник - A B I M,  ближній чотирикутник D C F E
    Prlpd = np.array([[0, 0, 0, 1],
                      [st, 0, 0, 1],
                      [st, st, 0, 1],
                      [0, st, 0, 1],
                      [0, 0, st, 1],
                      [st, 0, st, 1],
                      [st, st, st, 1],
                      [0, st, st, 1]])  # по строках
    print('Вхідна матриця')
    print(Prlpd)

    # ----------------------------------- початкові параметри ------------------------------
    st = 45
    TetaG1 = 210
    TetaG2 = 120
    l = (xw / 2) - st
    m = (yw / 2) - st - 200
    n = m + 200

    # ---------------------------- растеризація -----------------
    win = GraphWin("3-D растровий паралелепіпед, аксонометрична проєкція на ХУ", xw, yw)
    win.setBackground('white')
    Prlpd1 = ShiftXYZ(Prlpd, l, m, n)
    Prlpd2 = dimetri(Prlpd1, TetaG1, TetaG2)
    Prxy3 = ProjectXY(Prlpd2)
    PrlpdWiz_Pixel(Prxy3)  # растеризація
    win.getMouse()
    win.close()

    # --------- інтерполяція методом Лагранжа ---------
    LagrangeInter(Prxy3)

    # --------- векторизація з видаленням невидимих граней ---------
    win = GraphWin("3-D векторний КОЛЬОРОВИЙ паралелепіпед з видаленням невидимих граней", xw, yw)
    win.setBackground('white')
    l = (xw / 2) - st; m = (yw / 2) - st; n = m
    Prlpd1 = ShiftXYZ(Prlpd, l, m - 200, n)
    Prlpd2 = dimetri(Prlpd1, TetaG1, TetaG2)
    Prxy3 = ProjectXY(Prlpd2)
    PrlpdWizReal_G(Prlpd2, Prxy3, (xw * 2), (yw * 2), (yw * 2))
    win.getMouse()
    win.close()
