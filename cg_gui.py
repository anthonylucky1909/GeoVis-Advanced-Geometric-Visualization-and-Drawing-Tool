#!/usr/bin/env python
# -*- coding:utf-8 -*-
import math
import pickle
import sys
from typing import Optional

import cg_algorithms as alg
import PyQt5
from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QColor, QMouseEvent, QPainter
from PyQt5.QtWidgets import (QApplication, QColorDialog, QFileDialog,
                             QGraphicsItem, QGraphicsScene, QGraphicsView,
                             QHBoxLayout, QInputDialog, QListWidget,
                             QMainWindow, QMessageBox,
                             QStyleOptionGraphicsItem, QWidget, qApp, QGraphicsRectItem)


class MyCanvas(QGraphicsView):
    """
    画布窗体类，继承自QGraphicsView，采用QGraphicsView、QGraphicsScene、QGraphicsItem的绘图框架
    """

    def __init__(self, *args):
        super().__init__(*args)
        self.main_window = None
        self.list_widget = None
        self.item_dict = {}
        self.selected_id = ''

        self.status = ''
        self.temp_algorithm = ''
        self.temp_id = ''
        self.pen_color = QColor(0, 0, 0)
        self.temp_item = None
        self.center_point = None
        self.origin_coordinate = None
        self.origin_array = None
        self.border = None

    def start_draw_line(self, algorithm, item_id):
        self.status = 'line'
        self.temp_algorithm = algorithm
        self.temp_id = item_id
        self.temp_item = None

    def start_draw_ellipse(self, algorithm, item_id):
        self.status = 'ellipse'
        self.temp_algorithm = algorithm
        self.temp_id = item_id
        self.temp_item = None

    def start_draw_polygon(self, algorithm, item_id):
        self.status = 'polygon'
        self.temp_algorithm = algorithm
        self.temp_id = item_id
        self.temp_item = None

    def start_translate(self):
        self.status = 'translate'
        self.temp_item = None
        self.origin_coordinate = None
        self.origin_array = None

    def start_clip(self, algorithm):
        self.status = 'clip'
        self.temp_algorithm = algorithm
        self.temp_item = None
        self.origin_coordinate = None
        self.origin_array = None

    def start_rotate(self):
        self.status = 'rotate'
        self.temp_item = None
        self.origin_array = None
        self.center_point = None

    def start_scale(self):
        self.status = 'scale'
        self.temp_item = None
        self.origin_array = None
        self.center_point = None

    def start_draw_curve(self, algorithm, item_id):
        self.status = 'curve'
        self.temp_algorithm = algorithm
        self.temp_id = item_id
        self.temp_item = None

    def finish_draw(self):
        self.temp_id = self.main_window.get_id()

    def clear_selection(self):
        if self.selected_id != '':
            self.item_dict[self.selected_id].selected = False
            self.selected_id = ''

    def selection_changed(self, selected):
        if self.status == 'polygon' or self.status == 'curve':
            self.finish_draw()
        self.center_point = None
        if self.selected_id != '':
            self.item_dict[self.selected_id].selected = False
            self.item_dict[self.selected_id].update()
        if selected != '':
            self.main_window.statusBar().showMessage('图元选择： %s' % selected)
            self.selected_id = selected
            self.item_dict[selected].selected = True
            self.item_dict[selected].update()
            self.status = ''
            self.updateScene([self.sceneRect()])

    def mousePressEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.localPos().toPoint())
        x = int(pos.x())
        y = int(pos.y())
        if self.status == 'line':
            self.temp_item = MyItem(self.temp_id, self.status, [
                                    [x, y], [x, y]], self.temp_algorithm, self.pen_color)
            self.scene().addItem(self.temp_item)
        elif self.status == 'polygon' or self.status == 'curve':
            if self.temp_item is None:
                self.temp_item = MyItem(self.temp_id, self.status, [
                                        [x, y]], self.temp_algorithm, self.pen_color)
                self.scene().addItem(self.temp_item)
            else:
                self.temp_item.p_list.append([x, y])
        elif self.status == 'ellipse':
            self.temp_item = MyItem(self.temp_id, self.status, [
                                    [x, y], [x, y]], self.temp_algorithm, self.pen_color)
            self.scene().addItem(self.temp_item)
        elif self.status == 'translate':
            if (self.selected_id != ''):
                self.temp_item = self.item_dict[self.selected_id]
                self.origin_coordinate = pos
                self.origin_array = self.temp_item.p_list
        elif self.status == 'rotate':
            if (self.selected_id != ''):
                self.temp_item = self.item_dict[self.selected_id]
                self.origin_array = self.temp_item.p_list
                if self.center_point == None:
                    self.center_point = pos
                else:
                    self.origin_coordinate = pos
        elif self.status == 'scale':
            if (self.selected_id != ''):
                self.temp_item = self.item_dict[self.selected_id]
                self.origin_array = self.temp_item.p_list
                if self.center_point == None:
                    self.center_point = pos
                else:
                    self.origin_coordinate = pos
        elif self.status == 'clip':
            if self.selected_id != '':
                self.temp_item = self.item_dict[self.selected_id]
                if self.temp_item.item_type == 'line':
                    self.origin_coordinate = pos
                    self.origin_array = self.temp_item.p_list
        self.updateScene([self.sceneRect()])
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.localPos().toPoint())
        x = int(pos.x())
        y = int(pos.y())
        if self.status == 'line':
            self.temp_item.p_list[1] = [x, y]
        elif self.status == 'polygon':
            self.temp_item.p_list[-1] = [x, y]
        elif self.status == 'ellipse':
            self.temp_item.p_list[1] = [x, y]
        elif self.status == 'curve':
            self.temp_item.p_list[-1] = [x, y]
        elif self.status == 'translate':
            if self.selected_id != '':
                dx = x - int(self.origin_coordinate.x())
                dy = y - int(self.origin_coordinate.y())
                self.temp_item.p_list = alg.translate(
                    self.origin_array, dx, dy)
        elif self.status == 'rotate':
            if self.selected_id != '' and self.center_point != None and self.origin_coordinate != None:
                x_center = int(self.origin_coordinate.x() -
                               self.center_point.x())
                y_center = int(self.origin_coordinate.y() -
                               self.center_point.y())
                length_center_coordinate = math.sqrt(
                    x_center ** 2 + y_center ** 2)
                x_current = x - int(self.center_point.x())
                y_current = y - int(self.center_point.y())
                length_current = math.sqrt(x_current ** 2 + y_current ** 2)
                if length_center_coordinate != 0 and length_current != 0:
                    # find value of r
                    value_center_x = x_center / length_center_coordinate
                    value_center_y = y_center / length_center_coordinate

                    value_current_x = x_current / length_current
                    value_current_y = y_current / length_current
                    # base on formula
                    delta_sin = value_current_y * value_center_x - value_current_x * value_center_y
                    delta_cos = value_current_x * value_center_x + value_current_y * value_center_y
                    if delta_cos >= 0:
                        r = math.asin(delta_sin)
                    else:
                        r = math.pi - math.asin(delta_sin)
                    self.temp_item.p_list = alg.rotate(self.origin_array, int(
                        self.center_point.x()), int(self.center_point.y()), r)
        elif self.status == 'scale':
            if self.selected_id != '' and self.center_point != None and self.origin_coordinate != None:
                prev_x = int(self.origin_coordinate.x() -
                             self.center_point.x())
                prev_y = int(self.origin_coordinate.y() -
                             self.center_point.y())
                length = math.sqrt(prev_x ** 2 + prev_y ** 2)
                if length != 0:
                    current_x = x - int(self.center_point.x())
                    current_y = y - int(self.center_point.y())
                    current_length = math.sqrt(current_x ** 2 + current_y ** 2)
                    self.temp_item.p_list = alg.scale(self.origin_array, int(
                        self.center_point.x()), int(self.center_point.y()), current_length / length)

        elif self.status == 'clip':
            if self.selected_id != '' and self.origin_coordinate != None and self.temp_item.item_type == 'line':
                x_min,x_max = min(int(self.origin_coordinate.x()), x),max(int(self.origin_coordinate.x()), x)
                y_min,y_max = min(int(self.origin_coordinate.y()), y),max(int(self.origin_coordinate.y()), y)
                if self.border == None:
                    self.border = QGraphicsRectItem(x_min - 1, y_min - 1, x_max - x_min + 2, y_max - y_min + 2)
                    self.scene().addItem(self.border)
                    self.border.setPen(QColor(0, 255, 255))
                else:
                    self.border.setRect(x_min - 1, y_min - 1, x_max - x_min + 2, y_max - y_min + 2)
        self.updateScene([self.sceneRect()])
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if self.status == 'line':
            self.item_dict[self.temp_id] = self.temp_item
            self.list_widget.addItem(self.temp_id)
            self.finish_draw()
        elif self.status == 'polygon':
            self.item_dict[self.temp_id] = self.temp_item
            if not self.list_widget.findItems(self.temp_id, Qt.MatchContains):
                self.list_widget.addItem(self.temp_id)
        elif self.status == 'ellipse':
            self.item_dict[self.temp_id] = self.temp_item
            self.list_widget.addItem(self.temp_id)
            self.finish_draw()
        elif self.status == 'curve':
            self.item_dict[self.temp_id] = self.temp_item
            if not self.list_widget.findItems(self.temp_id, Qt.MatchContains):
                self.list_widget.addItem(self.temp_id)
        elif self.status == 'clip':
            posisition = self.mapToScene(event.localPos().toPoint())
            x,y = int(posisition.x()),int(posisition.y())
            if self.origin_coordinate != None and self.temp_item.item_type == 'line' and self.selected_id != '':
                x_minimum,x_maximum = min(int(self.origin_coordinate.x()), x),max(int(self.origin_coordinate.x()), x)
                y_minimum,y_maximum = min(int(self.origin_coordinate.y()), y),max(int(self.origin_coordinate.y()), y)
                temp_p_list = alg.clip(self.origin_array, x_minimum, y_minimum, x_maximum, y_maximum, self.temp_algorithm)
                if len(temp_p_list) == 0:
                    nums = self.list_widget.findItems(
                        self.selected_id, Qt.MatchContains)
                    row = self.list_widget.row(nums[0])
                    temp_id = self.selected_id
                    self.clear_selection()
                    self.list_widget.clearSelection()
                    self.scene().removeItem(self.temp_item)
                    self.temp_item = None
                    del self.item_dict[temp_id]
                    self.list_widget.takeItem(row)
                else:
                    self.temp_item.p_list = temp_p_list
            if self.border != None:
                self.scene().removeItem(self.border)
                self.border = None
            self.updateScene([self.sceneRect()])
        super().mouseReleaseEvent(event)


class MyItem(QGraphicsItem):
    """
    自定义图元类，继承自QGraphicsItem
    """

    def __init__(self, item_id: str, item_type: str, p_list: list, algorithm: str = '', color=QColor(0, 0, 0), parent: QGraphicsItem = None,):
        """

        :param item_id: 图元ID
        :param item_type: 图元类型，'line'、'polygon'、'ellipse'、'curve'等
        :param p_list: 图元参数
        :param algorithm: 绘制算法，'DDA'、'Bresenham'、'Bezier'、'B-spline'等
        :param parent:
        """
        super().__init__(parent)
        self.id = item_id           # 图元ID
        self.item_type = item_type  # 图元类型，'line'、'polygon'、'ellipse'、'curve'等
        self.p_list = p_list        # 图元参数
        self.algorithm = algorithm  # 绘制算法，'DDA'、'Bresenham'、'Bezier'、'B-spline'等
        self.selected = False
        self.color = color

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: Optional[QWidget] = ...) -> None:
        if self.item_type == 'line':
            item_pixels = alg.draw_line(self.p_list, self.algorithm)
            painter.setPen(self.color)
            for p in item_pixels:
                painter.drawPoint(*p)
            if self.selected:
                painter.setPen(QColor(255, 0, 0))
                painter.drawRect(self.boundingRect())
        elif self.item_type == 'polygon':
            item_pixels = alg.draw_polygon(self.p_list, self.algorithm)
            painter.setPen(self.color)
            for p in item_pixels:
                painter.drawPoint(*p)
            if self.selected:
                painter.setPen(QColor(255, 0, 0))
                painter.drawRect(self.boundingRect())
        elif self.item_type == 'ellipse':
            item_pixels = alg.draw_ellipse(self.p_list)
            painter.setPen(self.color)
            for p in item_pixels:
                painter.drawPoint(*p)
            if self.selected:
                painter.setPen(QColor(255, 0, 0))
                painter.drawRect(self.boundingRect())
        elif self.item_type == 'curve':
            item_pixels = alg.draw_curve(self.p_list, self.algorithm)
            array = alg.draw_polygon(self.p_list, 'DDA')
            painter.setPen(self.color)
            for p in item_pixels:
                painter.drawPoint(*p)
            painter.setPen(QColor(0, 80, 80))
            for p in array:
                painter.drawPoint(*p)
            if self.selected:
                painter.setPen(QColor(255, 0, 0))
                painter.drawRect(self.boundingRect())

    def boundingRect(self) -> QRectF:
        if self.item_type == 'line':
            print("line")
            x0, y0 = self.p_list[0]
            x1, y1 = self.p_list[1]
            x,y = min(x0, x1),min(y0, y1)
            width = max(x0, x1) - x
            height = max(y0, y1) - y
            return QRectF(x - 1, y - 1, width + 2, height + 2)
        elif self.item_type == 'polygon':
            print("polygon")
            x_min, y_min = self.p_list[0]
            x_max, y_max = self.p_list[0]
            for point in self.p_list:
                if point[0] < x_min:
                    x_min = point[0]
                if point[1] < y_min:
                    y_min = point[1]
                if point[0] > x_max:
                    x_max = point[0]
                if point[1] > y_max:
                    y_max = point[1]
            width = x_max - x_min
            height= y_max - y_min
            return QRectF(x_min - 1, y_min - 1, width + 2, height + 2)
        elif self.item_type == 'ellipse':
            print("ellipse")
            x0, y0 = self.p_list[0]
            x1, y1 = self.p_list[1]
            x = min(x0, x1)
            y = min(y0, y1)
            width = max(x0, x1) - x
            height = max(y0, y1) - y
            return QRectF(x - 1, y - 1, width + 2, height + 2)
        elif self.item_type == 'curve':
            x_min, y_min = self.p_list[0]
            x_max, y_max = self.p_list[0]
            for point in self.p_list:
                if point[0] < x_min:
                    x_min = point[0]
                if point[1] < y_min:
                    y_min = point[1]
                if point[0] > x_max:
                    x_max = point[0]
                if point[1] > y_max:
                    y_max = point[1]
            width = x_max - x_min
            height = y_max - y_min
            return QRectF(x_min - 1, y_min - 1, width + 2, height + 2)


class MainWindow(QMainWindow):
    """
    主窗口类
    """

    def __init__(self):
        super().__init__()
        self.item_cnt = 0
        self.path = ''

        # 使用QListWidget来记录已有的图元，并用于选择图元。注：这是图元选择的简单实现方法，更好的实现是在画布中直接用鼠标选择图元
        self.list_widget = QListWidget(self)
        self.list_widget.setMinimumWidth(200)

        # 使用QGraphicsView作为画布
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, 600, 600)
        self.canvas_widget = MyCanvas(self.scene, self)
        self.canvas_widget.setFixedSize(600, 600)
        self.canvas_widget.main_window = self
        self.canvas_widget.list_widget = self.list_widget

        # 设置菜单栏
        print("MainWindow")
        menubar = self.menuBar()
        file_menu = menubar.addMenu('文件')
        set_pen_act = file_menu.addAction('设置画笔')
        reset_canvas_act = file_menu.addAction('重置画布')
        save_canvas = file_menu.addAction('保存画布')
        exit_act = file_menu.addAction('退出')
        draw_menu = menubar.addMenu('绘制')
        line_menu = draw_menu.addMenu('线段')
        line_naive_act = line_menu.addAction('Naive')
        line_dda_act = line_menu.addAction('DDA')
        line_bresenham_act = line_menu.addAction('Bresenham')
        polygon_menu = draw_menu.addMenu('多边形')
        polygon_dda_act = polygon_menu.addAction('DDA')
        polygon_bresenham_act = polygon_menu.addAction('Bresenham')
        ellipse_act = draw_menu.addAction('椭圆')
        curve_menu = draw_menu.addMenu('曲线')
        curve_bezier_act = curve_menu.addAction('Bezier')
        curve_b_spline_act = curve_menu.addAction('B-spline')
        edit_menu = menubar.addMenu('编辑')
        translate_act = edit_menu.addAction('平移')
        rotate_act = edit_menu.addAction('旋转')
        scale_act = edit_menu.addAction('缩放')
        clip_menu = edit_menu.addMenu('裁剪')
        clip_cohen_sutherland_act = clip_menu.addAction('Cohen-Sutherland')
        clip_liang_barsky_act = clip_menu.addAction('Liang-Barsky')

        # 连接信号和槽函数
        exit_act.triggered.connect(self.quit_action)
        line_naive_act.triggered.connect(self.line_naive_action)
        line_dda_act.triggered.connect(self.line_dda_action)
        line_bresenham_act.triggered.connect(self.line_bresenham_action)
        polygon_dda_act.triggered.connect(self.polygon_dda_action)
        polygon_bresenham_act.triggered.connect(self.polygon_bresenham_action)
        ellipse_act.triggered.connect(self.ellipse_action)
        curve_bezier_act.triggered.connect(self.curve_bezier_action)
        curve_b_spline_act.triggered.connect(self.curve_b_spline_action)
        translate_act.triggered.connect(self.translate_action)
        rotate_act.triggered.connect(self.rotate_action)
        scale_act.triggered.connect(self.scale_action)
        clip_cohen_sutherland_act.triggered.connect(
            self.clip_cohen_sutherland_action)
        clip_liang_barsky_act.triggered.connect(self.clip_liang_barsky_action)
        reset_canvas_act.triggered.connect(self.reset_canvas_action)
        save_canvas.triggered.connect(self.save_canvas_action)
        set_pen_act.triggered.connect(self.set_pen_action)
        self.list_widget.currentTextChanged.connect(
            self.canvas_widget.selection_changed)

        # 设置主窗口的布局
        self.hbox_layout = QHBoxLayout()
        self.hbox_layout.addWidget(self.canvas_widget)
        self.hbox_layout.addWidget(self.list_widget, stretch=1)
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.hbox_layout)
        self.setCentralWidget(self.central_widget)
        self.statusBar().showMessage('空闲')
        self.resize(600, 600)
        self.setWindowTitle('CG Demo')

    def get_id(self):
        _id = str(self.item_cnt)
        self.item_cnt += 1
        return _id

    def line_naive_action(self):
        self.canvas_widget.start_draw_line('Naive', self.get_id())
        self.statusBar().showMessage('Naive算法绘制线段')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def line_dda_action(self):
        self.canvas_widget.start_draw_line('DDA', self.get_id())
        self.statusBar().showMessage('DDA算法绘制线段')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def line_bresenham_action(self):
        self.canvas_widget.start_draw_line('Bresenham', self.get_id())
        self.statusBar().showMessage('Bresenham算法绘制线段')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def polygon_dda_action(self):
        print("polygon_dda_action")
        self.canvas_widget.start_draw_polygon('DDA', self.get_id())
        self.statusBar().showMessage('DDA算法绘制多边形')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def polygon_bresenham_action(self):
        print("polygon_bresenham_action")
        self.canvas_widget.start_draw_polygon('Bresenham', self.get_id())
        self.statusBar().showMessage('Bresenham算法绘制多边形')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def ellipse_action(self):
        self.canvas_widget.start_draw_ellipse('center', self.get_id())
        self.statusBar().showMessage('绘制椭圆（采用中点圆生成算法）')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def translate_action(self):
        self.canvas_widget.start_translate()
        self.statusBar().showMessage('平移')

    def rotate_action(self):
        self.canvas_widget.start_rotate()
        self.statusBar().showMessage('旋转变换')

    def scale_action(self):
        self.canvas_widget.start_scale()
        self.statusBar().showMessage('缩放变换')

    def reset_canvas_action(self):
        length = QInputDialog.getInt(self, '请输入', 'Length', 100, 100, 1000)[0]
        width = QInputDialog.getInt(self, '请输入', 'Width', 100, 100, 1000)[0]
        self.list_widget.clearSelection()
        self.list_widget.clear()
        self.canvas_widget.clear_selection()
        self.canvas_widget.item_dict.clear()
        self.canvas_widget.scene().clear()
        self.scene.setSceneRect(0, 0, length, width)
        self.canvas_widget.setFixedSize(length, width)
        self.setWindowTitle('CG Demo')

    def save_canvas_action(self):
        self.statusBar().showMessage('保存画布')
        menu_bar = QFileDialog.Options()
        self.path, cond = QFileDialog.getSaveFileName(
            self, "QFileDialog.getSaveFileName()", "", "Pictures (*.bmp)", options=menu_bar)
        if cond:
            image = self.canvas_widget.grab(
                self.canvas_widget.sceneRect().toRect())
            image.save(self.path)

    def quit_action(self):
        self.statusBar().showMessage('退出')
        reply = QMessageBox.question(
            self, '退出,是否保存', '退出,是否保存', QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            self.save_canvas_action()
            qApp.quit()
        elif reply == QMessageBox.No:
            qApp.quit()

    def set_pen_action(self):
        color = QColorDialog.getColor()
        if (color.isValid()):
            self.canvas_widget.pen_color = color

    def curve_bezier_action(self):
        self.canvas_widget.start_draw_curve('Bezier', self.get_id())
        self.statusBar().showMessage('Bezier曲线')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def curve_b_spline_action(self):
        self.canvas_widget.start_draw_curve('B-spline', self.get_id())
        self.statusBar().showMessage('B-spline曲线')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def clip_cohen_sutherland_action(self):
        self.canvas_widget.start_clip('Cohen-Sutherland')
        self.statusBar().showMessage('Cohen-Sutherland裁剪')

    def clip_liang_barsky_action(self):
        self.canvas_widget.start_clip('Liang-Barsky')
        self.statusBar().showMessage('Liang-Barsky裁剪')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
