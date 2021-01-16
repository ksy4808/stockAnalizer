import os
import sys
import datetime
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDate
from PyQt5.QtCore import QStringListModel
from PyQt5.QtCore import pyqtSlot, Qt
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
        self._u.item_comboBox.currentIndexChanged.connect(self.dispConcludeTable)
        #날짜 위제에서 날짜를 변경하면 테이블을 갱신한다.
        self._u.dateEdit.dateTimeChanged.connect(self.dispConcludeTable)



    def defaultTextSet(self):
        self._u.dateEdit.setDate(datetime.date.today())
        self._u.dateEdit.setMinimumDate(QDate(2021, 1, 1))
        self._u.dateEdit.setMaximumDate(QDate(2100, 12, 31))

        self._u.dateEdit_2.setDate(datetime.date.today())
        self._u.dateEdit_2.setMinimumDate(QDate(2021, 1, 1))
        self._u.dateEdit_2.setMaximumDate(QDate(2100, 12, 31))

        self._u.dateEdit_3.setDate(datetime.date.today())
        self._u.dateEdit_3.setMinimumDate(QDate(2021, 1, 1))
        self._u.dateEdit_3.setMaximumDate(QDate(2100, 12, 31))
        return

    def dispComboBox(self):
        util = self.util
        tables = self._u.model.getAllItemList(util.getDateForFileName(self._u))
        for index in range(len(tables)):
            item = util.getPureText(tables[index])
            self._u.item_comboBox.addItem(item)
            self._setDropCompleter(tables)
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

    def dispConcludeTable(self):
        #util = self.util
        #datestr = self._u.reqGetDateForFileName(self)
        #item = self.item_comboBox.currentText()
        rows = self._u.reqConcInfoByItem()
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



class graph():#그래프를 창에 표시하기 위한 객체
    def __init__(self, _upper):
        self._u = _upper
        return
class eventSet():#이벤트 관련 처리 객체
    def __init__(self, _upper):
        self._u = _upper
        return
class input():#입력 데이터 관련 객체
    def __init__(self, _upper):
        self._u = _upper
        return