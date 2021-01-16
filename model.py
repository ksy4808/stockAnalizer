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

    def getAllItemList(self, datestr):
        util = self.util
        con = sqlite3.connect("../conclusions/" + datestr + ".db")
        cur = con.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        rows = cur.fetchall()
        con.close()
        return rows

    def getConcInfoByItem(self, date, item):
        con = sqlite3.connect("../conclusions/" + date + ".db")
        cur = con.cursor()
        cur.execute("select * from %s;" % item)
        rows = cur.fetchall()
        con.close()
        return rows