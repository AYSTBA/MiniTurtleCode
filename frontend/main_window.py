#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mini Turtle Code - 主窗口类
"""

import sys
import os
import subprocess
import threading
from PySide6.QtWidgets import (
    QMainWindow, QMenuBar, QDockWidget, QTextEdit, QPlainTextEdit, 
    QTreeView, QFileSystemModel, QVBoxLayout, QWidget, QSplitter,
    QStackedWidget, QToolBar, QPushButton, QStatusBar, QMessageBox, QFileDialog,
    QHBoxLayout
)
from PySide6.QtGui import QAction, QTextCursor
from PySide6.QtCore import Qt, QDir, QSize
from PySide6.QtWebEngineWidgets import QWebEngineView

from .ui.widgets import LineNumberWidget, TurtleWidget, PythonSyntaxHighlighter

class MainWindow(QMainWindow):
    """主窗口类"""
    def __init__(self):
        super().__init__()
        self.last_save_path = None  # 上一次保存的文件路径
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        # 设置窗口属性
        self.setWindowTitle("Mini Turtle Code")
        self.setGeometry(100, 100, 1280, 720)
        self.setMinimumSize(1024, 600)
        
        # 创建主编辑区和绘图区
        self.create_main_editor()
        self.create_turtle_view()
        
        # 创建左侧边栏
        self.create_left_sidebar()
        
        # 创建底部终端
        self.create_terminal()
        
        # 创建菜单栏
        self.create_menu_bar()
        
        # 创建状态栏
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("就绪")
        
        # 创建运行按钮
        self.create_run_button()
        
        # 布局管理
        self.setup_layout()
        
        # 默认隐藏导航栏
        self.toggle_nav()
    
    def create_menu_bar(self):
        """创建菜单栏"""
        # 确保菜单栏在最顶层
        menu_bar = self.menuBar()
        menu_bar.raise_()
        
        # 设置菜单栏样式，确保文字可见且可点击
        menu_bar.setStyleSheet("QMenuBar { background-color: #f0f0f0; border: 1px solid #d0d0d0; } QMenuBar::item { padding: 6px 12px; font-size: 12px; } QMenuBar::item:selected { background-color: #e0e0e0; } QMenu { background-color: white; border: 1px solid #d0d0d0; } QMenu::item { padding: 4px 20px; } QMenu::item:selected { background-color: #e0e0e0; }")
        
        # 文件菜单
        file_menu = menu_bar.addMenu("文件")
        
        new_action = QAction("新建 (Ctrl+N)", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)
        
        open_action = QAction("打开 (Ctrl+O)", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        
        save_action = QAction("保存 (Ctrl+S)", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)
        
        save_as_action = QAction("另存为 (Ctrl+Shift+S)", self)
        save_as_action.setShortcut("Ctrl+Shift+S")
        save_as_action.triggered.connect(self.save_as_file)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("退出", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 编辑菜单
        edit_menu = menu_bar.addMenu("编辑")
        
        undo_action = QAction("撤销 (Ctrl+Z)", self)
        undo_action.setShortcut("Ctrl+Z")
        undo_action.triggered.connect(self.editor.undo)
        edit_menu.addAction(undo_action)
        
        redo_action = QAction("重做 (Ctrl+Y)", self)
        redo_action.setShortcut("Ctrl+Y")
        redo_action.triggered.connect(self.editor.redo)
        edit_menu.addAction(redo_action)
        
        edit_menu.addSeparator()
        
        copy_action = QAction("复制 (Ctrl+C)", self)
        copy_action.setShortcut("Ctrl+C")
        copy_action.triggered.connect(self.editor.copy)
        edit_menu.addAction(copy_action)
        
        paste_action = QAction("粘贴 (Ctrl+V)", self)
        paste_action.setShortcut("Ctrl+V")
        paste_action.triggered.connect(self.editor.paste)
        edit_menu.addAction(paste_action)
        
        select_all_action = QAction("全选 (Ctrl+A)", self)
        select_all_action.setShortcut("Ctrl+A")
        select_all_action.triggered.connect(self.editor.selectAll)
        edit_menu.addAction(select_all_action)
        
        # 视图菜单
        view_menu = menu_bar.addMenu("视图")
        
        toggle_terminal_action = QAction("显示/隐藏终端 (F12)", self)
        toggle_terminal_action.setShortcut("F12")
        toggle_terminal_action.triggered.connect(self.toggle_terminal)
        view_menu.addAction(toggle_terminal_action)
        
        toggle_nav_action = QAction("显示/隐藏导航栏 (F11)", self)
        toggle_nav_action.setShortcut("F11")
        toggle_nav_action.triggered.connect(self.toggle_nav)
        view_menu.addAction(toggle_nav_action)
        
        # 确保菜单栏获得焦点
        menu_bar.setFocusPolicy(Qt.StrongFocus)
        # 确保菜单栏可点击
        menu_bar.setEnabled(True)
    
    def create_left_sidebar(self):
        """创建左侧边栏"""
        # 创建左侧工具条
        self.left_toolbar = QToolBar("导航", self)
        self.left_toolbar.setOrientation(Qt.Vertical)
        self.left_toolbar.setFixedWidth(50)
        
        # 创建切换按钮
        file_explorer_btn = QPushButton("📁", self)
        file_explorer_btn.setToolTip("文件资源管理器")
        file_explorer_btn.setFixedSize(40, 40)
        file_explorer_btn.setStyleSheet("font-size: 18px;")
        file_explorer_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.left_toolbar.addWidget(file_explorer_btn)
        
        website_btn = QPushButton("🌐", self)
        website_btn.setToolTip("官网入口")
        website_btn.setFixedSize(40, 40)
        website_btn.setStyleSheet("font-size: 18px;")
        website_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        self.left_toolbar.addWidget(website_btn)
        
        competition_btn = QPushButton("🏆", self)
        competition_btn.setToolTip("赛事入口")
        competition_btn.setFixedSize(40, 40)
        competition_btn.setStyleSheet("font-size: 18px;")
        competition_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        self.left_toolbar.addWidget(competition_btn)
        
        # 创建堆栈窗口
        self.stacked_widget = QStackedWidget(self)
        
        # 文件资源管理器
        file_model = QFileSystemModel()
        file_model.setRootPath(QDir.currentPath())
        self.file_tree = QTreeView()
        self.file_tree.setModel(file_model)
        self.file_tree.setRootIndex(file_model.index(QDir.currentPath()))
        # 连接双击信号，实现双击打开文件
        self.file_tree.doubleClicked.connect(self.open_file_from_tree)
        self.stacked_widget.addWidget(self.file_tree)
        
        # 官网入口
        self.website_view = QWebEngineView()
        self.website_view.setUrl("https://example.com")  # 占位URL
        self.stacked_widget.addWidget(self.website_view)
        
        # 赛事入口
        self.competition_view = QWebEngineView()
        self.competition_view.setUrl("https://example.com/competition")  # 占位URL
        self.stacked_widget.addWidget(self.competition_view)
        
        # 创建左侧停靠窗口
        self.left_dock = QDockWidget("导航", self)
        self.left_dock.setAllowedAreas(Qt.LeftDockWidgetArea)
        self.left_dock.setWidget(self.stacked_widget)
        self.left_dock.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)
        
        self.addDockWidget(Qt.LeftDockWidgetArea, self.left_dock)
        self.addToolBar(Qt.LeftToolBarArea, self.left_toolbar)
    
    def create_main_editor(self):
        """创建主编辑区"""
        # 创建编辑器和行号widget
        self.editor = QPlainTextEdit(self)
        self.editor.setPlainText("#!/usr/bin/env python3\n# -*- coding: utf-8 -*-\n\nimport turtle\n\n# 绘制一个正方形\nt = turtle.Turtle()\nfor _ in range(4):\n    t.forward(100)\n    t.right(90)\n\nturtle.done()")
        
        # 添加行号显示
        self.line_number_widget = LineNumberWidget(self.editor)
        
        # 创建水平布局，包含行号和编辑器
        editor_layout = QHBoxLayout()
        editor_layout.addWidget(self.line_number_widget)
        editor_layout.addWidget(self.editor)
        editor_layout.setContentsMargins(0, 0, 0, 0)
        
        # 创建容器widget
        editor_container = QWidget(self)
        editor_container.setLayout(editor_layout)
        
        # 保存容器widget引用
        self.editor_container = editor_container
        
        # 添加语法高亮
        self.highlighter = PythonSyntaxHighlighter(self.editor.document())
        
        # 连接信号，实现自动缩进
        self.editor.textChanged.connect(self.handle_text_changed)
        
        # 连接编辑器的滚动条信号，确保行号同步滚动
        self.editor.verticalScrollBar().valueChanged.connect(self.line_number_widget.update_line_numbers)
        
        # 连接编辑器的尺寸变化信号，确保行号widget高度一致
        self.editor.resizeEvent = lambda event: self.line_number_widget.setFixedHeight(self.editor.height())
    

    
    def create_turtle_view(self):
        """创建海龟绘图视图"""
        self.turtle_widget = QWidget(self)
        self.turtle_layout = QVBoxLayout(self.turtle_widget)
        
        # 清空按钮
        clear_button = QPushButton("清空画布 (Ctrl+Shift+R)", self)
        clear_button.setShortcut("Ctrl+Shift+R")
        clear_button.clicked.connect(self.clear_turtle)
        self.turtle_layout.addWidget(clear_button)
        
        # 绘图区域 - 使用自定义的TurtleWidget
        self.turtle_display = TurtleWidget(self)
        self.turtle_layout.addWidget(self.turtle_display)
        
        # 初始化turtle实例
        self.turtle_instance = self.turtle_display
        
        # 添加运行按钮
        run_button = QPushButton("运行代码 (F5)", self)
        run_button.setShortcut("F5")
        run_button.clicked.connect(self.run_code)
        self.turtle_layout.addWidget(run_button)
    
    def create_terminal(self):
        """创建终端"""
        self.terminal = QTextEdit(self)
        self.terminal.setReadOnly(True)
        self.terminal.setStyleSheet("background-color: #f0f0f0;")
        # 允许复制操作
        self.terminal.setTextInteractionFlags(Qt.TextSelectableByMouse | Qt.TextSelectableByKeyboard)
        
        # 创建终端停靠窗口
        self.terminal_dock = QDockWidget("输出终端", self)
        self.terminal_dock.setAllowedAreas(Qt.BottomDockWidgetArea)
        # 移除关闭按钮，只保留浮动和停靠按钮（大小调节默认启用）
        self.terminal_dock.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)
        self.terminal_dock.setWidget(self.terminal)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.terminal_dock)
        # 设置终端的最小高度
        self.terminal_dock.setMinimumHeight(100)
    
    def create_run_button(self):
        """创建运行按钮"""
        self.run_button = QPushButton("运行 (F5)", self)
        self.run_button.clicked.connect(self.run_code)
        self.status_bar.addPermanentWidget(self.run_button)
    
    def setup_layout(self):
        """设置布局"""
        # 创建主分割器
        main_splitter = QSplitter(Qt.Horizontal, self)
        
        # 主编辑区和绘图区分割器
        editor_splitter = QSplitter(Qt.Horizontal, main_splitter)
        editor_splitter.addWidget(self.editor_container)
        editor_splitter.addWidget(self.turtle_widget)
        editor_splitter.setSizes([600, 400])
        
        # 设置中心部件
        self.setCentralWidget(editor_splitter)
    
    def new_file(self):
        """新建文件"""
        self.editor.clear()
        self.editor.setPlainText("#!/usr/bin/env python3\n# -*- coding: utf-8 -*-\n\nimport turtle\n")
        self.status_bar.showMessage("新建文件")
    
    def open_file(self):
        """打开文件"""
        file_path, _ = QFileDialog.getOpenFileName(self, "打开文件", "", "Python文件 (*.py)")
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.editor.setPlainText(content)
                self.status_bar.showMessage(f"打开文件: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"无法打开文件: {str(e)}")
    
    def save_file(self):
        """保存文件"""
        # 如果有上一次保存路径，直接使用
        if self.last_save_path:
            file_path = self.last_save_path
        else:
            # 否则打开文件对话框
            file_path, _ = QFileDialog.getSaveFileName(self, "保存文件", "", "Python文件 (*.py);;Mini Turtle文件 (*.mtc)")
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.editor.toPlainText())
                self.last_save_path = file_path  # 更新上一次保存路径
                self.status_bar.showMessage(f"保存文件: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"无法保存文件: {str(e)}")
    
    def save_as_file(self):
        """另存为文件"""
        # 总是打开文件对话框，让用户选择新的保存位置
        file_path, _ = QFileDialog.getSaveFileName(self, "另存为文件", "", "Python文件 (*.py);;Mini Turtle文件 (*.mtc)")
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.editor.toPlainText())
                self.last_save_path = file_path  # 更新上一次保存路径
                self.status_bar.showMessage(f"保存文件: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"无法保存文件: {str(e)}")
    
    def toggle_terminal(self):
        """显示/隐藏终端"""
        if self.terminal_dock.isVisible():
            self.terminal_dock.hide()
        else:
            self.terminal_dock.show()
    
    def toggle_nav(self):
        """显示/隐藏导航栏"""
        if self.left_dock.isVisible():
            self.left_dock.hide()
            self.left_toolbar.hide()
        else:
            self.left_dock.show()
            self.left_toolbar.show()
    

    
    def run_code(self):
        """运行代码"""
        # 运行代码
        self.terminal.clear()
        self.terminal.append("=== 运行结果 ===")
        
        # 获取用户代码
        code = self.editor.toPlainText()
        
        # 清空之前的绘图
        if self.turtle_instance:
            self.turtle_instance.clear()
        
        # 创建一个完整的turtle模块模拟器
        class Turtle:
            def __init__(self, widget):
                self.widget = widget
                self.fill_color = QColor(255, 255, 255)
                self.is_filling = False
                self.filling_points = []
            
            def forward(self, distance):
                self.widget.forward(distance)
            
            def backward(self, distance):
                self.widget.backward(distance)
            
            def right(self, angle):
                self.widget.right(angle)
            
            def left(self, angle):
                self.widget.left(angle)
            
            def penup(self):
                self.widget.penup()
            
            def pendown(self):
                self.widget.pendown()
            
            def color(self, color):
                self.widget.setpencolor(color)
            
            def pencolor(self, color):
                self.widget.setpencolor(color)
            
            def fillcolor(self, color):
                if isinstance(color, str):
                    self.fill_color = QColor(color)
                elif isinstance(color, tuple) and len(color) == 3:
                    self.fill_color = QColor(*color)
            
            def pensize(self, size):
                self.widget.setpensize(size)
            
            def speed(self, speed):
                # 设置TurtleWidget的速度
                self.widget.set_speed(speed)
            
            def begin_fill(self):
                self.is_filling = True
                self.filling_points = []
            
            def end_fill(self):
                self.is_filling = False
                # 这里可以实现填充功能，但需要修改TurtleWidget
            
            def goto(self, x, y):
                self.widget.goto(x, y)
            
            def hideturtle(self):
                # 模拟hideturtle方法，实际不做任何操作
                pass
            
            def clear(self):
                self.widget.clear()
        
        class TurtleModule:
            def __init__(self, widget):
                self.widget = widget
                self._screen = None
            
            def Turtle(self):
                return Turtle(self.widget)
            
            def done(self):
                pass
            
            def forward(self, distance):
                self.widget.forward(distance)
            
            def backward(self, distance):
                self.widget.backward(distance)
            
            def right(self, angle):
                self.widget.right(angle)
            
            def left(self, angle):
                self.widget.left(angle)
            
            def penup(self):
                self.widget.penup()
            
            def pendown(self):
                self.widget.pendown()
            
            def color(self, color):
                self.widget.setpencolor(color)
            
            def pencolor(self, color):
                self.widget.setpencolor(color)
            
            def fillcolor(self, color):
                pass
            
            def pensize(self, size):
                self.widget.setpensize(size)
            
            def speed(self, speed):
                pass
            
            def begin_fill(self):
                pass
            
            def goto(self, x, y):
                self.widget.goto(x, y)
            
            def end_fill(self):
                pass
            
            def hideturtle(self):
                pass
            
            def clear(self):
                self.widget.clear()
        
        # 创建turtle模块实例
        turtle_module = TurtleModule(self.turtle_instance)
        
        # 创建一个全局命名空间，包含自定义的turtle模块
        global_vars = {
            'turtle': turtle_module,
            '__builtins__': __builtins__
        }
        
        # 创建一个局部命名空间
        local_vars = {
            't': Turtle(self.turtle_instance),
            'forward': self.turtle_instance.forward,
            'backward': self.turtle_instance.backward,
            'right': self.turtle_instance.right,
            'left': self.turtle_instance.left,
            'penup': self.turtle_instance.penup,
            'pendown': self.turtle_instance.pendown,
            'setpencolor': self.turtle_instance.setpencolor,
            'setpensize': self.turtle_instance.setpensize,
            'clear': self.turtle_instance.clear,
            'goto': self.turtle_instance.goto
        }
        
        # 执行用户代码
        try:
            # 替换代码中的import turtle语句
            modified_code = code.replace('import turtle', '# import turtle (replaced by Mini Turtle Code)')
            
            # 重定向标准输出和输入
            import io
            import sys
            old_stdout = sys.stdout
            old_stdin = sys.stdin
            sys.stdout = io.StringIO()
            
            # 自定义input函数
            def custom_input(prompt=''):
                from PySide6.QtWidgets import QInputDialog
                text, ok = QInputDialog.getText(self, "输入", prompt)
                if ok:
                    return text
                return ''
            
            # 添加custom_input到全局变量
            global_vars['input'] = custom_input
            
            try:
                exec(modified_code, global_vars, local_vars)
                # 获取print输出
                output = sys.stdout.getvalue()
                if output:
                    self.terminal.append(output)
                self.terminal.append("代码运行成功！")
            finally:
                sys.stdout = old_stdout
                sys.stdin = old_stdin
                
        except Exception as e:
            import traceback
            error_msg = f"错误: {str(e)}\n{traceback.format_exc()}"
            self.terminal.append(error_msg)
    

    
    def clear_turtle(self):
        """清空海龟画布"""
        if self.turtle_instance:
            self.turtle_instance.clear()
            self.terminal.append("=== 画布已清空 ===")
        else:
            self.terminal.append("=== 请先运行代码创建海龟实例 ===")
    
    def handle_text_changed(self):
        """处理文本变化，实现自动缩进"""
        from PySide6.QtGui import QTextCursor
        cursor = self.editor.textCursor()
        # 获取当前行
        cursor.movePosition(QTextCursor.StartOfLine)
        cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)
        current_line = cursor.selectedText()
        
        # 检查是否以冒号结尾
        if current_line.strip().endswith(':'):
            # 移动到行尾
            cursor.movePosition(QTextCursor.EndOfLine)
            # 插入换行和缩进
            cursor.insertText('\n    ')
            # 更新光标位置
            self.editor.setTextCursor(cursor)
    
    def open_file_from_tree(self, index):
        """从文件树中打开文件"""
        file_model = self.file_tree.model()
        file_path = file_model.filePath(index)
        # 检查是否是Python文件
        if file_path.endswith('.py'):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.editor.setPlainText(content)
                self.status_bar.showMessage(f"打开文件: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"无法打开文件: {str(e)}")
