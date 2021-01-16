import os
import sys
import datetime
from PyQt5.QtCore import QDate


class Util():
    def __init__(self):
        return

    def getDateForFileName(self, _upper):#조금 특별한 케이스로 window에 설정되어있는 정보가 필요하기 때문에 presenter에서(혹은 presenter를 아는 객체가) self를(presenter를) 인자로 하여 호출해야함.
        date = _upper.dateEdit.date()
        i = 0

        while True:
            # date = date+timedelta(days=-i)
            date = date.addDays(-i)
            datestr = date.toString("yyyy_MM_dd")
            if True == self.staticisFileExist(date):
                _upper.dateEdit.setDate(date)
                return datestr
            i += 1

    def staticisFileExist(self, date):
        datestr = date.toString("yyyy_MM_dd")
        file = "../conclusions/" + datestr + ".db"
        if os.path.exists(file):
            return True
        return False

    def getPureText(self, tuple):
        item = str(tuple)
        item = item.replace("('", "")
        item = item.replace("',)", "")
        return item
