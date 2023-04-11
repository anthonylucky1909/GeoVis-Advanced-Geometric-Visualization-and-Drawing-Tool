#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 本文件只允许依赖math库
from cgi import print_form
import math


def draw_line(p_list, algorithm):
    """绘制线段

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 线段的起点和终点坐标
    :param algorithm: (string) 绘制使用的算法，包括'DDA'和'Bresenham'，此处的'Naive'仅作为示例，测试时不会出现
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    x0, y0 = p_list[0]
    x1, y1 = p_list[1]
    result = []
    if algorithm == 'Naive':
        if x0 == x1:
            for y in range(y0, y1 + 1):
                result.append((x0, y))
        else:
            if x0 > x1:
                x0, y0, x1, y1 = x1, y1, x0, y0
            k = (y1 - y0) / (x1 - x0)
            for x in range(x0, x1 + 1):
                result.append((x, int(y0 + k * (x - x0))))
    elif algorithm == 'DDA':
        if x0 == x1 and y0 == y1:
            result.append((x1, y1))
        elif abs(y1 - y0) > abs(x1 - x0):
            # if m > 1
            k = (x1 - x0) / (y1 - y0)
            if y1 < y0:
                x0, y0, x1, y1 = x1, y1, x0, y0
            x = x0
            for y in range(y0, y1 + 1):
                result.append((int(x), int(y)))
                x = x + k
        else:
            # if m <= 1
            k = (y1 - y0) / (x1 - x0)
            if x1 < x0:
                x0, y0, x1, y1 = x1, y1, x0, y0
            y = y0
            for x in range(x0, x1 + 1):
                result.append((int(x), int(y)))
                y = y + k

    elif algorithm == 'Bresenham':

        dx = abs(x1-x0)
        dy = abs(y1-y0)
        if dx == dy:
            if x0 > x1:
                x0, y0, x1, y1 = x1, y1, x0, y0
            if y0 < y1:  # positive
                delta_y = 1
            else:
                delta_y = -1
            for x in range(0, dx+1):
                result.append((int(x0 + x), int(y0 + delta_y * x)))
        elif dy == 0:
            # dy = zero mean that y1 and y0 in the same  value coordinate
            x0, x1 = min(x0, x1), max(x0, x1)
            for x in range(x0, x1+1):
                result.append((int(x), int(y1)))
        elif dx == 0:
            # because dx is zero , it means that x1 and x0 in same value coordinate
            y0, y1 = min(y0, y1), max(y0, y1)
            for y in range(y0, y1+1):
                result.append((int(x0), int(y)))
        elif dy < dx:
            dx2, dy2 = 2 * dx, 2 * dy
            if x0 > x1:
                x0, y0, x1, y1 = x1, y1, x0, y0
            if y0 < y1:  # positive
                delta_y = 1
            else:
                delta_y = -1
            y = y0
            p = 2 * dy - dx
            result.append((int(x0), int(y0)))
            for x in range(x0+1, x1+1):
                if p <= 0:
                    p = p + dy2
                else:
                    y = y + delta_y
                    p = p + dy2 - dx2
                result.append((int(x), int(y)))
        else:
            dx2, dy2 = 2 * dx, 2 * dy
            if y0 > y1:
                x0, y0, x1, y1 = x1, y1, x0, y0
            if x0 < x1:  # positive
                delta_x = 1
            else:
                delta_x = -1
            x = x0
            p = 2 * dy - dx
            result.append((int(x0), int(y0)))
            for y in range(y0+1, y1+1):
                if p <= 0:
                    p = p + dx2
                else:
                    x = x + delta_x
                    p = p + dx2 - dy2
                result.append((int(x), int(y)))
    return result


def draw_polygon(p_list, algorithm):
    """绘制多边形

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 多边形的顶点坐标列表
    :param algorithm: (string) 绘制使用的算法，包括'DDA'和'Bresenham'
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    result = []
    for i in range(len(p_list)):
        line = draw_line([p_list[i - 1], p_list[i]], algorithm)
        result += line
    return result


def draw_ellipse(p_list):
    """绘制椭圆（采用中点圆生成算法）

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 椭圆的矩形包围框左上角和右下角顶点坐标
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    result = []
    x1, y1, x2, y2 = p_list[0][0], p_list[0][1], p_list[1][0], p_list[1][1]
    if y1 == y2:  # if y1 and y2 is same , means that we have to draw line
        return draw_line(p_list, "Bresenham")

    cx, cy = (x1 + x2)/2, (y1+y2)/2
    rx, ry = abs(x2-x1)/2, abs(y2-y1)/2
    x, y = 0, ry
    result.append((int(cx+x), int(cy+y)))
    result.append((int(cx-x), int(cy-y)))
    p0 = pow(rx, 2) - (pow(rx, 2) * ry) + (pow(rx, 2)/4)
    # this algorithm we used bresenham logic to draw ellipse, like we draw circle
    while pow(rx, 2) * y > pow(ry, 2)*x:
        result.append((int(cx+x), int(cy+y)))
        result.append((int(cx-x), int(cy+y)))
        result.append((int(cx+x), int(cy-y)))
        result.append((int(cx-x), int(cy-y)))

        if p0 < 0:
            x, y = x+1, y
            p0 = p0 + 2 * ry * ry * x + ry * ry
        else:
            x, y = x + 1, y - 1
            p0 = p0 + 2 * ry * ry * x - 2 * rx * rx * y + ry * ry
    p1 = ry * ry * (x + 1 / 2) * (x + 1 / 2) + rx * rx * \
        (y - 1) * (y - 1) - rx * rx * ry * ry
    while y >= 0:  # when the condtion y >=0
        result.append((int(cx+x), int(cy+y)))
        result.append((int(cx-x), int(cy+y)))
        result.append((int(cx+x), int(cy-y)))
        result.append((int(cx-x), int(cy-y)))
        if p1 > 0:
            x, y = x, y - 1
            p1 = p1 - 2 * rx * rx * y + rx * rx
        else:
            x, y = x + 1, y - 1
            p1 = p1 + 2 * ry * ry * x - 2 * rx * rx * y + rx * rx
    while x <= rx:  # when x <= rx
        result.append((int(cx + x), int(cy)))
        result.append((int(cx - x), int(cy)))
        x = x + 1
    return result


def calculate(element, p_list):
    #we use bspline math formula to calculate 
    array = [-element ** 3 + 3 * element ** 2 - 3 * element + 1, 3 * element ** 3 - 6 *
            element ** 2 + 4, -3 * element ** 3 + 3 * element ** 2 + 3 * element + 1, element ** 3]
    result = 0.0
    for i in range(4):
        result += array[i] * p_list[i]
    return result / 6


def draw_curve(p_list, algorithm):
    """绘制曲线

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 曲线的控制点坐标列表
    :param algorithm: (string) 绘制使用的算法，包括'Bezier'和'B-spline'（三次均匀B样条曲线，曲线不必经过首末控制点）
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    #set delta_u  be 0.001 
    delta_u = 0.001
    result = []
    #use b-spline algorithm to make a curve 
    if algorithm == 'B-spline':
        #set a value a =0
        a = 0
        while a <= 1:
            #calculate use loops
            for i in range(len(p_list) - 3):
                x_listing = [point[0] for point in p_list[i:i + 4]]
                y_listing = [point[1] for point in p_list[i:i + 4]]
                result.append([int(calculate(a, x_listing) + 0.5),
                              int(calculate(a, y_listing) + 0.5)])
            a += delta_u
    #use bezier algorithm to make a curve 
    elif algorithm == 'Bezier':
        length = len(p_list) - 1
        result.append(p_list[0])
        a = delta_u
        #use a loop that a < 1 to iteration
        while a < 1:
            res = p_list.copy()
            for i in range(length):
                tmp = []
                for j in range(len(res) - 1):
                    x0, y0 = res[j]
                    x1, y1 = res[j + 1]
                    tmp.append([(1 - a) * x0 + a * x1, (1 - a) * y0+ a * y1])
                res = tmp.copy()
            x, y = int(res[0][0] + 0.5), int(res[0][1] + 0.5)
            result.append((x, y))
            a += delta_u
        result.append(p_list[-1])
    return result


def translate(p_list, dx, dy):
    """平移变换

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param dx: (int) 水平方向平移量
    :param dy: (int) 垂直方向平移量
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    # To translate a point from coordinate x, y to x1,y1, with distance tx and ty . we just add it.
    result = []
    for (a, b) in p_list:
        a, b = a + dx, b + dy
        result.append((a, b))
    return result


def rotate(p_list, x, y, r):
    """旋转变换（除椭圆外）

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param x: (int) 旋转中心x坐标
    :param y: (int) 旋转中心y坐标
    :param r: (int) 顺时针旋转角度（°）
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    result = []
    #use formula to rotate , use sin and cos function
    for (a, b) in p_list:
        a, b = x + (a - x) * math.cos(r) - (b - y) * math.sin(r), y + \
            (a - x) * math.sin(r) + (b - y) * math.cos(r)
        result.append((int(a), int(b)))
    return result


def scale(p_list, x, y, s):
    """缩放变换

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param x: (int) 缩放中心x坐标
    :param y: (int) 缩放中心y坐标
    :param s: (float) 缩放倍数
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    # scalling to resize size of object
    result = []
    for (a, b) in p_list:
        a, b = x + (a - x) * s, y + (b - y) * s
        result.append((int(a), int(b)))
    return result


def clip(p_list, x_min, y_min, x_max, y_max, algorithm):
    """线段裁剪

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 线段的起点和终点坐标
    :param x_min: 裁剪窗口左上角x坐标
    :param y_min: 裁剪窗口左上角y坐标
    :param x_max: 裁剪窗口右下角x坐标
    :param y_max: 裁剪窗口右下角y坐标
    :param algorithm: (string) 使用的裁剪算法，包括'Cohen-Sutherland'和'Liang-Barsky'
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1]]) 裁剪后线段的起点和终点坐标
    """
    x1, y1 = p_list[0]
    x2, y2 = p_list[1]
    if algorithm == "Liang-Barsky":
        delta_x = x1 - x2
        delta_y = y1-y2
        #calculate array_p and array_q 
        array_p = (-delta_x, delta_x, -delta_y, delta_y)
        array_q = (x2 - x_min, x_max - x2, y2 - y_min, y_max - y2)
        if array_p[0] == 0:
            #if delta_y == 0 , we have to use assert function 
            assert (delta_y != 0)
            if  array_q[1] < 0 or array_q[0] < 0: # outside 
                return []
            else:
                u1, u2 = array_q[2] / array_p[2], array_q[3] / array_p[3]
                u1, u2 = min(u1, u2), max(u1, u2)
                u1, u2 = max(0, u1), min(1, u2)
                if u1 > u2:
                    return []
                return ((int(x2 + u1 * delta_x), int(y2 + u1 * delta_y)), (int(x2 + u2 * delta_x), int(y2 + u2 * delta_y)))
        if array_p[2] == 0:
            if array_q[3] < 0 or array_q[2] < 0:
                return []
            else:
                u1, u2 = array_q[0] / array_p[0], array_q[1] / array_p[1]
                u1, u2 = min(u1, u2), max(u1, u2)
                u1, u2 = max(0, u1), min(1, u2)
                if u1 > u2:
                    return []
                return ((int(x2 + u1 * delta_x), int(y2 + u1 * delta_y)), (int(x2 + u2 * delta_x), int(y2 + u2 * delta_y)))
        u1, u2 = 0, 1
        for k in range(0, 4):
            if array_p[k] < 0:
                u1 = max(array_q[k] / array_p[k], u1)
            elif array_p[k] > 0:
                u2 = min(array_q[k] / array_p[k], u2)
        if u1 > u2:
            return []
        else:
            return ((int(x2 + u1 * delta_x), int(y2 + u1 * delta_y)), (int(x2 + u2 * delta_x), int(y2 + u2 * delta_y)))
    elif algorithm == "Cohen-Sutherland":
        #calculate pos 0 and pos 1
        pos0 = (x1 < x_min) + ((x1 > x_max) << 1) + ((y1 < y_min) << 2) + ((y1 > y_max) << 3)
        pos1 = (x2 < x_min) + ((x2 > x_max) << 1) + ((y2 < y_min) << 2) + ((y2 > y_max) << 3)
        #if condition pos0 and pos1 == 0 then we have to return p_list
        if pos0 == 0 and pos1 == 0:
            return p_list
        elif pos0 & pos1 != 0:
            return ()
        else:
            if pos0 & 2:
                y1 = y1 + (y2 - y1) * (x_max - x1) / (x2 - x1)
                x1 = x_max
            elif pos0 & 1:
                y1 = y1 + (y2 - y1) * (x_min - x1) / (x2 - x1)
                x1 = x_min
            
            
            pos0 = (x1 < x_min) + ((x1 > x_max) << 1) + \
                ((y1 < y_min) << 2) + ((y1 > y_max) << 3)
            
            if pos0 & 4:
                x1 = x1 + (x2 - x1) * (y_min - y1) / (y2 - y1)
                y1 = y_min
            elif pos0 & 8:
                x1 = x1 + (x2 - x1) * (y_max - y1) / (y2 - y1)
                y1 = y_max
            
            pos0 = (x1 < x_min) + ((x1 > x_max) << 1) + \
                ((y1 < y_min) << 2) + ((y1 > y_max) << 3)
            
            if pos0 == 0 and pos1 == 0:
                return ((int(x1), int(y1)), (int(x2), int(y2)))
            elif pos0 & pos1 != 0:
                return ()
            
            if pos1 & 2:
                y2 = y1 + (y2 - y1) * (x_max - x1) / (x2 - x1)
                x2 = x_max
            elif pos1 & 1:
                y2 = y1 + (y1 - y1) * (x_min - x1) / (x2 - x1)
                x2 = x_min
            
            pos1 = (x2 < x_min) + ((x2 > x_max) << 1) + \
                ((y2 < y_min) << 2) + ((y2 > y_max) << 3)
            
            if pos1 & 4:
                x2 = x1+ (x2 - x1) * (y_min - y1) / (y2 - y1)
                y2 = y_min
            elif pos1 & 8:
                x2 = x1 + (x2 - x1) * (y_max - y1) / (y2 - y1)
                y2 = y_max
            return ((int(x1), int(y1)), (int(x2), int(y2)))
