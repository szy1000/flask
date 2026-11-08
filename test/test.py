# -*- coding: utf-8 -*-
"""
@Time       : 2026/11/7 23:42
@Author     : jack_shen
@File       : test.py
@Description: 
"""

a = 0



def add():
    # a = 0 放到这里 用global报错 需要用nonlocal
    def subAdd():
        global a
        print('first',a)
        a =  a + 1
        print('second',a + 1)
    subAdd()
    return a


print(add())
