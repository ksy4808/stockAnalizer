import os
import sys
import datetime
from PyQt5.QtCore import QDate


class ksyUtil():
    def __init__(self, _upper):
        self._upper = _upper
        date = self._upper.dateEdit.date()
        return

    def getDateForFileName(self):
        date = self._upper.dateEdit.date()
        # datestr = "2021_01_08"
        i = 0

        while True:
            # date = date+timedelta(days=-i)
            date = date.addDays(-i)
            datestr = date.toString("yyyy_MM_dd")
            if True == self.staticisFileExist(date):
                self._upper.dateEdit.setDate(date)
                return datestr
            i += 1

    def staticisFileExist(self, date):
        datestr = date.toString("yyyy_MM_dd")
        file = "../conclusions/" + datestr + ".db"
        if os.path.exists(file):
            return True
        return False
