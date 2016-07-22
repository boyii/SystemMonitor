# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sysmonitor.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!
import sys
import re
import operator
from PyQt4.Qt import *
from PyQt4 import QtCore, QtGui
import psutil as pu
from usage_function_version1 import memUsage, getMemUsage, cpuUsage, getProcessResource, diskIOcountEachProcess, humanize, networkUsageEachDevice, processList, getCPUusage, getProcess
import copy
import numpy as np
from pyqtgraph import GraphicsWindow
import pyqtgraph
from Win10_warning import Windows10_notification

beforeDiskRead = 0
beforeDiskWrite = 0
beforeNetSend = 0
beforeNetRecv = 0
sortedColNum = 0
sortedOrder = Qt.AscendingOrder
netSortedColNum = 0
netSortedOrder = Qt.AscendingOrder
networkUsageList = None
diskUsageList = None
popMsg = None
warnCountList = {}

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
        MainWindow.resize(856, 406)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.widget = QtGui.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(60, 100, 750, 166))
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
        self.label_2.setFixedWidth(166)
        self.horizontalLayout_4.addWidget(self.label_2)
        self.diskUsage = QtGui.QLabel(self.widget)
        self.diskUsage.setObjectName(_fromUtf8("diskUsage"))
        self.horizontalLayout_4.addWidget(self.diskUsage)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_4 = QtGui.QLabel(self.widget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_4.setFixedWidth(166)
        self.horizontalLayout.addWidget(self.label_4)
        self.netUsage = QtGui.QLabel(self.widget)
        self.netUsage.setObjectName(_fromUtf8("netUsage"))
        self.horizontalLayout.addWidget(self.netUsage)
        self.netDetailButton = QtGui.QPushButton(self.centralwidget)
        self.netDetailButton.setGeometry(QtCore.QRect(725, 222.5, 60, 27))
        self.netDetailButton.setObjectName(_fromUtf8("netDetailButton"))
        
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.detailButton = QtGui.QPushButton(self.centralwidget)
        self.detailButton.setGeometry(QtCore.QRect(635, 300, 150, 46))
        self.detailButton.setObjectName(_fromUtf8("detailButton"))        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 796, 38))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        # update usage
        self.ctimer = QtCore.QTimer()
        QtCore.QObject.connect(self.ctimer, QtCore.SIGNAL("timeout()"), self.updateUsage)
        self.ntimer = None
        
        # detail window extend
        self.w = None
        self.detailButton.clicked.connect(self.popExtend)
        
        # network detail window extend
        self.nw = None
        self.netDetailButton.clicked.connect(self.netPopExtend)
        
        global popMsg
        popMsg = Windows10_notification()
        
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        # set up initial value of every usage
        self.memUsage.setValue(memUsage())
        self.cpuUsage.setValue(cpuUsage())
        self.diskUsage.setText("Read: 0.0 bytes/s | Write: 0.0 bytes/s")
        self.netUsage.setText("Sent: 0.0 bytes/s | Recv: 0.0 bytes/s")

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.label.setText(_translate("MainWindow", "CPU usage:      ", None))
        self.label_3.setText(_translate("MainWindow", "Memory usage: ", None))
        self.label_2.setText(_translate("MainWindow", "Disk usage:      ", None))
        self.label_4.setText(_translate("MainWindow", "Network usage:", None))
        self.netUsage.setText(_translate("MainWindow", "TextLabel", None))
        self.netDetailButton.setText(_translate("MainWindow",">>>",None))
        self.detailButton.setText(_translate("MainWindow", "Detail >>>", None))
 
        # start ctimer
        self.ctimer.start(500)
        
    def updateUsage(self):
        global networkUsageList
        global diskUsageList
        global warnCountList
        global popMsg
        
        ## check overusing processes
        for pid in pu.pids():
            try:
                p = getProcess(pid)
                if warnCountList[pid][0] == 0 and getCPUusage(p) > 50:
                    warnCountList[pid][0] = 20
                    popMsg.show("CPU usage warning",p.name()+" spends a lot of cpu resource")
                elif getCPUusage(p) > 50:
                    warnCountList[pid][0] -= 1
                if warnCountList[pid][1] == 0 and getMemUsage(p) > 1024 * 1024 * 1024:
                    warnCountList[pid][1] = 20
                    popMsg.show("Memory usage warning",p.name()+" spends a lot of memory resource") 
                elif getMemUsage(p) > 1024 * 1024 * 1024:
                    warnCountList[pid][1] -= 1
            except KeyError:
                warnCountList[pid] = [0, 0]
            except pu.NoSuchProcess:
                del warnCountList[pid]
                
        self.memUsage.setValue(memUsage())
        self.cpuUsage.setValue(cpuUsage())
        diskUsageList = diskIOcountEachProcess()
        readTotal = 0
        writeTotal = 0
        for diskUsage in diskUsageList:
            readTotal += diskUsageList[diskUsage][0]
            writeTotal += diskUsageList[diskUsage][1]
        self.diskUsage.setText( "Read: "+humanize(readTotal)+"/s"+" | Write: "+humanize(writeTotal)+"/s" )
        networkUsageList = networkUsageEachDevice()
        sentTotal = 0
        recvTotal = 0
        for networkUsage in networkUsageList:
            sentTotal += networkUsage[1]
            recvTotal += networkUsage[2]
        self.netUsage.setText("Sent: "+humanize(sentTotal*2)+"/s | Recv: "+humanize(recvTotal*2)+"/s")

    def popExtend(self):
        self.w = DetailWindow()
        self.w.show()
       
    def netPopExtend(self):
        #self.nw = NetDetailWindow()
        #self.nw.show()
        self.nw = GraphicsWindow()
        
        # 3) Plot in chunks, adding one new plot curve for every 100 samples
        self.chunkSize = 10
        # Remove chunks after we have 10
        self.maxChunks = 20
        self.startTime = pyqtgraph.ptime.time()
        self.nw.nextRow()
        self.p5 = self.nw.addPlot(colspan=2)
        self.p5.setLabel('bottom', 'Time', 's')
        self.p5.setXRange(-10, 0)
        self.p5.setYRange(0,1000)
        self.p5.setMouseEnabled(x=False,y=False)
        self.p5.setMenuEnabled(False)
        self.p5.showGrid(x=True,y=True,alpha=0.5)
        self.curves = [[],[]]
        self.data5 = np.empty((self.chunkSize+1,3))
        self.ptr5 = 0
        self.ntimer = QtCore.QTimer()
        self.ntimer.timeout.connect(self.updateNetGraph)
        self.ntimer.start(500)
        
    def updateNetGraph(self):
        now = pyqtgraph.ptime.time()
        global networkUsageList
        netUsage = networkUsageList
        for c in self.curves[0]:
            c.setPos(-(now-self.startTime), 0)
        for c in self.curves[1]:
            c.setPos(-(now-self.startTime), 0)        
        
        i = self.ptr5 % self.chunkSize
        if i == 0:
            curve1 = self.p5.plot(pen=(0,2))
            self.curves[0].append(curve1)
            curve2 = self.p5.plot(pen=(1,2))
            self.curves[1].append(curve2)
            last = self.data5[-1]
            self.data5 = np.empty((self.chunkSize+1,3))        
            self.data5[0] = last
            while len(self.curves[0]) > self.maxChunks:
                c = self.curves[0].pop(0)
                self.p5.removeItem(c)
                d = self.curves[0].pop(0)
                self.p5.removeItem(d)
        else:
            curve1 = self.curves[0][-1]
            curve2 = self.curves[1][-1]
        self.data5[i+1,0] = now - self.startTime
        sentTotal = 0
        recvTotal = 0
        for networkUsage in networkUsageList:
            sentTotal += networkUsage[1]
            recvTotal += networkUsage[2]
        self.data5[i+1,1] = sentTotal*2/1024
        self.data5[i+1,2] = recvTotal*2/1024
        curve1.setData(x=self.data5[:i+2, 0], y=self.data5[:i+2, 1])
        curve2.setData(x=self.data5[:i+2, 0], y=self.data5[:i+2, 2])
        self.ptr5 += 1
                
class DetailWindow(QWidget): 
    def __init__(self): 
        QWidget.__init__(self) 
        # create table
        self.tabledata = []
        self.get_table_data()
        table = self.createTable() 
         
        # layout
        layout = QVBoxLayout()
        layout.addWidget(table) 
        self.setLayout(layout)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        
    def get_table_data(self):
        tabledata_ = getProcessResource()
        for pid in tabledata_:
            tabledata_[pid][1] = str(tabledata_[pid][1])+'%'
            tabledata_[pid][2] = humanize(tabledata_[pid][2])
            tabledata_[pid] = tabledata_[pid] + [ humanize(diskUsageList[ pid ][0])+'/s' ]
            tabledata_[pid] = tabledata_[pid] + [ humanize(diskUsageList[ pid ][1])+'/s' ]  
            self.tabledata.append( tabledata_[pid] )

    def createTable(self):
        # create the view
        tv = QTableView()

        # set the table model
        header = ['Name', 'Cpu', 'Memory', 'Disk Read', 'Disk Write']
        tm = DetailTableModel(self.tabledata, header, self) 
        tv.setModel(tm)

        # set the minimum size
        tv.setMinimumSize(1066, 800)

        # hide grid
        tv.setShowGrid(True)

        # set the font
        font = QFont("Gulim", 9)
        tv.setFont(font)

        # hide vertical header
        vh = tv.verticalHeader()
        vh.setVisible(False)

        # set horizontal header properties
        hh = tv.horizontalHeader()
        hh.setStretchLastSection(True)

        # set column width
        tv.setColumnWidth(0,300)
        tv.setColumnWidth(1,130)
        tv.setColumnWidth(2,200)
        tv.setColumnWidth(3,200)
        tv.setColumnWidth(4,200)
        
        # set row height
        nrows = len(self.tabledata)
        for row in xrange(nrows):
            tv.setRowHeight(row, 30)

        # enable sorting
        tv.setSortingEnabled(True)

        return tv
        
 
class DetailTableModel(QAbstractTableModel): 
    def __init__(self, datain, headerdata, parent=None, *args): 
        """ datain: a list of lists
            headerdata: a list of strings
        """
        QAbstractTableModel.__init__(self, parent, *args) 
        self.arraydata = datain
        self.headerdata = headerdata
        self.timer  = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update)     
        self.timer.start(1000)
 
    def rowCount(self, parent): 
        return len(self.arraydata) 
 
    def columnCount(self, parent): 
        return len(self.arraydata[0]) 
 
    def data(self, index, role):
        if not index.isValid(): 
            return QVariant() 
        elif role != QtCore.Qt.DisplayRole: 
            return QVariant()
        return QtCore.QVariant(self.arraydata[index.row()][index.column()]) 

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.headerdata[col])
        return QVariant()

    def sort(self, Ncol, order):
        """Sort table by given column number.
        """
        global sortedColNum
        global sortedOrder
        
        sortedColNum = Ncol
        sortedOrder = order
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        arraydata__ = getProcessResource()
        arraydata_ = []
        for pid in arraydata__:
            arraydata__[pid] = arraydata__[pid] + [ diskUsageList[ pid ][0] ]
            arraydata__[pid] = arraydata__[pid] + [ diskUsageList[ pid ][1] ]
            arraydata_.append( arraydata__[pid] )
        if Ncol == 0:
            self.arraydata = sorted(arraydata_, key=lambda s: s[Ncol].lower())
        else:
            self.arraydata = sorted(arraydata_, key=operator.itemgetter(Ncol))
        if sortedOrder == Qt.AscendingOrder:
            self.arraydata.reverse()
        
        for i in range(len(self.arraydata)):
            self.arraydata[i][1] = ("%3.1f" % self.arraydata[i][1])+'%'
            self.arraydata[i][2] = humanize(self.arraydata[i][2])
            self.arraydata[i][3] = humanize(self.arraydata[i][3])+'/s'  
            self.arraydata[i][4] = humanize(self.arraydata[i][4])+'/s'

        self.emit(SIGNAL("layoutChanged()"))
        
    def update(self):
        global sortedColNum
        
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        arraydata__ = getProcessResource()
        arraydata_ = []
        for pid in arraydata__:
            arraydata__[pid] = arraydata__[pid] + [ diskUsageList[ pid ][0] ]
            arraydata__[pid] = arraydata__[pid] + [ diskUsageList[ pid ][1] ]
            arraydata_.append( arraydata__[pid] )
        self.arraydata = arraydata_
        self.sort(sortedColNum,sortedOrder)
        self.emit(SIGNAL("layoutChanged()")) 

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    mainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())    
