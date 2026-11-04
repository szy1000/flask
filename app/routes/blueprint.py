# -*- coding: utf-8 -*-
"""
@Time       : 2026/11/4 16:48
@Author     : jack_shen
@File       : blueprint.py
@Description: 
"""

from flask import Blueprint

main_bp = Blueprint("main", __name__, url_prefix="/api")