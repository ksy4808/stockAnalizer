import os
import sys
from pyxing.session import *

from PyQt5.QtWidgets import *
from PyQt5 import uic
import win32com.client
import pythoncom






form_class = uic.loadUiType('xingAPI.ui')[0]


class XASessionEvents:
    상태 = False

    def OnLogin(self, code, msg):
        print("OnLogin : ", code, msg)
        XASessionEvents.상태 = True

    def OnLogout(self):
        print('--------------------')
        pass

    def OnDisconnect(self):
        print('=====================')
        pass
class XASessionEventHandler:
    login_state = 0

    def OnLogin(self, code, msg):
        if code == "0000":
            print("로그인 성공")
            XASessionEventHandler.login_state = 1
        else:
            print("로그인 실패")

instXASession = win32com.client.DispatchWithEvents("XA_Session.XASession", XASessionEventHandler)

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # ui 파일 화면 출력
        self.login()
    def login(self):
        id = "ksy4808"
        passwd = "dhzp12!@"
        cert_passwd = "dhzpqkfl1!@"
        instXASession.ConnetcServer("htx.ebestsec.co.kr",20001)
        instXASession.Login(id, passwd, cert_passwd, 0, 0)
        while XASessionEventHandler.login_state == 0:
            pythoncom.PumpWaitingMessages()
        return

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywindow = MyWindow()
    mywindow.show()
    app.exec_()


