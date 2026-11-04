# -*- coding: utf-8 -*-
"""
@Time       : 2026/11/4 17:10
@Author     : jack_shen
@File       : book.py
@Description: 
"""
# from flask_wtf import FlaskForm
from wtforms import Form, StringField, IntegerField
from wtforms.validators import DataRequired, length, NumberRange


class SearchForm(Form):
    keywords = StringField(validators=[length(min=1, max=30), DataRequired()])
    page = IntegerField(validators=[DataRequired(), NumberRange(min=1, max=99)], default=1)
