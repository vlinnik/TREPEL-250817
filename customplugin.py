#!/usr/bin/python3
from qtpy.QtGui import QIcon
from qtpy.QtWidgets import QWidget
from pysca.helpers import register_user_widgets

register_user_widgets('ui/widgets',ctx=globals(),include='customplugin')
# Пример пользовательского плагина для Qt Designer

