#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
代码联想功能模块
"""

import re

class CodeCompletion:
    """代码联想类"""
    def __init__(self):
        # Python关键字
        self.keywords = [
            'and', 'as', 'assert', 'break', 'class', 'continue', 'def', 'del',
            'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if',
            'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass',
            'raise', 'return', 'try', 'while', 'with', 'yield'
        ]
        
        # 内置函数
        self.builtin_functions = [
            'print', 'input', 'len', 'range', 'list', 'dict', 'set', 'tuple',
            'str', 'int', 'float', 'bool', 'type', 'isinstance', 'abs', 'max',
            'min', 'sum', 'sorted', 'enumerate', 'zip', 'map', 'filter', 'reduce',
            'open', 'close', 'read', 'write', 'append', 'extend', 'insert', 'remove',
            'pop', 'clear', 'copy', 'get', 'keys', 'values', 'items'
        ]
        
        # 海龟库函数
        self.turtle_functions = [
            'forward', 'backward', 'right', 'left', 'penup', 'pendown',
            'goto', 'setpencolor', 'setpensize', 'clear', 'speed'
        ]
        
        # 已导入的模块
        self.imported_modules = []
        
        # 自定义函数和变量
        self.custom_functions = []
        self.custom_variables = []
    
    def update_context(self, code):
        """更新代码上下文"""
        # 重置自定义函数和变量
        self.custom_functions = []
        self.custom_variables = []
        
        # 提取导入的模块
        self.imported_modules = []
        import_pattern = re.compile(r'import\s+([a-zA-Z_]\w*)')
        from_import_pattern = re.compile(r'from\s+([a-zA-Z_]\w*)\s+import')
        
        for match in import_pattern.finditer(code):
            self.imported_modules.append(match.group(1))
        
        for match in from_import_pattern.finditer(code):
            self.imported_modules.append(match.group(1))
        
        # 提取自定义函数
        function_pattern = re.compile(r'def\s+([a-zA-Z_]\w*)\s*\(')
        for match in function_pattern.finditer(code):
            self.custom_functions.append(match.group(1))
        
        # 提取自定义变量（简单实现）
        variable_pattern = re.compile(r'\b([a-zA-Z_]\w*)\s*=')
        for match in variable_pattern.finditer(code):
            var_name = match.group(1)
            if var_name not in self.keywords and var_name not in self.builtin_functions:
                self.custom_variables.append(var_name)
    
    def get_completions(self, text, cursor_pos):
        """获取代码联想建议"""
        # 获取光标前的文本
        prefix = text[:cursor_pos]
        
        # 提取最后一个单词
        last_word = ''
        for char in reversed(prefix):
            if char.isalnum() or char == '_':
                last_word = char + last_word
            else:
                break
        
        # 生成联想建议
        completions = []
        
        # 关键字联想
        for keyword in self.keywords:
            if keyword.startswith(last_word):
                completions.append({'type': 'keyword', 'text': keyword, 'description': 'Python关键字'})
        
        # 内置函数联想
        for func in self.builtin_functions:
            if func.startswith(last_word):
                completions.append({'type': 'function', 'text': func, 'description': '内置函数'})
        
        # 海龟库函数联想
        if 'turtle' in self.imported_modules:
            for func in self.turtle_functions:
                if func.startswith(last_word):
                    completions.append({'type': 'function', 'text': func, 'description': 'turtle库函数'})
        
        # 自定义函数联想
        for func in self.custom_functions:
            if func.startswith(last_word):
                completions.append({'type': 'function', 'text': func, 'description': '自定义函数'})
        
        # 自定义变量联想
        for var in self.custom_variables:
            if var.startswith(last_word):
                completions.append({'type': 'variable', 'text': var, 'description': '自定义变量'})
        
        # 模块联想
        for module in self.imported_modules:
            if module.startswith(last_word):
                completions.append({'type': 'module', 'text': module, 'description': '导入的模块'})
        
        # 去重并限制数量
        seen = set()
        unique_completions = []
        for comp in completions:
            if comp['text'] not in seen:
                seen.add(comp['text'])
                unique_completions.append(comp)
        
        return unique_completions[:10]  # 最多返回10个建议
