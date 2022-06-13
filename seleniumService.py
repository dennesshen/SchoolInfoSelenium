import time

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# personDatas = [處室, 姓名, 生日, 性別, 地點, 狀態, 身份, 備註]
def personDataInput(driver:WebDriver, personDatas:list):
    xpath = "/html/body/div[1]/div[2]/div[2]/table/tbody/tr[2]/td[1]/div/div[2]/h3[1]/table/tbody/tr/td[2]/img"
    driver.find_element(By.XPATH, xpath).click()
    time.sleep(1)

    iframe = driver.find_element(By.ID, "TB_iframeContent")
    driver.switch_to.frame(iframe)

    # 處室、姓名、出生年
    driver.find_element(By.ID, "department").send_keys(personDatas[0])
    driver.find_element(By.ID, "name").send_keys(personDatas[1])
    Select(driver.find_element(By.ID, "BirthYears")).select_by_value(personDatas[2])

    #性別 男生給0 女生給1
    driver.find_elements(By.ID, "sex")[int(personDatas[3])].click()

    location  = personDatas[4]  # 醫院 "1" 家中"4"
    situation = personDatas[5]   # 疑似病例 "D" 確定病例 "S" 接種疫苗不良反應"A2"

    match situation:
        case "D":
            Select(driver.find_element(By.ID, "ncovType")).select_by_value("D")
            Select(driver.find_element(By.ID, "ncovHandle")).select_by_value("A")
            Select(driver.find_element(By.ID, "ncovAutonomy")).select_by_value("I")
            Select(driver.find_element(By.ID, "ncovFilter")).select_by_value("E")

        case "S":
            Select(driver.find_element(By.ID, "ncovType")).select_by_value("S")
            driver.find_element(By.ID, "ncovLocation_1").click()
            Select(driver.find_element(By.ID, "ncovStatus")).select_by_value("H")
            if location == "1":
                Select(driver.find_element(By.ID, "ncovHandle")).select_by_value("I")
            else:
                Select(driver.find_element(By.ID, "ncovHandle")).select_by_value("A")
                Select(driver.find_element(By.ID, "ncovAutonomy")).select_by_value("I")


        case "A2":
            Select(driver.find_element(By.ID, "ncovType")).select_by_value("A2")

    #狀態：一律寫疾病
    Select(driver.find_element(By.ID, "state_sno")).select_by_value("6")

    # 職稱： 學生 "1"  教師 "2" 教職員 "4"
    identity = personDatas[6]
    match identity:
        case "1":
            Select(driver.find_element(By.ID, "title")).select_by_value("1")
            Select(driver.find_element(By.ID, "student_cate_sno")).select_by_value("3")
            Select(driver.find_element(By.ID, "school_system_sno")).select_by_value("3")

        case "2":
            Select(driver.find_element(By.ID, "title")).select_by_value("2")
            Select(driver.find_element(By.ID, "teacherType")).select_by_value("T")

        case "4":
            Select(driver.find_element(By.ID, "title")).select_by_value("4")



    # 所在位置 醫院 "1" 家中"4"
    Select(driver.find_element(By.ID, "locate_sno")).select_by_value(location)

    # 角色 一律選疾患人員 "7"
    Select(driver.find_element(By.ID, "role_sno")).select_by_value("7")

    # 是否曾經發生 選否
    driver.find_elements(By.ID, "is_experience")[1].click()

    # 備註
    driver.find_element(By.ID, "summary").send_keys(personDatas[7])

    # 按下送出
    time.sleep(2)
    driver.find_element(By.ID, "button3").click()
    WebDriverWait(driver, 10).until(EC.alert_is_present(), 'Timed out waiting for simple alert to appear')
    driver.switch_to.alert.accept()

    time.sleep(2)
    driver.switch_to.default_content()
