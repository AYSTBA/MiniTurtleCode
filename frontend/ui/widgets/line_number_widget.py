#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
行号显示组件
"""

from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QColor

class LineNumberWidget(QWidget):
    """行号显示widget"""
    def __init__(self, editor, parent=None):
        super().__init__(parent)
        self.editor = editor
        self.setStyleSheet("background-color: #f0f0f0; border-right: 1px solid #d0d0d0;")
        self.setFixedWidth(40)
        self.update_line_numbers()
        
        # 连接信号，当编辑器内容变化时更新行号
        editor.textChanged.connect(self.update_line_numbers)
        editor.verticalScrollBar().valueChanged.connect(self.update_line_numbers)
    
    def update_line_numbers(self):
        """更新行号"""
        self.update()
    
    def paintEvent(self, event):
        """绘制行号"""
        painter = QPainter(self)
        painter.setPen(QColor('#808080'))
        font = painter.font()
        font.setPointSize(10)
        painter.setFont(font)
        
        # 获取编辑器的可见区域
        viewport = self.editor.viewport()
        top = viewport.geometry().top()
        bottom = viewport.geometry().bottom()
        
        # 获取可见区域的第一行和最后一行
        first_block = self.editor.firstVisibleBlock()
        last_block = first_block
        while True:
            next_block = last_block.next()
            if not next_block.isValid() or self.editor.blockBoundingGeometry(next_block).translated(self.editor.contentOffset()).top() > bottom:
                break
            last_block = next_block
        
        # 绘制行号
        block = first_block
        line_number = block.blockNumber() + 1
        while block.isValid() and block != last_block.next():
            rect = self.editor.blockBoundingGeometry(block).translated(self.editor.contentOffset())
            if rect.top() > bottom:
                break
            painter.drawText(5, rect.top() + rect.height() - 5, str(line_number))
            block = block.next()
            line_number += 1
