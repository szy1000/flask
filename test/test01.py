# -*- coding: utf-8 -*-
"""
@Time       : 2026/11/5 15:37
@Author     : jack_shen
@File       : test01.py
@Description: 
"""

from werkzeug.local import LocalStack


s = LocalStack()
s.push(1)
print(s.pop)
print(s.top)