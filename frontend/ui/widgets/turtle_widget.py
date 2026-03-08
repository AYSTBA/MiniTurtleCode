#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
海龟绘图组件
"""

from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QColor
from PySide6.QtCore import QPoint, QTimer

class TurtleWidget(QWidget):
    """自定义的turtle绘图widget"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(400, 300)
        self.setStyleSheet("background-color: white;")
        
        # 初始化turtle状态
        self.position = QPoint(200, 150)  # 初始位置
        self.angle = 0  # 初始角度（度）
        self.pen_down = True  # 初始状态为落笔
        self.pen_color = QColor(0, 0, 0)  # 初始颜色为黑色
        self.pen_width = 1  # 初始笔宽
        self._speed = 5  # 初始速度（1-10，1最慢，10最快）
        
        # 存储绘制的路径
        self.paths = []
        
        # 动画相关
        self.animation_active = False
        self.animation_timer = None
        self.animation_steps = []
    
    def paintEvent(self, event):
        """绘制事件"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 绘制所有路径
        for path in self.paths:
            pen = QPen(path['color'], path['width'])
            painter.setPen(pen)
            painter.drawPolyline(path['points'])
    
    def forward(self, distance):
        """向前移动（带动画）"""
        from math import radians, cos, sin
        angle_rad = radians(self.angle)
        new_x = self.position.x() + distance * cos(angle_rad)
        new_y = self.position.y() - distance * sin(angle_rad)  # y轴向下为正
        
        # 直接绘制，不使用动画，确保所有步骤都能完成
        if self.pen_down:
            # 添加新路径
            points = [self.position, QPoint(new_x, new_y)]
            self.paths.append({
                'points': points,
                'color': self.pen_color,
                'width': self.pen_width
            })
        
        # 更新位置
        self.position = QPoint(new_x, new_y)
        self.update()
    
    def goto(self, x, y):
        """移动到指定位置"""
        new_x, new_y = x, y
        
        # 直接绘制，不使用动画，确保所有步骤都能完成
        if self.pen_down:
            # 添加新路径
            points = [self.position, QPoint(new_x, new_y)]
            self.paths.append({
                'points': points,
                'color': self.pen_color,
                'width': self.pen_width
            })
        
        # 更新位置
        self.position = QPoint(new_x, new_y)
        self.update()
    
    def start_animation(self):
        """开始动画"""
        if not self.animation_steps:
            return
        
        self.animation_active = True
        self.animation_timer = QTimer(self)
        
        def animate():
            if not self.animation_steps:
                self.animation_timer.stop()
                self.animation_active = False
                return
            
            # 获取下一步位置
            next_pos = self.animation_steps.pop(0)
            
            # 添加路径
            if self.pen_down:
                points = [self.position, next_pos]
                self.paths.append({
                    'points': points,
                    'color': self.pen_color,
                    'width': self.pen_width
                })
            
            # 更新位置
            self.position = next_pos
            self.update()
        
        # 根据速度设置定时器间隔
        interval = max(10, 100 - self._speed * 9)  # 速度1-10对应间隔100-19ms
        self.animation_timer.timeout.connect(animate)
        self.animation_timer.start(interval)
    
    def backward(self, distance):
        """向后移动"""
        self.forward(-distance)
    
    def right(self, angle):
        """向右转"""
        self.angle -= angle
    
    def left(self, angle):
        """向左转"""
        self.angle += angle
    
    def penup(self):
        """抬笔"""
        self.pen_down = False
    
    def pendown(self):
        """落笔"""
        self.pen_down = True
    
    def setpencolor(self, color):
        """设置笔色"""
        if isinstance(color, str):
            self.pen_color = QColor(color)
        elif isinstance(color, tuple) and len(color) == 3:
            self.pen_color = QColor(*color)
    
    def setpensize(self, size):
        """设置笔宽"""
        self.pen_width = size
    
    def clear(self):
        """清空画布"""
        self.paths = []
        self.position = QPoint(200, 150)
        self.angle = 0
        self.update()
    
    def set_speed(self, speed):
        """设置速度"""
        # 限制速度范围在1-10之间，0表示最快
        if speed == 0:
            self._speed = 10  # 0表示最快
        else:
            self._speed = max(1, min(10, speed))
