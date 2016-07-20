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
        self.ctimer.start(1000)
        
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
                    warnCountList[pid][0] = 10
                    popMsg.show("CPU usage warning",p.name()+" spends a lot of cpu resource")
                elif getCPUusage(p) > 50:
                    warnCountList[pid][0] -= 1
                if warnCountList[pid][1] == 0 and getMemUsage(p) > 1024 * 1024 * 1024:
                    warnCountList[pid][1] = 10
                    popMsg.show("Memory usage warning",p.name()+" spends a lot of memory resource") 
                elif getMemUsage(p) > 1024 * 1024 * 1024:
                    warnCountList[pid][1] -= 1
            except KeyError:
                print "Add process"                
                warnCountList[pid] = [0, 0]
            except pu.NoSuchProcess:
                print "process was dead"
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
        self.netUsage.setText("Sent: "+humanize(sentTotal)+"/s | Recv: "+humanize(recvTotal)+"/s")
        

    def popExtend(self):
        self.w = DetailWindow()
        self.w.show()
       
    def netPopExtend(self):
        self.nw = NetDetailWindow()
        self.nw.show()

class NetDetailWindow(QWidget): 
    def __init__(self): 
        QWidget.__init__(self) 
        # create table
        self.get_table_data()
        table = self.createTable() 
         
        # layout
        layout = QVBoxLayout()
        layout.addWidget(table) 
        self.setLayout(layout)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        

    
    def get_table_data(self):
        self.tabledata = copy.deepcopy(networkUsageList)
        for i in range(len(self.tabledata)):
            self.tabledata[i][1] = humanize(self.tabledata[i][1])+'/s'
            self.tabledata[i][2] = humanize(self.tabledata[i][2])+'/s'

    def createTable(self):
        # create the view
        tv = QTableView()

        # set the table model
        header = ['Name', 'Sent', 'Recv']
        tm = NetDetailTableModel(self.tabledata, header, self) 
        tv.setModel(tm)

        # set the minimum size
        tv.setMinimumSize(800, 400)

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
        tv.setColumnWidth(1,200)
        tv.setColumnWidth(2,200)
        
        # set row height
        nrows = len(self.tabledata)
        for row in xrange(nrows):
            tv.setRowHeight(row, 30)

        # enable sorting
        tv.setSortingEnabled(True)

        return tv
    
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
        

        
class NetDetailTableModel(QAbstractTableModel): 
    def __init__(self, datain, headerdata, parent=None, *args): 
        """ datain: a list of lists
            headerdata: a list of strings
        """
        QAbstractTableModel.__init__(self, parent, *args) 
        self.arraydata = datain
        self.headerdata = headerdata
        self.timer  = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update)     
        self.timer.start(200)
 
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
        global netSortedColNum
        global netSortedOrder
        
        netSortedColNum = Ncol
        netSortedOrder = order
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        arraydata_ = copy.deepcopy(networkUsageList)
        if Ncol == 0:
            self.arraydata = sorted(arraydata_, key=lambda s: s[Ncol].lower())
        else:
            self.arraydata = sorted(arraydata_, key=operator.itemgetter(Ncol))
        if netSortedOrder == Qt.AscendingOrder:
            self.arraydata.reverse()  
        for i in range(len(self.arraydata)):
            self.arraydata[i][1] = humanize(self.arraydata[i][1])+'/s'
            self.arraydata[i][2] = humanize(self.arraydata[i][2])+'/s'
        self.emit(SIGNAL("layoutChanged()"))
        
    def update(self):
        global netSortedColNum
        global netSortedOrder
        
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.arraydata = copy.deepcopy(networkUsageList)
        self.sort(netSortedColNum,netSortedOrder)
        self.emit(SIGNAL("layoutChanged()")) 


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    mainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())    
