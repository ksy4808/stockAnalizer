import os
import sys
import datetime
from datetime import timedelta
from PyQt5.QtCore import QDate
import sqlite3
import ksyUtil

class getFromLocalDB():#로컬 DB에서 파일을 가지고 오는 객체
    def __init__(self):
        #utility객체를 초기화 한다.
        self.util = ksyUtil.Util()
        return

    def getAllItemList(self, dateStr):
        util = self.util
        if self.staticisFileExist(dateStr):
            con = sqlite3.connect("../conclusions/" + dateStr + ".db")
            cur = con.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
            rows = cur.fetchall()
            con.close()
            return rows
        return None

    def getConcInfoByItem(self, dateStr, itemStr):
        if self.staticisFileExist(dateStr):
            if self.staticisItemExsit(dateStr, itemStr) == True:
                con = sqlite3.connect("../conclusions/" + dateStr + ".db")
                cur = con.cursor()
                cur.execute("select * from %s;" % itemStr)
                rows = cur.fetchall()
                con.close()
                return rows
        return None

    def staticisFileExist(self, dateStr):
        #datestr = date.toString("yyyy_MM_dd")
        file = "../conclusions/" + dateStr + ".db"
        if os.path.exists(file):
            return True
        return False

    def staticisItemExsit(self, dateStr, itemStr):
        if True == self.staticisFileExist(dateStr):
            con = sqlite3.connect("../conclusions/" + dateStr + ".db")
            cur = con.cursor()
            cur.execute("SELECT count(*) from sqlite_master WHERE type='table' AND Name = '%s';"%itemStr)
            sQuery = cur.fetchone()
            #cur.execute("select * from %s;" % itemStr)
            #rows = cur.fetchall()
            con.close()
            if sQuery[0] < 1:
                return False
            return True
        return False

    def reqTotalConcInfo(self, itemStr, startDate, endDate):
        retSegAllDays = []
        days = (endDate - startDate).days + 1#시작날짜와 종료날짜를 포함해야하므로 1을 더함.
        for i in range(days):
            retSegEachdate = []
            getDateOfData= startDate + datetime.timedelta(days=i)
            getDateOfDataStr = self.util.retDateForFileName(getDateOfData)
            if self.staticisItemExsit(getDateOfDataStr, itemStr) == True:#
                con = sqlite3.connect("../conclusions/" + getDateOfDataStr + ".db")
                cur = con.cursor()
                cur.execute("select * from %s;" % itemStr)
                rows = cur.fetchall()
                retSegEachdate = rows
            retSegAllDays.append(retSegEachdate)
        return retSegAllDays