import wmi
import psutil as pu
import os
from collections import namedtuple

networkTuple = namedtuple('networkTuple', 'device, sent, recv, pkg_sent, pkg_recv')

def memUsageEachProcess():
    for id in .pids():
        p = pu.Process(id)
        mem = p.memory_info()[0]/float(2**20)
        total+=mem
        print p.name(), mem


def diskUsageEachDisk():
    c = wmi.WMI()

    for d in c.Win32_LogicalDisk():
        try:
            print( d.Caption, str(100-float(int(d.FreeSpace))/float(int(d.Size))*100.0)[:5]+'%',str(float(int(d.Size)-int(d.FreeSpace))/2**30)[:5]+" gb / "+str(float(int(d.Size))/2**30)[:5]+" gb")
        except:
            print( d.Caption, d.FreeSpace, d.Size )

def diskUsage():
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

def memUsage():
    return pu.virtual_memory()[2]

def cpuUsage():
    return pu.cpu_percent()

def NetworkUsage():
    networks = list()
    for k,v in pu.net_io_counters(pernic=True).items():
        if k == 'lo':
            continue

        networks.append(
            networkTuple(
                device = k,
                sent = humanize(v.bytes_sent),
                recv = humanize(v.bytes_recv),
                pkg_sent = v.packets_sent,
                pkg_recv = v.packets_recv
            )
        )

def humanize(num):
    for x in ['bytes', 'KB', 'MB', 'GB']:
        if num < 1024.0:
            return "%3.1f%s" % (num, x)
        num /= 1024.0
    return "%3.1f%s" % (num, 'TB')
