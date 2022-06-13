import time

from ManipulateScript import SchoolScript
from chromeDriver import SeleniumDriver
from ExcelManipulate import ExcelManipulate

from DataService import dealPesonDatas

def startAutomation(datas:list):
    schooldriver = SeleniumDriver("./chromedriver/chromedriver")
    schooldriver.runPageByURL("https://csrc.edu.tw/")
    schoolscript = SchoolScript(schooldriver.driver,datas)

    schooldriver.execute_with_errorLimit(3, schoolscript.firstPageScript)
    schooldriver.execute_with_errorLimit(3, schoolscript.secondPageScript)
    schooldriver.execute_with_errorLimit(3, schoolscript.secondPageScript2)
    schooldriver.execute_with_errorLimit(3, schoolscript.secondPageScript3)
    schooldriver.execute_with_errorLimit(3, schoolscript.secondPageScript4)

    time.sleep(120)

def dataPrepare():
    recordExcel = ExcelManipulate("./明正國小確診通報.xlsx")
    studentData = ExcelManipulate("./全校名冊.xlsx")

    originRecords = recordExcel.getAllDataList()
    print(originRecords)

    return dealPesonDatas(originRecords, studentData)

if __name__ == "__main__":

    print("提醒：excel 檔必須要是xlsx的版本，不能是舊版本xls")
    print("     該Excel檔案不能有標題欄或列。")
    print("     開始執行程式前需要先關閉該Excel檔。")
    datas = dataPrepare()
    print(datas[0])
    print(datas[1])
    input("確認資料無誤請按Enter繼續，若要修正資料，請關閉本程式，待Excel內資料修正完畢後再重新執行")
    startAutomation(datas)


