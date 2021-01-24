import win32com.client as winAPI
import pythoncom

XINGAPI_PATH = '/eBEST/xingAPI/'

class XASessionEventHandler:
    login_state = 0

    def OnLogin(self, code, msg):
        if code == "0000":
            print("로그인 성공")
            XASessionEventHandler.login_state = 1
        else:
            print("로그인 실패")

#instXASession = win32com.client.DispatchWithEvents("XA_Session.XASession", XASessionEventHandler)
instXASession = winAPI.DispatchWithEvents("XA_Session.XASession", XASessionEventHandler)


id = "ksy4808"
passwd = "dhzp12!@"
cert_passwd = "dhzpqkfl1!@"

instXASession.ConnectServer("hts.ebestsec.co.kr", 20001)
instXASession.Login(id, passwd, cert_passwd, 0, 0)

while XASessionEventHandler.login_state == 0:
    pythoncom.PumpWaitingMessages()