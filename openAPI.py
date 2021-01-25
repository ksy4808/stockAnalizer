import sys
import os
import openpyxl
import sqlite3
import datetime
import threading
import time
from openpyxl import Workbook
from random import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QAxContainer import *
from time import sleep
from threading import Lock


from PyQt5.QAxContainer import *
from PyQt5.QtCore import *


class openAPI():
    def __init__(self, _upper):
        self._u = _upper
        self.opt10015Proc = False
        self.opt10081Proc = True
        self.opt10015TrData = []
        self.opt10081TrData = []

        self.kiwoom = QAxWidget(
            "KHOPENAPI.KHOpenAPICtrl.1")  # 키움증권 Open API+의 ProgID를 사용하여 생성된 QAxWidget을 kiwoom 변수에 할당

        self.kiwoom.OnEventConnect.connect(self.event_connect)  # 키움 서버 접속 관련 이벤트가 발생할 경우 event_connect 함수 호출
        self.kiwoom.OnReceiveTrData.connect(self.receive_trdata)  # 키움 데이터 수신 관련 이벤트가 발생할 경우 receive_trdata 함수 호출
        return
    def isLogon(self):
        if self._u.isLogin.text() == "로그인 됨":
            return True
        else:
            return False
    def event_connect(self, err_code):
        if err_code == 0:  # err_code가 0이면 로그인 성공 그외 실패
            self._u.isLogin.setText("로그인 됨")  # ui 파일을 생성할때 작성한 plainTextEdit의 objectName 으로 해당 plainTextEdit에 텍스트를 추가함
            self._u.btnLogin.setDisabled(True)  # 로그인 버튼을 비활성화 상태로 변경
        else:
            self._u.isLogin.setText("로그오프 상태")  # ui 파일을 생성할때 작성한 plainTextEdit의 objectName 으로 해당 plainTextEdit에 텍스트를 추가함
            self._u.btnLogin.setDisabled(False)  # 로그인 버튼을 활성화 상태로 변경
        return
    def receive_trdata(self, screen_no, rqname, trcode, recordname, prev_next, data_len, err_code, msg1, msg2):  # 키움 데이터 수신 함수
        if prev_next == '2':
            self.remained_data = True
        else:
            self.remained_data = False

        if rqname == "opt10015_req":
            self._opt10015(rqname, trcode)
            self.opt10015Proc = False
        elif rqname == "opt10081_req":
            self._opt10081(rqname, trcode)
            self.opt10081Proc = False

        self.tr_event_loop.exit()
        return
    def login_btn(self):
        ret = self.kiwoom.dynamicCall("CommConnect()")  # 키움 로그인 윈도우를 실행
        return
    def _opt10081(self, rqname, trcode):
        data_cnt = self.kiwoom.dynamicCall("GetRepeatCnt(QString, QString)", trcode, rqname)
        총일봉 = []
        for i in range(0, data_cnt):
            일자별데이터 = []
            일자 = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname,
                                           i, "일자")
            현재가 = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname,
                                           i, "현재가")
            거래량 = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname,
                                          i, "거래량")
            거래대금 = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname,
                                           i, "거래대금")
            시가 = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname,
                                           i, "시가")
            고가 = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname,
                                           i, "고가")
            저가 = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname,
                                           i, "저가")
            수정주가구분 = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname,
                                         i, "수정주가구분")
            수정비율 = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname,
                                         i, "수정비율")
            일자별데이터.append(일자.strip())
            일자별데이터.append(현재가.strip())
            일자별데이터.append(거래량.strip())
            일자별데이터.append(거래대금.strip())
            일자별데이터.append(고가.strip())
            일자별데이터.append(저가.strip())
            일자별데이터.append(수정주가구분.strip())
            일자별데이터.append(수정비율.strip())
            총일봉.append(일자별데이터)
            self.opt10081TrData = 총일봉
        return
    def _opt10015(self, rqname, trcode):
        data_cnt = self.kiwoom.dynamicCall("GetRepeatCnt(QString, QString)", trcode, rqname)
        for i in range(0, data_cnt):
            일자 = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname,
                                           i, "일자")  # 일자에 해당하는 string을 read
            종가 = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "",
                                                    rqname, i, "종가")  # 종가에 해당하는 string을 read
            전일대비기호 = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "",
                                                   rqname, i, "전일대비기호")  # 전일대비기호에 해당하는 string을 read
            전일대비 = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "",
                                      rqname, i, "전일대비")  # 전일대비기호에 해당하는 string을 read
            등락율 = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "",
                                      rqname, i, "등락율")  # 전일대비기호에 해당하는 string을 read
            거래량 = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "",
                                      rqname, i, "거래량")  # 전일대비기호에 해당하는 string을 read
            거래대금 = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "",
                                      rqname, i, "거래대금")  # 전일대비기호에 해당하는 string을 read
            장전거래량 = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "",
                                      rqname, i, "장전거래량")  # 전일대비기호에 해당하는 string을 read
            장전거래비중 = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "",
                                      rqname, i, "장전거래비중")  # 전일대비기호에 해당하는 string을 read
            장중거래량 = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "",
                                      rqname, i, "장중거래량")  # 전일대비기호에 해당하는 string을 read
            장중거래비중 = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "",
                                      rqname, i, "장중거래비중")  # 전일대비기호에 해당하는 string을 read
            장후거래량 = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "",
                                      rqname, i, "장후거래량")  # 전일대비기호에 해당하는 string을 read
            장후거래비중 = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "",
                                      rqname, i, "장후거래비중")  # 전일대비기호에 해당하는 string을 read


    def reqOpt10015(self, item, code, startDate, endDate):
        self.opt10015Proc = True
        endDateStr = str(endDate).replace("-", "")#마지막 날짜부터 역으로 받아오기때문에 endDate를 날짜로 넘긴다.
        self.set_input_value("종목코드", code)
        self.set_input_value("시작일자", endDateStr)
        self.comm_rq_data("opt10015_req", "opt10015", 0, "0101")

    def reqOpt10081(self, code, endDate, revisedPrice):
        self.opt10081Proc = True
        endDateStr = str(endDate).replace("-", "")#마지막 날짜부터 역으로 받아오기때문에 endDate를 날짜로 넘긴다.
        self.set_input_value("종목코드", code)
        self.set_input_value("기준일자", endDateStr)
        self.set_input_value("수정주가구분", str(revisedPrice))
        self.comm_rq_data("opt10081_req", "opt10081", 0, "0101")
        return

    def comm_rq_data(self, rqname, trcode, next, screen_no):
        self.kiwoom.dynamicCall("CommRqData(QString, QString, int, QString)", rqname, trcode, next, screen_no)
        self.tr_event_loop = QEventLoop()
        self.tr_event_loop.exec_()
        return

    def set_input_value(self, id, value):
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", id, value)