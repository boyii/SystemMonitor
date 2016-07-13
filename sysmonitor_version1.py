# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sysmonitor.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from usage_function_version1 import memUsage, cpuUsage, diskUsage, NetworkUsage


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(796, 406)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.widget = QtGui.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(60, 100, 601, 166))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label = QtGui.QLabel(self.widget)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_2.addWidget(self.label)
        self.cpuUsage = QtGui.QProgressBar(self.widget)
        self.cpuUsage.setProperty("value", 30)
        self.cpuUsage.setObjectName(_fromUtf8("cpuUsage"))
        self.horizontalLayout_2.addWidget(self.cpuUsage)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_3 = QtGui.QLabel(self.widget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_3.addWidget(self.label_3)
        self.memUsage = QtGui.QProgressBar(self.widget)
        self.memUsage.setProperty("value", 24)
        self.memUsage.setObjectName(_fromUtf8("memUsage"))
        self.horizontalLayout_3.addWidget(self.memUsage)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label_2 = QtGui.QLabel(self.widget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_4.addWidget(self.label_2)
        self.diskUsage = QtGui.QProgressBar(self.widget)
        self.diskUsage.setProperty("value", 24)
        self.diskUsage.setObjectName(_fromUtf8("diskUsage"))
        self.horizontalLayout_4.addWidget(self.diskUsage)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_4 = QtGui.QLabel(self.widget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout.addWidget(self.label_4)
        self.netUsage = QtGui.QLabel(self.widget)
        self.netUsage.setObjectName(_fromUtf8("netUsage"))
        self.horizontalLayout.addWidget(self.netUsage)
        self.verticalLayout.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 796, 38))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        ## for update usage every 1 second
        self.ctimer = QtCore.QTimer()
        QtCore.QObject.connect(self.ctimer, QtCore.SIGNAL("timeout()"), self.updateUsage)
        
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        ## set up initial value of every usage
        self.memUsage.setValue(memUsage())
        self.cpuUsage.setValue(cpuUsage())
        self.diskUsage.setValue(diskUsage())
        self.netUsage.setText(NetworkUsage())    

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.label.setText(_translate("MainWindow", "CPU usage:      ", None))
        self.label_3.setText(_translate("MainWindow", "Memory usage: ", None))
        self.label_2.setText(_translate("MainWindow", "Disk usage:      ", None))
        self.label_4.setText(_translate("MainWindow", "Network usage:", None))
        self.netUsage.setText(_translate("MainWindow", "TextLabel", None))
        ## for start ctimer
        self.ctimer.start(1000)
        
    def updateUsage(self):
        self.memUsage.setValue(memUsage())
        self.cpuUsage.setValue(cpuUsage())
        self.diskUsage.setValue(diskUsage())
        self.netUsage.setText(NetworkUsage())


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    mainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())    
