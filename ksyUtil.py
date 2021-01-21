import os
import sys
import datetime
import datetime as dt
from PyQt5.QtCore import QDate



class Util():
    def __init__(self):
        return

    def getDateForFileName(self, _upper):#조금 특별한 케이스로 window에 설정되어있는 정보가 필요하기 때문에 presenter에서(혹은 presenter를 아는 객체가) self를(presenter를) 인자로 하여 호출해야함.
        date = _upper.dateEdit.date()
        datestr = date.toString("yyyy_MM_dd")
        return datestr

    def retDateForFileName(self, date):#datetime 타입의 변수를 받아서 파일명으로 사용할 수 있는 형태의 String으로 변환한다.
        datestr = str(date)
        datestr = datestr.replace("-", "_")
        return datestr

    def getPureText(self, tuple):#DB에서 가지고 온 Item name은 괄호가 포함되기 때문에 이를 제거하기 위한함수.
        item = str(tuple)
        item = item.replace("('", "")
        item = item.replace("',)", "")
        return item

    def retDatetimeFromEditVal(self, dateStr):
        dateFormatter = "%Y_%m_%d"
        dateStr = str(dateStr)
        date = dt.datetime.strptime(dateStr, dateFormatter)
        return date

    def covtQdateToPydate(self, QtDate):
        #날짜만 변경할 경우 toPyDate, 시간까지 변경할 경우 toPyDateTime 등으로 사용하여야 함.
        pyDate = QtDate.toPyDate()
        return pyDate

    def dispWeekDayKr(self, date):
        if date.weekday() == 0:
            return "월요일"
        elif date.weekday() == 1:
            return "화요일"
        elif date.weekday() == 2:
            return "수요일"
        elif date.weekday() == 3:
            return "목요일"
        elif date.weekday() == 4:
            return "금요일"
        elif date.weekday() == 5:
            return "토요일"
        elif date.weekday() == 6:
            return "일요일"

    def dispWeekDayQt(self, qtDate):
        date = self.covtQdateToPydate(qtDate)
        if date.weekday() == 0:
            return "월요일"
        elif date.weekday() == 1:
            return "화요일"
        elif date.weekday() == 2:
            return "수요일"
        elif date.weekday() == 3:
            return "목요일"
        elif date.weekday() == 4:
            return "금요일"
        elif date.weekday() == 5:
            return "토요일"
        elif date.weekday() == 6:
            return "일요일"
    def getItemNameFromItemDBList(self, DBList):
        return DBList[1].replace("'","")


    def doNothing(self):
        return
