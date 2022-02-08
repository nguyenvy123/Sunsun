# -*- encoding=utf8 -*-
__author__ = "LinhDNA"

import traceback
from airtest.core.api import *
from airtest.core.api import using
using("Content.air")
from Content import *
from Features import *
using("Main.air")
from ExcelUtility import *

auto_setup(__file__)
fName = "Login"

def runLogin(deviceId):
    global arrRs
    try:
        for fn in getFunctionNeedTest(fName):
            eval(fn)
    except Exception as e:
        crashTime = datetime.datetime.now()
        url = generateScreenshotName(deviceId, crashTime)
        img = snapshot(filename = url)
        timeCrash = str(crashTime)[:str(crashTime).find('.')]
        periodTime = int(crashTime.timestamp()) - int(timeStart.timestamp())
        timeInterval = "Phút " + str(periodTime // 60) + ":" + str(periodTime % 60)
        arrRs.append({
            'content': "Crash when check " + fName,
            'status': "CRASH",
            'image': url,
            'reason': repr(e),
            'time': timeCrash,
            'interval': timeInterval
        })
        traceback.print_exc() 
        
# --------------------------------------Login---------------------------------------

# Start game với accName được truyền vào (trên 6 kí tự). 
# Nếu accName chưa có trong list thì sẽ check Register account đó
def StartGame(caseId, accName): 
    if len(accName) < 6:
        WriteLogRunning(caseId, "Login Fail - Account name is too short", "", False, False)
        return
    isRegister = False
    idAccLogin = -1
    for i in range(len(nameLogin)):
        if nameLogin[i] == accName: # Có sẵn trong list
            idAccLogin = i
            break
    if idAccLogin < 0:  # Không có trong list thì check đăng kí
        isRegister = True
    if poco(BTN_PLAY).exists(): # Đã login từ trước
        ClosePopups()
        print("Already logged in game")
        curId = GetCurUId()
        if isRegister:  # Register account mới
            LogOut()
            LoginZAcc(caseId, accName, isRegister)
            ClosePopups()
            CheckImgExists(caseId, "Register account %s" %accName, poco(BTN_VIP), True)
        else: # Login account được chỉ dịnh    
            if curId != userId[idAccLogin]:
                LogOut()
                LoginZAcc(caseId, accName, isRegister)
                ClosePopups()
            CheckImgExists(caseId, "Login game by account %s" %accName, poco(BTN_VIP), True)
    else:
        if exists(loginFB): # Chưa login, đang show form login FB
            keyevent("BACK")
            sleep(10)
        CheckImgExists(caseId, "At scene login", poco(BTN_GUEST), True)
        if poco(BTN_GUEST).exists():
            LoginZAcc(caseId, accName, isRegister)
            ClosePopups()
            CheckImgExists(caseId, "Log into game", poco(BTN_VIP), True, True, 3)
    
def LogOut():
    poco(BTN_SETTING).click()
    poco(BTN_LOG_OUT).click()
    
def LoginZAcc(caseId, accName, isRegister): #Chưa check new user có tutorial
    poco(BTN_CHEAT).click([0.5,0.5])
    poco(BTN_ZACC).click([0.5,0.5])
    poco(BOX_NAME).click([0.5,0.5])
    for i in range(10):
        keyevent("KEYCODE_DEL")
    text(accName)
    poco(BOX_PASS).click([0.5,0.5])
    for i in range(10):
        keyevent("KEYCODE_DEL")
    text(passLogin)
    if isRegister: 
        poco(BTN_REGISTER).click([0.5,0.5])
    else: 
        poco(BTN_LOGINZ).click([0.5,0.5])
    sleep(15)
    if poco(text = NOTIFICATION).exists():
        poco(BTN_OK).click()
        if poco(text = TXT_ACC_EXISTS).exists():
            WriteLogRunning(caseId, "Register Fail - Account %s already exists" %accName, "", False, False)
        if poco(text = TXT_ACC_INCORRECT).exists():
            WriteLogRunning(caseId, "Login Fail - Username/Pass is invalid", "", False, False)  
        poco(BTN_OUT_LOGINZ).click([0.5,0.5])