import os
import sys
import datetime
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDate
from PyQt5.QtCore import QStringListModel
from PyQt5.QtCore import pyqtSlot, Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.patches as mpatches
import numpy as np
import ksyUtil


class Text():#텍스트를 창에 표시하기 위한 객체
    def __init__(self, _upper):
        self._u = _upper
        #utility객체를 초기화 한다.
        self.util = ksyUtil.Util()
        return
    def displayInit(self):
        # 초기에 표시할 텍스트를 셋팅한다. 특히 날짜 등은 해당 날짜에 따라 변동이 되므로 가변적이어서 프로그램 실행시 셋팅하도록한다.
        self.defaultTextSet()
        # 오늘날짜(가장 최근 거래일) 체결정보를 보유한 항목들을 로컬 DB로부터 읽어와서 display
        self.dispComboBox()
        # 지정된 날짜, 지정된 종목에 대하여 체결정보를 테이블에 표시한다.
        self.dispConcludeTable()


        ###### 이벤트 등록 #######
        #콤보박스에서 종목을 변경하면 테이블을 갱신한다.
        self._u.item_comboBox.currentIndexChanged.connect(self.dispConcludeTableByItem)
        #날짜 위제에서 날짜를 변경하면 테이블을 갱신한다.
        self._u.dateEdit.dateTimeChanged.connect(self.dispConcludeTableByDate)
        #run버튼 클릭 이벤트 연결
        self._u.run_btn.clicked.connect(self.runBtn)




    def defaultTextSet(self):
        self._u.dateEdit.setDate(datetime.date.today())

        self._u.dateLabel.setText(self.util.dispWeekDayKr(datetime.date.today()))
        self._u.dateEdit.setMinimumDate(QDate(2021, 1, 1))
        self._u.dateEdit.setMaximumDate(QDate(2100, 12, 31))

        self._u.endWeekday.setText(self.util.dispWeekDayKr(datetime.date.today()))
        self._u.dateEdit_3.setDate(datetime.date.today())
        self._u.dateEdit_3.setMinimumDate(QDate(2021, 1, 1))
        self._u.dateEdit_3.setMaximumDate(QDate(2100, 12, 31))

        self._u.startWeekday.setText(self.util.dispWeekDayKr(datetime.date.today()))
        self._u.dateEdit_2.setDate(datetime.date.today())
        self._u.dateEdit_2.setMinimumDate(QDate(2021, 1, 1))
        self._u.dateEdit_2.setMaximumDate(QDate(2100, 12, 31))
        return





    def dispComboBox(self):
        util = self.util
        tables = self._u.model.getAllItemList(util.getDateForFileName(self._u))
        if tables != None:
            #self._u.item_comboBox.clear()
            self._setDropCompleter(tables)
            for index in range(len(tables)):
                item = util.getPureText(tables[index])
                self._u.item_comboBox.addItem(item)
        else:#해당날짜 데이터가 없는경우(주말이거나 데이터가없거나 등등, table을 비운다.)
            self._u.item_comboBox.clear()

        return

    def getComboboxCurText(self, comboBox):
        return comboBox.currentText()

    def _setDropCompleter(self, tables):
        #tables = self.getAllItemList()
        forDropList = []
        util = self.util
        for index in range(len(tables)):
            item = util.getPureText(tables[index])
            forDropList.append(item)
            #self.item_comboBox.addItem(item)

        forDropModel = QStringListModel()##관심종목으로 추가하기 위한 line editer의 completer model
        forDropModel.setStringList(forDropList)
        forDropCompleter = QCompleter()  ##관심종목으로 추가하기 위한 line editer의 completer
        forDropCompleter.setModel(forDropModel)

        self._u.item_comboBox.setCompleter(forDropCompleter)

        lb = QLabel()#자동완성기능을 사용하기 위한 객체 생성 아마도 자동완성기능은 QLabel객체의 기능을 활용하나 봄
        self._u.item_comboBox.currentTextChanged.connect(lb.setText)#자동완성기능을 호출

    def dispConcludeTableByDate(self):#날짜가 변경된 이벤트에 대한 체결정보 refresh동작, 해당 날짜의 DB에 따라 종목명 콤보박스도 업데이트 해야함
        self.dispConcludeTable()
        self.dispComboBox()
        return
    def dispConcludeTableByItem(self):#종목명이 변경된 이벤트에 대한 체결정보 refresh동작, 종목명 콤보박스 업데이트는 하지 않아도 됨.
        self.dispConcludeTable()
        return

    def dispConcludeTable(self):
        util = self.util
        #datestr = self._u.reqGetDateForFileName(self)
        #item = self.item_comboBox.currentText()
        date = self._u.dateEdit.date()
        date = util.covtQdateToPydate(date)
        self._u.dateLabel.setText(self.util.dispWeekDayKr(date))
        rows = self._u.reqConcInfoByItem()
        if rows != None:
            self._u.concTableWidget.setColumnCount(4)
            self._u.concTableWidget.setRowCount(len(rows))
            self._u.concTableWidget.setHorizontalHeaderLabels(["시간", "체결가", "체결량", "체결금액"])
            for i, row in enumerate(rows, 0):
                insertTime = QTableWidgetItem(row[1])
                insertPrice = QTableWidgetItem(str(format(row[2], ",")))
                insertQty = QTableWidgetItem(str(format(row[3], ",")))
                insertValue = QTableWidgetItem(str(format(row[4], ",")))
                insertTime.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
                insertPrice.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
                insertQty.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
                insertValue.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
                self._u.concTableWidget.setItem(i, 0, insertTime)
                self._u.concTableWidget.setItem(i, 1, insertPrice)
                self._u.concTableWidget.setItem(i, 2, insertQty)
                self._u.concTableWidget.setItem(i, 3, insertValue)
        else:
            self._u.concTableWidget.clear()

    def runBtn(self):
        return


class graph():#그래프를 창에 표시하기 위한 객체
    def __init__(self, _upper):
        self._u = _upper
        # utility객체를 초기화 한다.
        self.util = ksyUtil.Util()

        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)

        # run버튼 클릭 이벤트 연결
        self._u.btnTrandReq.clicked.connect(self.btnTrandReqClicked)

        #날짜 위제에서 날짜를 변경하면 테이블을 갱신한다.
        self._u.dateEdit_2.dateTimeChanged.connect(self.checkRangeOfStartDay)
        self._u.dateEdit_3.dateTimeChanged.connect(self.checkRangeOfEndDay)

        _upper.ConcHistoryGraph.addWidget(self.canvas)
        self.plotConcHistoryGraph()
        return

    def checkRangeOfStartDay(self):#시작날짜는 endDay보다 클 수 없다.(endDay는 오늘보다 클수없는 조건이 붙기때문에 endDay하고만 비교하면 됨.)
        today = datetime.date.today()
        startDayStr = self._u.dateEdit_2.date()
        endDayStr = self._u.dateEdit_3.date()
        startDay = self.util.covtQdateToPydate(startDayStr)
        endDay = self.util.covtQdateToPydate(endDayStr)
        if startDay > endDay:
            self._u.dateEdit_2.setDate(endDay)
        self._u.startWeekday.setText(self.util.dispWeekDayQt(self._u.dateEdit_2.date()))
        return
    def checkRangeOfEndDay(self):#종료날짜는 오늘보다 클 수 없고 startDay보다 작을 수 없다.
        today = datetime.date.today()
        startDayStr = self._u.dateEdit_2.date()
        endDayStr = self._u.dateEdit_3.date()
        startDay = self.util.covtQdateToPydate(startDayStr)
        endDay = self.util.covtQdateToPydate(endDayStr)
        if endDay > today:
            self._u.dateEdit_3.setDate(today)
        if endDay < startDayStr:
            self._u.dateEdit_3.setDate(startDayStr)
        self._u.endWeekday.setText(self.util.dispWeekDayQt(self._u.dateEdit_3.date()))
        return

    def plotConcHistoryGraph(self):
        x = np.arange(0, 100, 1)
        y = np.sin(x)

        ax = self.fig.add_subplot(212)#그래프를 여러개 그릴때 영역을 분할하여 그릴 수 있음 (세로영역갯수, 가로영역 갯수, 현재 표시할 위치)
        ax.plot(x, y, label="label")
        ax.set_xlabel("x_axis")
        ax.set_ylabel("y_axis")

        ax.set_title("my graph")
        ax.legend()#그래프의 명각을 표시하는 메서드
        self.canvas.draw()
        return

    def btnTrandReqClicked(self):
        qtStartDateStr = self._u.dateEdit_2.date()
        qtEndDateStr = self._u.dateEdit_3.date()
        startDate = self.util.covtQdateToPydate(qtStartDateStr)
        endDate = self.util.covtQdateToPydate(qtEndDateStr)
        item = self._u.lineEditForRun_2.text()
        baseAmount = self._u.lineEditForRun_3
        if self._u.unitDay.isChecked() == True:
            reqUnit = "day"
        elif self._u.unitWeek.isChecked() == True:
            reqUnit = "week"
        elif self._u.unitMonth.isChecked() == True:
            reqUnit = "month"
        else:#radio버튼이 아무것도 선택되어있지 않은경우 일봉으로 설정.
            reqUnit = "day"
        self._u.TrandReqModel(startDate, endDate, item, baseAmount, reqUnit)
        return
    def plotConcGraph(self, dispLists):
        x = 0
        y = 0
        self.fig.clf(212)#새로 그리기 전에 figure클리어, 클리어에는 cla(axis클리어), clf(figure클리어), close(window클리어)가 있음.
        ax = self.fig.add_subplot(212)
        ax.plot(x, y, label="label")
        ax.set_xlabel("date")
        ax.set_ylabel("y_axis")

        ax.set_title("my graph")
        ax.legend()
        self.canvas.draw()
        return
class eventSet():#이벤트 관련 처리 객체
    def __init__(self, _upper):
        self._u = _upper
        return
class input():#입력 데이터 관련 객체
    def __init__(self, _upper):
        self._u = _upper
        return