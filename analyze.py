import os
import sys
import datetime
import sqlite3
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from mpl_toolkits.mplot3d import Axes3D


from pandas import Series, DataFrame

import multiprocessing as mp
from PyQt5.QtWidgets import *
from PyQt5 import QtGui

from PyQt5 import uic
from PyQt5.QtCore import QDate
from PyQt5.QtCore import pyqtSlot, Qt

import datetime as dt
from datetime import timedelta
from PyQt5.QtCore import QStringListModel
from multiprocessing import Pool
from os import getpid
import ItemSort
import threading
import time
import os.path

import ksyUtil
import ksyUi
from model import getFromLocalDB as getLocalDB
import openAPI

form_class = uic.loadUiType('analyze.ui')[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.w = None
        self.setupUi(self)

        #ui관련 객체 초기화
        self.Text = ksyUi.Text(self)
        self.graph = ksyUi.graph(self)
        self.eventSet = ksyUi.eventSet(self)
        self.input = ksyUi.input(self)

        #utility 관련 객체 초기화
        self.util = ksyUtil.Util()
        util = self.util

        #model 관련 객체 초기화
        self.model = getLocalDB()

        #메인 windows display초기화
        self.Text.displayInit()

        #openAPI를 사용하기 위한 객체 초기화
        self.openApi = openAPI.openAPI(self)

        #스위치 이벤트를 mathod에 연결한다.
        self.concludeByItematDate.clicked.connect(self.ConcludeBy_ItematDate)
        self.reArrange.clicked.connect(self.re_arrange)
        self.concluionDetail.clicked.connect(self.ConcludeBy_custom)

        #체결정보 테이블 그리기 최초 프로그램실행시 설정되어있는 날짜와 종목의 체결정보를 표시한다.
        #self.dispConcludeTable()

        #메뉴바에서 관심종목 항목 선택시 이벤트 연결
        self.call_Itemsort.triggered.connect(run_subProcItemSort)

        self.lineEdit_second.setValidator(QtGui.QIntValidator(1,9999,self))#0초 부터 9999초까지 설정가능 범위로 한다.

        #graphCall = graphConclude(self)#생성할 class에 자신을 넘겨줌으로써 생성된 class에서 mainwindow를 바로 사용할수 있게 한다.

    def reqLogin(self):
        self.openApi.login_btn()
        return

    def ConcludeBy_custom(self):
        return
    def re_arrange(self):
        util = self.util
        datestr = util.getDateForFileName(self)
        discardFirstConc = True

        item = self.item_comboBox.currentText()
        con = sqlite3.connect("../conclusions/" + datestr + ".db")
        cur = con.cursor()
        cur.execute("select * from %s;" % item)
        rows = cur.fetchall()
        con.close()
        startTimeWindowStr = "090000"
        endTimeWindowStr = "153000"

        dateFormatter = "%Y_%m_%d %H%M%S"
        x = datestr+" "+startTimeWindowStr
        startTimeWindow = dt.datetime.strptime(x, dateFormatter)

        if self.lineEdit_second.text() == "":
            deltaSeconds = 0
        else:
            deltaSeconds = int(self.lineEdit_second.text())
        endTimeWindow = startTimeWindow + dt.timedelta(seconds=deltaSeconds)
        arrangeSet = []
        valueAccumulate = 0
        quantityAccumulate = 0
        j = 0
        for i in range(len(rows)):
            x = datestr + " " + endTimeWindowStr
            if startTimeWindow >= dt.datetime.strptime(x, dateFormatter):
                break
            rowsOffset = len(rows)-1-i
            row = rows[rowsOffset]
            x = datestr + " " + row[1]
            curTime = dt.datetime.strptime(x, dateFormatter)
            if curTime < startTimeWindow:#최초 시작 시간보다 앞선 경우 처리하지 않고 넘긴다.(장중 데이터만 처리하는데 개장 전 데이터는 무시하기 위함.
                continue
            elif curTime >= startTimeWindow and curTime < endTimeWindow:#현재 데이터가 time window내에 있는경우 accumulate한다.
                if discardFirstConc == True:#장 개시하고 최초 거래는 단일가 거래기 때문에 금액이 크고, 큰손 매도인지 매수인지 알 수 없으므로 무시한다.
                    discardFirstConc = False
                else:
                    valueAccumulate += int(row[4])
                    quantityAccumulate += int(row[3])
            else:#현재 데이터가 time window끝보다 크면 이전 accumulate했던 값을 startTimeWindow시점에 기록하고 새로 accumulate한다.
                arrangeUnit = []#여기서 생성을 해야 2차원리스트로 삽입이 됨.
                arrangeUnit.append(j)
                j += 1
                arrangeUnit.append(startTimeWindow.time())
                if self.lineEdit_TransVolume.text() == "":  # 기준금액이 비어있으면 모두 sum
                    arrangeUnit.append(valueAccumulate)
                    arrangeUnit.append(quantityAccumulate)
                elif abs(valueAccumulate) >= int(self.lineEdit_TransVolume.text()): #기준금액이 채워져있으면 sum한 금액이 기준금액보다 큰 경우 append
                    arrangeUnit.append(valueAccumulate)
                    arrangeUnit.append(quantityAccumulate)
                else:#기준금액보다 작으면 0을 append
                    arrangeUnit.append(0)
                    arrangeUnit.append(0)

                arrangeSet.append(arrangeUnit)
                valueAccumulate = 0
                quantityAccumulate = 0
                if discardFirstConc == True:#장 개시하고 최초 거래는 단일가 거래기 때문에 금액이 크고, 큰손 매도인지 매수인지 알 수 없으므로 무시한다.
                    discardFirstConc = False
                else:
                    valueAccumulate += int(row[4])
                    quantityAccumulate += int(row[3])

                startTimeWindow = endTimeWindow
                endTimeWindow = startTimeWindow + dt.timedelta(seconds=deltaSeconds)
                if curTime >= endTimeWindow:#현재 체결시간이 shift한 time Window보다 크면 time Window를 더 shift해야한다.
                    while curTime >= endTimeWindow:#현재 데이터의 시간이 time window안에 들어올때까지 time window를 shift한다.
                        arrangeUnit = []  # 여기서 생성을 해야 2차원리스트로 삽입이 됨.
                        arrangeUnit.append(j)
                        j += 1
                        arrangeUnit.append(startTimeWindow)
                        arrangeUnit.append(0)#체결금액 0으로 clear
                        arrangeUnit.append(0)#체결량 0으로 clear
                        arrangeSet.append(arrangeUnit)
                        # 현재 데이터의 시간까지 도달하기 전까지는 time window의 값을 0으로 채운다.
                        startTimeWindow = endTimeWindow
                        endTimeWindow = startTimeWindow + dt.timedelta(seconds=deltaSeconds)
        j = 0
        for i, row in enumerate(arrangeSet, 0):
            if row[3] != 0:#기준 금액 이상의 거래가 있는 경우만 표시하도록 함. 안그러면 평균가 계산할때 0 나누기때문에 에러남.
                j += 1
        self.concTableWidget_2.setColumnCount(3)
        self.concTableWidget_2.setRowCount(j)#기준금액을 넘는 경우만 리스트에 표시
        self.concTableWidget_2.setHorizontalHeaderLabels(["시간", "체결금액", "체결평균가"])

        Transe_Volume_sum = 0
        j = 0
        firstconclude = 1
        for i, row in enumerate(arrangeSet, 0):
            insertTime = QTableWidgetItem(str(row[1]))
            insertPrice = QTableWidgetItem(str(format(row[2],",")))
            insertTime.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
            insertPrice.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
            if row[3] != 0:#기준 금액 이상의 거래가 있는 경우만 표시하도록 함. 안그러면 평균가 계산할때 0 나누기때문에 에러남.
                mean = int(row[2]/row[3])
                insertmean = QTableWidgetItem(str(format(mean, ",")))
                insertmean.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
                self.concTableWidget_2.setItem(j, 0, insertTime)
                self.concTableWidget_2.setItem(j, 1, insertPrice)
                self.concTableWidget_2.setItem(j, 2, insertmean)
                j += 1
                Transe_Volume_sum += row[2]

        self.lineEdit_TransVolume_sum.setText(str(format(Transe_Volume_sum,",")))

    def reqConcInfoByItem(self):
        util = self.util
        date = util.getDateForFileName(self)
        item = self.item_comboBox.currentText()
        if item == "":#콤보박스가 비어있는경우임.
            rows = self.model.getAllItemList(date)
            if None != rows:
                item = self.util.getPureText(rows[0])
                rows = self.model.getConcInfoByItem(date, item)
                self.item_comboBox.setEditText(item)
                self.Text.dispComboBox()
                return rows
            else:
                return None

        rows = self.model.getConcInfoByItem(date, item)
        if rows == None:#콤보박스에 아이템은 있는데 실제 DB에 종목이 없는경우 있는 종목중 제일 앞의 종목을 표시한다.
            rows = self.model.getAllItemList(date)
            if rows == None:#DB도 없는경우 return None
                return None
            item = self.util.getPureText(rows[0])
            rows = self.model.getConcInfoByItem(date, item)
            self.item_comboBox.setEditText(item)

        return rows

    def ConcludeBy_ItematDate(self):
        util = self.util
        datestr = util.getDateForFileName(self)
        item = self.item_comboBox.currentText()
        con = sqlite3.connect("../conclusions/" + datestr + ".db")
        cur = con.cursor()
        cur.execute("select * from %s;" %item)
        rows = cur.fetchall()
        con.close()
        y_data = []
        x_data = []
        dateFormatter = "%Y_%m_%d %H%M%S%f"
        prevCnt = 0
        x_prev = 0
        for i, row in enumerate(rows, 0):
            y_data.insert(0, int(row[4]))
            x = row[1]
            if x == x_prev:
                prevCnt -= 1
            else:
                prevCnt = 1000
            x_prev = x
            x = datestr+" "+x+str(prevCnt).zfill(6)
            time = dt.datetime.strptime(x, dateFormatter)
            x_data.insert(0, time)
        plt.plot_date(x_data,y_data,linestyle="-",marker=".")
        plt.show()

    def reqGetDateForFileName(self):
        util = self.util
        return util.getDateForFileName(self)

    def TrendReqModel(self, startDate, endDate, item, baseAmount, reqUnit, reqWindow):

        days = (endDate - startDate).days + 1  # 시작날짜와 종료날짜를 포함해야하므로 1을 더함.
        #Item의 체결정보를 시작 날짜부터 끝 날짜까지 모두 가지고 온다.
        SegAllDays = self.model.reqTotalConcInfo(item, startDate, endDate)
        #dispLists: 기간동안 거래내역이 있는 날짜의 거래내역에서 time window별로 거래내역을 모아서 정리한 리스트
        dispLists = self.setPeriodBaseConc(SegAllDays, startDate, endDate, baseAmount, reqUnit, reqWindow)
        sortedDispList = self.sortDispList(dispLists, baseAmount)#기준금액에 미달하는 리스트는 제거한다.
        if reqUnit == "day":
            sumedTotalConcludeResurt = self.sumTotalConcludePerADay(sortedDispList)#기준금액이상의 체결정보를 날짜별로 sum
        elif reqUnit == "week":
            sumedTotalConcludeResurt = self.sumTotalConcludePerAWeek(sortedDispList)#기준금액이상의 체결정보를 날짜별로 sum
        elif reqUnit == "month":
            sumedTotalConcludeResurt = self.sumTotalConcludePerAMonth(sortedDispList)#기준금액이상의 체결정보를 날짜별로 sum
        self.graph.plotConcGraph(sumedTotalConcludeResurt)
        if self.openApi.isLogon() == True:#로그인 된 경우에만 아래 루틴 실행.
            """
            code = self.model.reqCodeByItem(item)
            self.openApi.reqOpt10015(item, code, startDate, endDate)
            while self.openApi.opt10015Proc == True:
                continue
            self.graph.plotTrHistory(self.openApi.opt10015TrData)
            """
            code = self.model.reqCodeByItem(item)
            revisePrice = 1#0이면 단순 당시 가격, 1이면 수정주가
            self.openApi.reqOpt10081(code, endDate, revisePrice)
            while self.openApi.opt10081Proc ==True:
                continue
            self.graph.plotTrHistory(self.openApi.opt10081TrData)

        return

    def sumTotalConcludePerADay(self, sortedDispList):
        isFirstDate = True
        retVal = []
        for calcUnit in sortedDispList:
            if(isFirstDate == True):#날짜별 체결정보 sum하는 동작에서 제일 첫 날짜
                isFirstDate = False
                curDate = dt.datetime.date(calcUnit[0])
                concAccList = []
                concAccList.append(curDate)
                concAcc = 0
                numAcc = 0
                concAcc += calcUnit[2]
                numAcc += calcUnit[1]
            elif curDate != dt.datetime.date(calcUnit[0]):#날짜가 바뀐경우 새로 sum을 하기 위해 리스트 초기화
                concAccList.append(numAcc)
                concAccList.append(concAcc)
                retVal.append(concAccList)#sub한 list를 append한다.
                curDate = dt.datetime.date(calcUnit[0])
                concAccList = []#새로운 리스트로 저장하기 위해 list를 새로 초기화
                concAccList.append(curDate)
                concAcc = 0
                numAcc = 0
                concAcc += calcUnit[2]
                numAcc += calcUnit[1]
            else:#이전 리스트와 같은 날짜인 경우 체결정보 Sum
                concAcc += calcUnit[2]
                numAcc += calcUnit[1]
                continue
        concAccList.append(numAcc)
        concAccList.append(concAcc)
        #마지막 acc한 데이터 append해야함.
        retVal.append(concAccList)
        return retVal


    def sumTotalConcludePerAWeek(self, sortedDispList):

        return

    def sumTotalConcludePerAMonth(self, sortedDispList):

        return

    def sortDispList(self, dispLists, baseAmount):
        retList = []
        for day in dispLists:
            for concUnit in day:
                if abs(int(concUnit[2])) > int(baseAmount):##기준금액 이상인 경우 append
                    retList.append(concUnit)
        return retList

    def setPeriodBaseConc(self, SegAllDays, startDate, endDate, baseAmount, reqUnit, reqWindow):
        retList = []
        startTimeWindowStr = "090000"
        endTimeWindowStr = "153000"
        dateFormatter = "%Y-%m-%d%H%M%S"
        startTime = dt.datetime.strptime(str(startDate) + startTimeWindowStr, dateFormatter)
        endTime = dt.datetime.strptime(str(startDate) + endTimeWindowStr, dateFormatter)
        accTimeWindow = reqWindow#default 1초로 설정한다. 나중엔 window를 변경하는하도록 할때 해당 변수를 수정한다
        for rows in SegAllDays:#SegAllDays: 해당 아이템의 startDate~endDate까지 모든 체결정보
            accForOneDay = []
            startTime = dt.datetime.strptime(str(startDate) + startTimeWindowStr, dateFormatter)
            endTime = dt.datetime.strptime(str(startDate) + endTimeWindowStr, dateFormatter)
            if rows == []:#주말등의 이유로 해당 날짜 데이터가 없는경우 그냥 넘긴다.
                startDate = startDate + dt.timedelta(days=1)
                continue
            if startDate <= endDate:
                #retList.append(startDate)
                totalRows = len(rows)
                firstConclude = True  # 9시 이후 제일 첫 거래는 단일가거래기 때문에 매수인지 매도인지 알 수 없으므로 무시하기 위한 flag
                frontWindow = dt.datetime.combine(startDate, dt.time(hour=9, minute=0, second=0))
                tailWindow = frontWindow + dt.timedelta(seconds=accTimeWindow)
                timeStamp = frontWindow
                accConclude = 0  # timewindow내의 체결 금액을 sum 하기 위한 변수
                accConcludeQty = 0  # timewindow내의 체결량을 sum 하기 위한 변수
                for i in range(totalRows):
                    row = rows[totalRows - i - 1]#rows: 해당 아이템의 날짜별 해당 일자의 모든 체결정보, 정배열 시간으로 확인하기 위해 뒤에서부터 처리.
                    dateFormatter = "%Y-%m-%d%H%M%S"
                    curTime = dt.datetime.strptime(str(startDate) + row[1], dateFormatter)
                    if curTime < startTime or curTime > endTime:#9시 이전의 데이터와 3시 30분 이후 데이터는 무시한다.
                        continue
                    if firstConclude == True and curTime > frontWindow:
                        firstConclude = False  # 9시 이후 제일 첫 거래는 단일가거래기 때문에 매수인지 매도인지 알 수 없으므로 무시하기 위한 flag clear
                        continue
                    if curTime >= frontWindow and curTime < tailWindow:
                        accConclude += int(row[4])
                        accConcludeQty += int(row[3])
                    if curTime >= tailWindow:#현재 시간이 timewindow를 벗어나므로 window를 shift해야함.
                        while curTime >= tailWindow:#현재시간이 timeWindow내에 들어올 때 까지 window를 shift한다.
                            frontWindow = tailWindow
                            tailWindow = frontWindow + dt.timedelta(seconds=accTimeWindow)
                            accRow = []
                            accRow.append(timeStamp)#1차원 배열
                            accRow.append(accConcludeQty)
                            accRow.append(accConclude)
                            accForOneDay.append(accRow)  # 계산할 window내에 있는 모든 거래 내역을 하나의 리스트로 정리 2차원배열
                            timeStamp = frontWindow
                            accConcludeQty = 0
                            accConclude = 0
                        #timestamp를 이용하여 현재까지 누적된 체결 량을 append한다.
                        accConclude = int(row[4])#체결정보 sum 값을 append한 다음엔 현재 체결 정보를 누적하기 시작한다.
                        accConcludeQty = int(row[3])
            startDate = startDate + dt.timedelta(days=1)
            retList.append(accForOneDay)
        return retList



def runItemSort():
    app = QApplication(sys.argv)
    myWindow = ItemSort.MyWindow()  # MyWindow 클래스를 생성하여 myWondow 변수에 할당
    myWindow.show()  # MyWindow 클래스를 노출
    app.exec_()  # 메인 이벤트 루프에 진입 후 프로그램이 종료될 때까지 무한 루프 상태 대기
def run_subProcItemSort():

    p_itemSort = mp.Process(target=runItemSort, args=())
    p_itemSort.start()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywindow = MyWindow()
    mywindow.show()
    app.exec_()


