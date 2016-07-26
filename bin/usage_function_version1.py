import wmi
import psutil as pu
import os
from collections import namedtuple
from Win10_warning import Windows10_notification

processList = {}
prevProcessDiskIOList = {}
prevDeviceNetList = {}

def diskAmountEachDisk():
    c = wmi.WMI()
    for d in c.Win32_LogicalDisk():
        try:
            print( d.Caption, str(100-float(int(d.FreeSpace))/float(int(d.Size))*100.0)[:5]+'%',str(float(int(d.Size)-int(d.FreeSpace))/2**30)[:5]+" gb / "+str(float(int(d.Size))/2**30)[:5]+" gb")
        except:
            print( d.Caption, d.FreeSpace, d.Size )

def diskAmount():
    c = wmi.WMI()
    total=0
    usage=0
    for d in c.Win32_LogicalDisk():
        try:
            total += int( d.Size )
            usage += int( d.Size ) - int( d.FreeSpace )
        except:
            if d.Size is None:
                total += 0
            else:
                total += int( d.Size )
    return float(str(usage/float(total)*100)[:5])


def cpuUsage():
    return pu.cpu_percent()

def getCPUusage(p):
    try:
        return p.cpu_percent() / pu.cpu_count()
    except pu.NoSuchProcess:
        return 0

def memUsage():
    return pu.virtual_memory()[2]

def getMemUsage(p):
    return p.memory_info()[0]

def memUsageEachProcess():
    memUsageList = []
    for pid in pu.pids():
        memUsageList.append([pid, getMemUsage(pid)])
    return memUsageList

"""
def diskIOcount():
    totalRead = 0
    totalWrite = 0
    for diskIOcount in diskIOcountEachProcess():
        totalRead += diskIOcount[1][0]
        totalWrite += diskIOcount[1][1]
    return totalRead, totalWrite
"""

def getDiskIOcount(p):
    diskIOcount = p.io_counters()
    diskRPS = diskIOcount[2] - prevProcessDiskIOList[p.pid][0]
    diskWPS = diskIOcount[3] - prevProcessDiskIOList[p.pid][1]
    prevProcessDiskIOList[p.pid][0] = diskIOcount[2]
    prevProcessDiskIOList[p.pid][1] = diskIOcount[3]
    return [diskRPS, diskWPS]

def diskIOcountEachProcess():
    diskIOcountList = {}
    for pid in pu.pids():
        try:
            p = getProcess(pid)
            diskIOcountList[pid] = getDiskIOcount(p)
        except pu.NoSuchProcess:
            deleteProcess(pid)
    return diskIOcountList
    
def networkUsageEachDevice():
    networkUsageList = list()
    for k, v in pu.net_io_counters(pernic = True).items():
        if k == 'lo':
            continue
        try:
            networkUsageList.append([k, v.bytes_sent - prevDeviceNetList[k][0], v.bytes_recv - prevDeviceNetList[k][1]])
            prevDeviceNetList[k] = [v.bytes_sent, v.bytes_recv]
        except KeyError:
            networkUsageList.append([k, 0, 0])
            prevDeviceNetList[k] = [v.bytes_sent, v.bytes_recv]

    return networkUsageList

def getProcessResource():
    global warnCount
    global popMsg
    
    processResourceList = {}
 
    for pid in pu.pids():
        try:
            p = getProcess(pid)
            diskIOcount = getDiskIOcount(p)
            cpu = getCPUusage(p)
            processResourceList[pid] = [p.name(),
                                        cpu,
                                        getMemUsage(p)]            
            
        except pu.NoSuchProcess:
            continue
    return processResourceList

def getProcess(pid):
    found = False
    try:
        p = processList[pid]
    except KeyError:
        p = pu.Process(pid)
        processList[pid] = p
        diskIOcount = p.io_counters()
        prevProcessDiskIOList[pid] = [diskIOcount[2], diskIOcount[3]]
    return p

def deleteProcess(pid):
    try:
        del processList[pid]
        del prevProcessDiskIOList[pid]
    except KeyError:
        pass


            
def humanize(num):
    for x in [' bytes', ' KB', ' MB', ' GB']:
        if num < 1024.0:
            return "%3.1f%s" % (num, x)
        num /= 1024.0
    return "%3.1f%s" % (num, ' TB')