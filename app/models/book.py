# -*- coding: utf-8 -*-
"""
@Time       : 2026/11/4 17:40
@Author     : jack_shen
@File       : book.py
@Description: 
"""

# from flask_sqlalchemy import
from sqlalchemy import Column, Integer, String, Date
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Book(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    author = Column(String(30), nullable=True, default='未知')
    binding = Column(String(20))
    publisher = Column(String(50))
    pubdate = Column(Date, nullable=True)
    isbn = Column(String(50), nullable=False, default='', unique=True)
    summary = Column(String(1000))
    image_url = Column(String(50))
