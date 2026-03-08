#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python语法高亮器组件
"""

from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor
import re

class PythonSyntaxHighlighter(QSyntaxHighlighter):
    """Python语法高亮器"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.keywords = [
            'and', 'as', 'assert', 'break', 'class', 'continue', 'def', 'del',
            'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if',
            'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass',
            'raise', 'return', 'try', 'while', 'with', 'yield'
        ]
        
        # 关键字格式
        self.keyword_format = QTextCharFormat()
        self.keyword_format.setForeground(QColor('#800080'))  # 紫色
        self.keyword_format.setFontWeight(75)
        
        # 字符串格式
        self.string_format = QTextCharFormat()
        self.string_format.setForeground(QColor('#008000'))
        
        # 注释格式
        self.comment_format = QTextCharFormat()
        self.comment_format.setForeground(QColor('#808080'))
        
        # 数字格式
        self.number_format = QTextCharFormat()
        self.number_format.setForeground(QColor('#FF8C00'))
        
        # 函数名格式
        self.function_format = QTextCharFormat()
        self.function_format.setForeground(QColor('#800080'))  # 紫色
        self.function_format.setFontWeight(75)
        
        # 类名格式
        self.class_format = QTextCharFormat()
        self.class_format.setForeground(QColor('#4B0082'))
        self.class_format.setFontWeight(75)
        
        # 运算符格式
        self.operator_format = QTextCharFormat()
        self.operator_format.setForeground(QColor('#8B4513'))
        
        # 内置函数格式
        self.builtin_format = QTextCharFormat()
        self.builtin_format.setForeground(QColor('#800080'))  # 紫色
        self.builtin_format.setFontWeight(75)
    
    def highlightBlock(self, text):
        """高亮文本块"""
        # 高亮关键字
        for keyword in self.keywords:
            start = 0
            while True:
                start = text.find(keyword, start)
                if start == -1:
                    break
                if (start == 0 or not text[start-1].isalnum()) and \
                   (start + len(keyword) == len(text) or not text[start + len(keyword)].isalnum()):
                    self.setFormat(start, len(keyword), self.keyword_format)
                start += len(keyword)
        
        # 高亮字符串
        in_string = False
        string_start = 0
        for i, char in enumerate(text):
            if char in ('"', "'") and (i == 0 or text[i-1] != '\\'):
                if not in_string:
                    in_string = True
                    string_start = i
                else:
                    in_string = False
                    self.setFormat(string_start, i - string_start + 1, self.string_format)
        
        # 高亮注释
        comment_start = text.find('#')
        if comment_start != -1:
            self.setFormat(comment_start, len(text) - comment_start, self.comment_format)
        
        # 高亮数字
        for match in re.finditer(r'\b\d+\.?\d*\b', text):
            self.setFormat(match.start(), match.end() - match.start(), self.number_format)
        
        # 高亮函数名
        for match in re.finditer(r'\bdef\s+([a-zA-Z_]\w*)\s*\(', text):
            self.setFormat(match.start(1), match.end(1) - match.start(1), self.function_format)
        
        # 高亮类名
        for match in re.finditer(r'\bclass\s+([a-zA-Z_]\w*)\s*', text):
            self.setFormat(match.start(1), match.end(1) - match.start(1), self.class_format)
        
        # 高亮内置函数
        builtins = ['print', 'input', 'len', 'range', 'list', 'dict', 'set', 'tuple', 'str', 'int', 'float', 'bool', 'type', 'isinstance', 'abs', 'max', 'min', 'sum', 'sorted']
        for builtin in builtins:
            start = 0
            while True:
                start = text.find(builtin, start)
                if start == -1:
                    break
                if (start == 0 or not text[start-1].isalnum()) and \
                   (start + len(builtin) == len(text) or text[start + len(builtin)] in ('(', ' ', '\t', '\n')):
                    self.setFormat(start, len(builtin), self.builtin_format)
                start += len(builtin)
