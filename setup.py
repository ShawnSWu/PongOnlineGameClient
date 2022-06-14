"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['main.py']
DATA_FILES = ['view', 'font', 'img', 'menu', 'config', 'online']
OPTIONS = {
    'includes': ['pygame'],
    'iconfile': 'img/app_icon.png',

}

setup(
    name="The Pong",
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)