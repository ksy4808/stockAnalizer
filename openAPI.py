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


class openAPI():
    def __init__(self, _upper):
        self._u = _upper
        self.kiwoom = QAxWidget(
            "KHOPENAPI.KHOpenAPICtrl.1")  # 키움증권 Open API+의 ProgID를 사용하여 생성된 QAxWidget을 kiwoom 변수에 할당

        self.kiwoom.OnEventConnect.connect(self.event_connect)  # 키움 서버 접속 관련 이벤트가 발생할 경우 event_connect 함수 호출
        self.kiwoom.OnReceiveTrData.connect(self.receive_trdata)  # 키움 데이터 수신 관련 이벤트가 발생할 경우 receive_trdata 함수 호출
        return
    def event_connect(self, err_code):
        if err_code == 0:  # err_code가 0이면 로그인 성공 그외 실패
            self._u.isLogin.setText("로그인 됨")  # ui 파일을 생성할때 작성한 plainTextEdit의 objectName 으로 해당 plainTextEdit에 텍스트를 추가함
            self._u.btnLogin.setDisabled(True)  # 로그인 버튼을 비활성화 상태로 변경
        else:
            self._u.isLogin.setText("로그오프 상태")  # ui 파일을 생성할때 작성한 plainTextEdit의 objectName 으로 해당 plainTextEdit에 텍스트를 추가함
            self._u.btnLogin.setDisabled(False)  # 로그인 버튼을 활성화 상태로 변경
        return
    def receive_trdata(self, screen_no, rqname, trcode, recordname, prev_next, data_len, err_code, msg1, msg2):  # 키움 데이터 수신 함수
        return
    def login_btn(self):
        ret = self.kiwoom.dynamicCall("CommConnect()")  # 키움 로그인 윈도우를 실행
        return