from ExcelManipulate import ExcelManipulate
from  exception_forSchoolInfo import  StudentDataNotFound, DataHasError, EmptyDataException


def dealPesonDatas(originRecords:list, studentData:ExcelManipulate, count=0):

    personDataLists = []
    # [隔離學生數, 隔離老師數, 隔離教職員數]
    globalDataList = [0, 0, 0]

    for originRecord in originRecords:
        count+=1
        try:
            personDataList = personDataFormat(originRecord, studentData, globalDataList)

        except EmptyDataException: continue

        except StudentDataNotFound:
            print("StudentDataNotFound")
            continue

        except ValueError:
            print(ValueError)
            continue

        except Exception as e:
            print("*1第"+str(count)+"筆有錯誤：",e.__class__, e.args)
            continue

        try:
            personDataList = personDataTransform(personDataList)
            personDataValidator(personDataList)
            print("塞入第"+str(count)+"筆資料")
            personDataLists.append(personDataList)
        except DataHasError as dhe:
            print("*2第" + str(count) + "筆有錯誤：", dhe)

    return [personDataLists, globalDataList]



def personDataFormat(originRecord:list, studentData:ExcelManipulate, globalDatalist:list):

    match originRecord[2]:
        case "學生":
            # 原生資料
            classesOrDepartment = dealclassString(originRecord[4], originRecord[5])
            name = originRecord[3]
            location = originRecord[8]
            status = statusCheck(originRecord[7])
            identity = "1" #職稱： 學生 "1"  教師 "2" 教職員 "4"
            otherInfo = originRecord[9]
            # 需要到學生資料表中抓取的資料
            seat = str(originRecord[6])
            studentDataRowIndex = studentRowIndex(classesOrDepartment, seat, studentData)
            birth = studentData.getCellcontent(studentDataRowIndex, 7)[0:4]
            sex = studentData.getCellcontent(studentDataRowIndex, 4)

            globalDatalist[0] += 1

        case "導師":
            # 原生資料
            classesOrDepartment = dealclassString(originRecord[11], originRecord[12])
            name = originRecord[10]
            location =originRecord[15]
            status = statusCheck(originRecord[14])
            identity = "2" #職稱： 學生 "1"  教師 "2" 教職員 "4"
            otherInfo = originRecord[16]
            birth = str(int(originRecord[13])+1911)
            sex = originRecord[28]

            globalDatalist[1] += 1

        case "科任教師":

            # 原生資料
            classesOrDepartment = "科任教師"
            name = originRecord[17]
            location = originRecord[20]
            status = statusCheck(originRecord[19])
            identity = "2" #職稱： 學生 "1"  教師 "2" 教職員 "4"
            otherInfo = originRecord[21]
            birth = str(int(originRecord[18])+1911)
            sex = originRecord[29]

            globalDatalist[1] += 1
        case "教職員(含行政老師)":
            # 原生資料
            classesOrDepartment = originRecord[23]
            name = originRecord[22]
            location = originRecord[26]
            status = statusCheck(originRecord[25])
            identity = "4" #職稱： 學生 "1"  教師 "2" 教職員 "4"
            otherInfo = originRecord[27]
            birth = str(int(originRecord[24])+1911)
            sex = originRecord[30]

            globalDatalist[2] += 1

        case _:
            if originRecord[0] != 'None' : raise DataHasError(("身份無法識別，請確認資料",))
            else: raise EmptyDataException

    return [classesOrDepartment, name, birth, sex, location, status, identity, otherInfo]


# personData = [處室/班級, 姓名, 生日, 性別, 地點, 狀態, 身份, 備註]
def personDataTransform(personData:list):
    if personData[1] == 'None': personData[1]=""
    if personData[3] == "男": personData[3] = "0"
    elif personData[3] == "女" : personData[3] = "1"
    if personData[4] == "在家中" : personData[4] = "4"
    elif personData[4] == "在醫院" : personData[4] = "1"
    if personData[7] == 'None' : personData[7] = ""
    return  personData

def personDataValidator(personData:list):
    if (not isinstance(personData[0], str)) or (len(personData[0]) != 3 and len(personData[0])!=4):
        raise DataHasError(("資料有誤，處室或班級名稱錯誤",))
    if (not isinstance(personData[1], str)) or len(personData[1]) < 1 or len(personData[1]) > 5 :
        raise DataHasError(("資料有誤，姓名錯誤",))
    if (not isinstance(personData[2], str)) or len(personData[2]) !=4 : raise DataHasError(("資料有誤，生日錯誤",))
    if (not isinstance(personData[3], str)) or (personData[3] != "0" and personData[3] != "1") :
        raise DataHasError(("資料有誤，性別錯誤",))
    if (not isinstance(personData[4], str)) or (personData[4] != "1" and personData[4] != "4") :
        raise DataHasError(("資料有誤，所在位置錯誤",))
    if (not isinstance(personData[5], str)) or (personData[5] != "D" and personData[5] != "S" and personData[5]!="A2") :
        raise DataHasError(("資料有誤，狀況錯誤",))
    if (not isinstance(personData[6], str)) or (personData[6] != "1" and personData[6] != "2" and personData[6]!="4") :
        raise DataHasError(("資料有誤，身份錯誤",))
    if (not isinstance(personData[7], str)) : raise DataHasError(("資料有誤，備註錯誤",))


def statusCheck(status:str):
    match status:
        case "快篩陽":
            return "S"
        case "PCR確診":
            return "S"
        case "疑似確診":
            return "D"
        case "接種疫苗不良反應":
            return "A2"

# 找到該學生在全校資料中是第幾筆資料123
def studentRowIndex(classes:str, seat:str, targetExcel: ExcelManipulate):
    classesFilterlist = targetExcel.compareContentByColumnAllRow(classes, 1)
    namefilterlist = targetExcel.compareContentByColumnWithinRow(seat, 2, classesFilterlist)

    if len(namefilterlist) == 0 : raise StudentDataNotFound
    return namefilterlist[0]

def dealclassString(grade:str, classes:str):
    return grade[0:2] + classes





if __name__ == "__main__":
    personDataValidator(["123","1" ,"1994", "1", "4","D", "2", ])