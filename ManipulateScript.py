import time

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import seleniumService


class SchoolScript:

    # globalData =[當天學生隔隔人數, 當天教師隔隔人數, 當天教職員隔離人數]
    # personData = [處室/班級, 姓名, 生日, 性別, 地點, 狀態, 身份, 備註]
    def __init__(self,mainDriver:WebDriver, datas:list):
        self.globalData = datas[1]
        self.personDatas = datas[0]
        self.mainDriver = mainDriver


    def firstPageScript(self):
        username = input("請輸入登入帳號：") or "x12u058"
        password = input("請輸入登入密碼：") or "j7524567"
        authcode = input("請輸入畫面上驗證碼:")
        while username == "" or  password == "" or authcode == "":
            print("您的帳號密碼或驗證碼有未輸入項目，請重新輸入")
            username = input("請輸入登入帳號：") or "x12u058"
            password = input("請輸入登入密碼：") or "j7524567"
            authcode = input("請輸入畫面上驗證碼:")

        self.mainDriver.find_element(By.ID, "strUserID").send_keys(username)
        self.mainDriver.find_element(By.ID, "strPwd").send_keys(password)
        self.mainDriver.find_element(By.ID, "strCaptchaCode").send_keys(authcode)

        self.mainDriver.find_element(By.CLASS_NAME, "loginbtn").click()
        self.mainDriver.implicitly_wait(10)
        self.mainDriver.find_element(By.CLASS_NAME, "topbtn4").click()
        self.mainDriver.implicitly_wait(10)
        # 進入通報頁面
        self.mainDriver.find_element(By.LINK_TEXT, "首　報").click()
        self.mainDriver.implicitly_wait(10)

    def secondPageScript(self):

        # 事件主類別
        Select(self.mainDriver.find_element(By.ID, "EventCategoryId")).select_by_value("H")
        self.mainDriver.find_element(By.ID, "EventTimeType").click()

        # 發生地點
        time.sleep(2)
        self.mainDriver.find_elements(By.ID,"in_school")[2].click()
        time.sleep(3)
        self.mainDriver.find_elements(By.ID, "which_status")[1].click()

        # 消息來源、媒體、其他學校
        Select(self.mainDriver.find_element(By.ID, "MessageFrom")).select_by_value("3")
        self.mainDriver.find_elements(By.ID,"is_medium")[0].click()
        self.mainDriver.find_elements(By.ID,"is_otherschool")[0].click()


    def secondPageScript2(self):

        # 次類別處理
        self.mainDriver.find_element(By.ID, "btn_EventData").click()
        time.sleep(3)
        self.mainDriver.implicitly_wait(10)
        iframe = self.mainDriver.find_element(By.ID,"TB_iframeContent")
        self.mainDriver.switch_to.frame(iframe)
        self.mainDriver.find_elements(By.CSS_SELECTOR, "span[style='cursor:pointer']")[7].click()
        self.mainDriver.switch_to.default_content()

        # 是否居家隔離的選取
        self.mainDriver.find_element(By.ID, "isAutonomy_Y").click()
        time.sleep(1)
        self.mainDriver.find_element(By.ID, "homeIsolation").click()
        time.sleep(1)
        self.mainDriver.find_element(By.ID, "stuIsolation").send_keys(self.globalData[0]) #當天學生隔隔人數
        self.mainDriver.find_element(By.ID, "tchIsolation").send_keys(self.globalData[1]) #當天教師隔隔人數
        self.mainDriver.find_element(By.ID, "staffIsolation").send_keys(self.globalData[2]) #當天教職員隔離人數
        self.mainDriver.find_element(By.ID, "coachIsolation").send_keys("0")
        self.mainDriver.find_element(By.ID, "playerIsolation").send_keys("0")
        self.mainDriver.find_element(By.ID, "volunteerIsolation").send_keys("0")
        self.mainDriver.find_element(By.ID, "outsourceIsolation").send_keys("0")

        # 是否職業傷害
        self.mainDriver.find_element(By.ID, "isOccupat_N").click()
        self.mainDriver.implicitly_wait(10)


    def secondPageScript3(self):

        # 是否停課
        self.mainDriver.find_elements(By.NAME , "StopClassFlag")[0].click()
        time.sleep(3)

        xpath = "/html/body/div[3]/div[2]/div/div/div/div/div[3]/div/table/tbody/tr/td/div/div/table/tbody/tr[1]/td[2]/select"
        stopClass =self.mainDriver.find_element(By.XPATH, xpath)
        Select(stopClass).select_by_value("ALL")
        time.sleep(1)

        self.mainDriver.find_element(By.ID,"nowStopQuantityPop").send_keys("39")
        self.mainDriver.find_element(By.ID,"stopTchQuantityPop").send_keys("0")
        self.mainDriver.find_element(By.ID,"stopStuQuantityPop").send_keys("1017")
        self.mainDriver.find_element(By.ID,"stopClassBtn").click()


    # 填寫每一筆個人資料
    def secondPageScript4(self):
        for personData in self.personDatas:
            seleniumService.personDataInput(self.mainDriver, personData)

        self.mainDriver.find_element(By.ID, "submitBtn").click()
        self.mainDriver.implicitly_wait(30)

    def thirdPageScript(self):
        self.mainDriver.find_element(By.ID,"EventReason").send_keys(self.globalData[3])
        self.mainDriver.find_element(By.ID,"EventHandleOther0").send_keys("1.加強校園清消。\n"+
                                                                          "2.請導師加強宣導在家要多注意自己的衞生習慣，以降低染疫風險。\n"+
                                                                          "3.持續關懷學生的身體健康及心理狀態。\n"
                                                                          "4.並注意學生在家自主學習情形。")

        print("按Enter完成通報")
        self.mainDriver.find_element(By.ID, "SubmitBtn").click()
        input()
        WebDriverWait(self.mainDriver, 10).until(EC.alert_is_present(), 'Timed out waiting for simple alert to appear')
        self.mainDriver.switch_to.alert.accept()


