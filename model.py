import os
import sys
import datetime
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

    def getConcInfoByItem(self, dateStr, item):
        if self.staticisFileExist(dateStr):
            if self.staticisItemExsit(dateStr, item) == True:
                con = sqlite3.connect("../conclusions/" + dateStr + ".db")
                cur = con.cursor()
                cur.execute("select * from %s;" % item)
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