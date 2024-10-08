# This Python file uses the following encoding: utf-8
import sys
import os
from PySide6.QtCore import QProcess
from PySide6.QtQuick import QQuickWindow,QSGRendererInterface
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

# 请通过launch.json运行，直接运行main.py不会执行pyside6-rcc，而导致资源文件缺少，具体逻辑查看tasks.json与Scripts/qrc2py.py
# 需要输出exe，安装pip install pyinstaller，然后pyinstaller example/main.spec，打包之前请先执行tasks.json，导出example_rc.py资源文件
# example_rc.py位置在example/resource文件夹下
#----------------------------------------------------------
import FluentUI

from helper.SettingsHelper import SettingsHelper
from AppInfo import AppInfo

# 注册资源以及自定义的QML组件
import resource.example_rc
from component.CircularReveal import CircularReveal
from component.FileWatcher import FileWatcher
from component.FpsItem import FpsItem
import helper.Log as Log

def main():
    Log.setup("example")
    QQuickWindow.setGraphicsApi(QSGRendererInterface.GraphicsApi.OpenGL)
    os.environ["QT_QUICK_CONTROLS_STYLE"] = "Basic"
    SettingsHelper().init()

    app = QGuiApplication(sys.argv)
    app.setOrganizationName("Quby")
    app.setOrganizationDomain("https://www.google.com")
    app.setApplicationName("example")

    engine = QQmlApplicationEngine()
    rootContext = engine.rootContext()
    rootContext.setContextProperty("SettingsHelper", SettingsHelper())
    rootContext.setContextProperty("AppInfo", AppInfo())
    
    FluentUI.init(engine)
    print(engine.importPathList())
    qml_file = "qrc:/example/qml/App.qml"
    engine.load(qml_file)
    if not engine.rootObjects():
        sys.exit(-1)

    exit_code = app.exec()
    if(exit_code == 931):
        #QGuiApplication.applicationFilePath()需要打包成exe后才能正确的路径重启，不然这个函数获取的路径是python的路径
        args = QGuiApplication.arguments()[1:]
        QProcess.startDetached(QGuiApplication.applicationFilePath(),args)
    
    sys.exit(exit_code)

if __name__ == "__main__":
    main()