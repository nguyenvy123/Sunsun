# -*- encoding=utf8 -*-
__author__ = "LinhDNA"

import datetime 
#import pandas as pd
from airtest.core.api import *
from poco.drivers.cocosjs import CocosJsPoco
poco = CocosJsPoco()
from airtest.core.api import using
using("Constant.air")
from Constant import *
using("Content.air")
from Content import *
using("Api.air")
from Api import *
using("Main.air")
from ExcelUtility import *
auto_setup(__file__)

lastCheckPoint, tcPass = True, True
countPass, countFail = 0, 0
arrRs, popups = [], []

def init(v1):
    global runningDevice
    runningDevice = v1
    
# ========================== Common Function ========================== 

# Check Gold ở Lobby
def CheckUpdateGold(caseId, txtCompare, txtLogContent):
    txtGoldUserIngame = poco(TXT_GOLD_LOBBY).get_text()
    CheckTxtExists(txtGoldUserIngame, txtCompare, caseId, "%s Client:" %txtLogContent) 
    txtGoldUserIngame = CompactGold(GetUserModel()["gold"])
    CheckTxtExists(txtGoldUserIngame, txtCompare, caseId, "%s Server:" %txtLogContent) 

# Loại bỏ dấu phân tách hàng nghìn của các số
# Separator: string (. ,)
def RemoveSeparator(txtGold, separator):
    arr = txtGold.split(separator)
    txt = ""
    for i in arr:
        txt = "%s%s" % (txt, i)
    return txt

# Định dạng lại số Gold theo dạng rút gọn giống trong game
def CompactGold(number):
    numString = "%s" % number
    prefix = ""
    if len(numString) > 9:
        numString = "%.2f" % (number / 1000000000.0) # FixNum("%.2f" % (number / 1000000000.0))
        prefix = "B"
    elif len(numString) > 6:
        numString = "%.2f" % (number / 1000000.0) # FixNum("%.2f" % (number / 1000000.0))
        prefix = "M"
    elif len(numString) > 4:
        numString = "%.2f" % (number / 1000.0) # FixNum("%.2f" % (number / 1000.0))
        prefix = "K"
    elif len(numString) > 3:
        numString = numString[:1] + "," + numString[1:len(numString)]
    if numString.count(".") == 1:
        while numString[len(numString) - 1] == '0':
            numString = numString[:len(numString) - 1]
        if numString[len(numString) - 1] == '.':
            numString = numString[:len(numString) - 1]
    numString = numString + prefix
    print("Before: %s ------ After: %s" % (number, numString))
    return numString

def FixNum(num):
    return "%.1f" % (int(float(num)*10)/10)

# Cheat Gold cho user, mặc định là 1000, không cần reload Lobby
def CheatGold(numGold):
    if not poco(BTN_CHEAT_PLAYER).exists():
        poco(BTN_CHEAT).click()
    if not poco(CHEAT_GOLD).exists():
        poco(BTN_CHEAT_PLAYER).click([0.5,0.5])
    if poco(CHEAT_GOLD).get_text() != str(numGold):
        poco(CHEAT_GOLD).click()
        for i in range(10):
            keyevent("KEYCODE_DEL")
        text(str(numGold))
    poco("Cheat_" + CHEAT_GOLD).child(BTN_CHEAT_PRIVATE).click()
    poco(BTN_CHEAT).click()
    print("Close Cheat Gold")

# Reload lobby bằng cách bấm chọn bàn rồi thoát
def ReloadLobby(isReload=False, isClose=True):
    poco(BTN_SELECT_TABLE).click([0.5,0.5])
    sleep(1)
    poco(BTN_EXIT).click()
    sleep(1)
    ClosePopups(isReload, isClose)

# Ở Lobby đóng các loại Popups có thể có, xếp theo thứ tự ưu tiên
# Sau khi gọi hàm này, có thể dùng data trong popups để check nếu cần
# isReload: Có reload lần nữa không? Nhiều trường hợp phải reload Lobby 2 lần cho chắc hehe
# isClose: Click btn Close không? Nhiều GUI có thể check click btn khác để close
def ClosePopups(isReload=False, isClose=True):
    global popups
    if not isReload:
        popups = []
    # Popup Claim Ranking Reward
    if poco(TXT_CLAIM).exists() and poco(TXT_CLAIM).get_text() == TOP_CONGRAT:
        popups.append(RANKING_REWARD)
        poco(BTN_CLAIM_REWARD).click()
        poco(BTN_CLOSE).click()
        sleep(1)
    # Popup Final Ranking
    if poco(GUI_END_RANKING).exists():
        popups.append(FINAL_RANING)
        poco(BTN_CONFIRM).click()
        sleep(1)
    # Popup Daily Bonus
    if poco(text = TXT_TODAY).exists():
        popups.append(DAILY_BONUS)
        poco(BTN_CLAIM_BONUS).click()
        sleep(1)
    # Tutorial        
    if poco(IMG_HAND).exists():
        popups.append(TUTORIAL)
        poco(BTN_PLAY).click()
        poco(BTN_LEAVE_GAME).click()
        sleep(1)
    # Popup Event WC
    if poco(POPUP_WC).exists():
        popups.append(POPUP_EVENT_WC)
        if isClose:
            poco(BTN_CLOSE).click()
        else:
            poco(BTN_ACTION).click()
            CheckImgExists(0, "Click Join Now In Popup Event, Open Event WC", poco(TITLE_GUI, text = TITLE_WC))
            if lastCheckPoint:
                poco(BTN_CLOSE).click()
                popups.append(EVENT_WC)
        sleep(1)
    # Event WC
    if poco(TITLE_GUI, text = TITLE_WC).exists():
        popups.append(EVENT_WC)
        poco(BTN_CLOSE).click()
        sleep(1)
    # Popup Final Ranking - Show after GUI Event when next day
    if poco(GUI_END_RANKING).exists():
        popups.append(FINAL_RANING)
        poco(BTN_CONFIRM).click()
        sleep(1)
    print("Popups List: %s" % popups)
    # Popup Deal Event WC
    if poco(TITLE_GUI, text = TITLE_DEAL).exists():
        popups.append(DEAL_WC)
        poco(BTN_CLOSE).click()
        sleep(1)
    # Popup Daily Bonus
    if poco(text = TXT_TODAY).exists():
        popups.append(DAILY_BONUS)
        poco(BTN_CLAIM_BONUS).click()
        sleep(1)
    # Notifications
    if poco(TITLE_GUI, text = NOTIFICATION).exists():
        popups.append(NOTI)
        poco(BTN_CLOSE).click()
        sleep(1)
    # Shop - receive gold support
    if poco(GUI_SHOP).exists():
        if poco(BTN_RECEIVE).exists():
            poco(BTN_RECEIVE).click()
            poco(BTN_BACK).click() # Touch out to receive
        poco(BTN_BACK).click()
        popups.append(GOLD_SUPPORT)
        sleep(1)
    # Popup Offer 1st
    if poco(GUI_OFFER_1ST).exists():
        popups.append(OFFER_1ST)
        poco(BTN_CLOSE).click()
        sleep(1)
    # Join Ranking
    if poco(text = GUI_RANKING).exists():
        popups.append(JOIN_RANKING)
        poco(BTN_CLOSE).click()
        sleep(1)

def CheckShowGoldSupport(caseId, expect=True):
    CheatGold(minGold - 1)  # Cheat gold không đủ chơi mức tối thiểu
    ReloadLobby()
    if expect:
        WriteLogRunning(caseId, "VIP out of Gold first time, receive Support", "", False, CheckPopupVisible(GOLD_SUPPORT), "0") 
    else:
        WriteLogRunning(caseId, "VIP out of Gold next time, not receive Support", "", False, not CheckPopupVisible(GOLD_SUPPORT), "0")

def CheckPopupVisible(popupName):
    hasPopupName = False
    for i in range(len(popups)):
        if popups[i] == popupName:
            hasPopupName = True
            break
    return hasPopupName

def AddBOT(num):
    if not poco(BTN_ADD_BOT).exists():
        poco(BTN_CHEAT).click()
    for i in range(num):
        poco(BTN_ADD_BOT).click([0.5, 0.5])
    poco(BTN_CHEAT).click()

def CheatTestCaseLogic(tcid):    
    if not poco(BTN_CHEAT_PLAYER).exists():
        poco(BTN_CHEAT).click()
    poco(TXT_TC_ID).click()
    for i in range(2):
        keyevent("KEYCODE_DEL")
    text(str(tcid))
    poco(BTN_CHEAT_TC).click()
    poco(BTN_CHEAT).click()
    print("Play case %s" %tcid)
    
def RestartGame(caseId, timeWait=20):
    stop_app(PKG)
    start_app(PKG)
    sleep(timeWait)
    ReloadLobby()

def PlayGameOverNight():
    CheatTime("0 23 59")
    uId = GetCurUId()
    uGold = api_getModel(uId, USER_MODEL)["gold"]
    if uGold < minGold:
        CheatGold(minGold)
    poco(BTN_PLAY).click()
    poco(BTN_CHEAT).wait_for_appearance()
    AddBOT(1)
    sleep(COUNT_DOWN_TIME)
    poco(BTN_LEAVE_GAME).click()    
    
# ========================== Functions about time ==========================

# Cheat time - Format time: "day+hour+minute" hoặc "day hour minute" hoặc "dd/mm/yy/hh/mm".
# Ex: CheatTime("1+0+0") - Cheat thêm 1 ngày - Thường dùng khi test VIP
# Ex: CheatTime("0+1+20") - Cheat thêm 1 giờ 20 phút cùng ngày - Thường dùng khi test Offer
# Ex: CheatTime("1 23 59") - Cheat đến 23 giờ 59 phút của 1 ngày tiếp theo - Thường dùng trong event, Daily Bonus, VIP
# Ex: CheatTime("13/3/2003/23/58") - Cheat time đến chính xác 1 mốc ngày giờ nào đó
def CheatTime(time):
    if not (time.count("/") > 0):
        curTime = GetCurTime().split("/")
        curDate = int(curTime[0])
        curMonth = int(curTime[1])
        curYear = int(curTime[2])
        curHour = int(curTime[3])
        curMinute = int(curTime[4])

        timestampNow = datetime.datetime(curYear, curMonth, curDate, curHour, curMinute).timestamp()
        
        isPlus = False  # Là cheat tăng giờ hay cheat số giờ chính xác
        if time.count("+") > 0:
            dataTime = time.split("+")
            isPlus = True
        else:
            dataTime = time.split(" ")
        mTxt = [[1, 31], [2, 28], [3, 31], [4, 30], [5, 31], [6, 30], [7, 31], [8, 31], [9, 30], [10, 31], [11, 30], [12, 31]]    
        numDay = mTxt[curMonth - 1][1]
        if curMonth == 2 and curYear % 4 == 0:
            numDay = 29
            
        if isPlus:  # Cheat thêm thời gian
            deltaSecond = ((int(dataTime[0]) * 24 + int(dataTime[1])) * 60 + int(dataTime[2])) * 60
            timestampNow += deltaSecond
            curTime = SeparateTime(datetime.datetime.fromtimestamp(timestampNow))
            timeCheat = GetCheatTimeInput(curTime)
        else:  # Cheat đúng mốc thời gian
            curHour = int(dataTime[1])
            curMinute = int(dataTime[2])
            
            d = int(dataTime[0]) + curDate
            if d > numDay:  # Tăng tháng lên 1, số ngày bắt đầu lại
                curMonth = curMonth + 1
                curDate = d - numDay
            else:
                curDate = d
                
            if curMonth > 12:  # Tăng năm lên 1, sô tháng bắt đầu lại
                curYear = curYear + 1
                curMonth = curMonth - 12
            timeCheat = "%s-%s-%s %s:%s:0" %(curYear, curMonth, curDate, curHour, curMinute)
    else:
        timeCheat = GetCheatTimeInput(time)
                
    print("Cheat time to %s" %timeCheat)
    
    # Thực hiện cheat time sau khi đã xác định được các thông số cần thiết
    a = api_postDoFunction(GetCurUId(), CHEAT_TIME, ["%s" %timeCheat.split(" ")[0],"%s" %timeCheat.split(" ")[1]])
    return a

# Phân tách DateTime: d/m/Y/H/M
# type of "time": datetime
def SeparateTime(time): 
    return "%s/%s/%s/%s/%s" %(time.strftime("%d"), time.strftime("%m"), time.strftime("%Y"), time.strftime("%H"), time.strftime("%M")) 

# Định dạng lại time ở btn Cheat thành: h/m/Y/H/M
def GetCurTime():
    txtDateTime = poco(TXT_TIME_SERVER).get_text().split(" - ")
    txtTime = txtDateTime[0].split(":")
    txtDate = txtDateTime[1].split(":")
    return "%s/%s/%s/%s/%s" %(txtDate[0], txtDate[1], txtDate[2], txtTime[0], txtTime[1])

# Định dạng lại time Cheat theo format param cheat: d-m-Y H:M:S
# "time": d/m/Y/H/M
def GetCheatTimeInput(time):
    curTime = time.split("/")
    curDate = int(curTime[0])
    curMonth = int(curTime[1])
    curYear = int(curTime[2])
    curHour = int(curTime[3])
    curMinute = int(curTime[4])
    return "%s-%s-%s %s:%s:0" %(curYear, curMonth, curDate, curHour, curMinute)

# ========================== Get User Current Data ========================== 

def GetUserModel():
    uId = GetCurUId()
    return api_getModel(uId, USER_MODEL)

def GetLevelVIPInGame():
    poco(NODE_AVATAR).offspring(AVATAR).click()
    for i in range(4):
        if exists(userVIP[i]):
            poco(BTN_CLOSE).click()
            print("User Level VIP %s" % i)
            break
    return i
    
def GetCurUId():
    poco(NODE_AVATAR).offspring(AVATAR).click()
    uId = poco(TXT_USER_ID).get_text()
    print("---------Current ID: %s" % uId)
    poco(BTN_CLOSE).click()
    return uId

# ========================== Write log ========================== 

# Kiểm tra xem show hình ảnh đúng mong đợi hay không rồi ghi log
# isExist: Check hình A có đang show không
# Nếu mong đợi là CÓ SHOW thì để isExists = True
# Nếu mong đợi là KHÔNG show thì để isExists = False
def CheckImgExists(caseId, step, content, isPoco=True, isExists=True, timeWait=1):
    ST.FIND_TIMEOUT_TMP = timeWait
    isEx = False
    if isPoco:
        isEx = content.exists()
    else:
        isEx = exists(content)
    if isEx:
#         print("Found %s" % content)
        WriteLogRunning(caseId, step, content, True, isExists)
    else:
#         print("Not Found %s" % content)
        WriteLogRunning(caseId, step, content, True, not isExists)

# Kiểm tra text hiển thị đúng hay sai rồi ghi log
def CheckTxtExists(txtInGame, txtCompare, caseId, step):
    if txtCompare in txtInGame:
        WriteLogRunning(caseId, step, txtCompare, False, True)
    else:
        WriteLogRunning(caseId, step, txtCompare, False, False, txtInGame)     
        
# Ghi log, áp dụng cho check Image, Gold
def WriteLogRunning(caseId, step, content, isImg, isPass, txtInGame=""):
    global tcPass, lastCheckPoint
    global arrRs
    des = step
    img = ""
    reason = ""
    timeFail = ""
    timeInterval = ""
    if isPass:
        if not isImg:
            des = "%s %s" %(step, content)
        stt = "Pass"
        lastCheckPoint = True
    else:
        failTime = datetime.datetime.now()
        if isImg:
            print("\n%s   |   %s   |   [FAIL]\n" % (caseId, step))
            content = "%s" % content
            if content[:2] == "P(":
                content = content[2:content.find(')')]
            print("\n   |   Find: %s\n" % content)
            url = generateScreenshotName(runningDevice, failTime)
            screenShot = snapshot(url)
            print("\n   |   Actual: %s\n" % (screenShot))
            img = url 
            reason = "Image --#-- Ingame"
        else:
            des = "%s %s" %(step, content)
            if txtInGame == "":
                print("\n%s   |   %s:   |   [FAIL]\n" % (caseId, des))
                url = generateScreenshotName(runningDevice, failTime)
                screenShot = snapshot(url)
                img = url
            else:
                url = generateScreenshotName(runningDevice, failTime)
                screenShot = snapshot(url)
                img = url
                print("\n%s   |   %s --#-- In Game: %s   |   [FAIL]\n" % (caseId, des, txtInGame))
                reason = "Expect: %s --#-- In Game: %s" %  (content, txtInGame)
        timeFail = str(failTime)[:str(failTime).find('.')]
        print('\n   |   Fail time: %s\n' %timeFail)
        stt = "Fail"
        periodTime = int(failTime.timestamp()) - int(timeStart.timestamp())
        timeInterval = "Phút " + str(periodTime // 60) + ":" + str(periodTime % 60)
        lastCheckPoint = False
        tcPass = False
        
    arrRs.append({
        'content': str(caseId) + " - " + des,
        'status': stt,
        'image': img,
        'reason': reason,
        'time': timeFail,
        'interval': timeInterval
    })
