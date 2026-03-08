#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Turtle runner script for embedding turtle window into Qt application
"""

import turtle
import sys
import ctypes
import json
import os
import time

# Get the window handle of the turtle window
def get_turtle_window_handle():
    """获取turtle窗口的句柄"""
    # Create a turtle screen
    screen = turtle.Screen()
    screen.title("Mini Turtle Code")
    
    # Get the window handle using ctypes
    hwnd = ctypes.windll.user32.FindWindowW(None, "Mini Turtle Code")
    return hwnd, screen

if __name__ == "__main__":
    print(f"当前工作目录: {os.getcwd()}")
    print(f"命令行参数: {sys.argv}")
    
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        print(f"尝试读取文件: {file_path}")
        print(f"文件是否存在: {os.path.exists(file_path)}")
        
        # Read user code from file
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                user_code = f.read()
            print("文件读取成功")
            
            # Get window handle and screen
            hwnd, screen = get_turtle_window_handle()
            print(f"获取到窗口句柄: {hwnd}")
            
            # Send window handle back to parent process
            print(json.dumps({"hwnd": hwnd}))
            sys.stdout.flush()
            
            # Wait for embedding to complete
            time.sleep(1.0)
            
            # Run user code
            print("开始执行用户代码")
            exec(user_code)
            print("用户代码执行完成")
            
            # Keep the window open
            try:
                turtle.done()
            except turtle.Terminator:
                print("Turtle窗口已关闭")
        except Exception as e:
            print(f"错误: {str(e)}")
            import traceback
            traceback.print_exc()
    else:
        print("没有提供文件路径参数")
