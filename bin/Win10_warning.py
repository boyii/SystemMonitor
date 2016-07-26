from win32gui import *
import win32con
import sys, os
import struct
import time

class Windows10_notification:
    def __init__(self):
        message_map = {win32con.WM_DESTROY: self.OnDestroy,}
        # Register the notification class

        wc = WNDCLASS()
        self.hinst = wc.hInstance = GetModuleHandle(None)
        wc.lpszClassName = "WarningNotification"
        wc.lpfnWndProc = message_map
        # A pointer to the notification procedure.

        self.classAtom = RegisterClass(wc)
        # Create notification

    def show(self, title, msg):
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self.wwn = CreateWindow(self.classAtom, "Taskbar", style, 0, 0,
        win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT, 0, 0,
        self.hinst, None)

        UpdateWindow(self.wwn)

        iconPathName = os.path.abspath(os.path.join( sys.path[0], "balloontip.ico" ))
        icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE

        try:
            pico = LoadImage(self.hinst, iconPathName, win32con.IMAGE_ICON, 0, 0, icon_flags)
        except:
            pico = LoadIcon(0, win32con.IDI_APPLICATION)
        flags = NIF_ICON | NIF_MESSAGE | NIF_TIP
        nid = (self.wwn, 0, flags, win32con.WM_USER+20, pico, "tooltip")
        Shell_NotifyIcon(NIM_ADD, nid)
        Shell_NotifyIcon(NIM_MODIFY, (self.wwn, 0, NIF_INFO, win32con.WM_USER+20, pico, "Balloon tooltip",title,200,msg))

    def OnDestroy(self, wwn, msg, wparam, lparam):
        nid = (self.wwn, 0)
        Shell_NotifyIcon(NIM_DELETE, nid)
        PostQuitMessage(0)