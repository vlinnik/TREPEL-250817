#!/usr/bin/python3
from AnyQt.QtGui import QIcon
from AnyQt.QtWidgets import QWidget
from pysca.helpers import register_user_widgets

register_user_widgets('ui/widgets',ctx=globals(),include='customplugin')
# Пример пользовательского плагина для Qt Designer

