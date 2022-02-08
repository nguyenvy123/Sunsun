# -*- encoding=utf8 -*-
__author__ = "LinhDNA"
import datetime
import traceback
from airtest.core.api import *
from airtest.core.api import using
using("Content.air")
from Content import *
from Features import *
from Login import *
using("Constant.air")
from Constant import *
using("Main.air")
from ExcelUtility import *
using("ConfigReader")
from ConfigReader import ConfigReader

# poco = UnityPoco()
auto_setup(__file__)
fName = "EventWC"

config = ConfigReader()
configChallenge = config.getConfigByElement(EVENT_WC_JS, "Challenge")
configOtherInfo = config.getConfigByElement(EVENT_WC_JS, "Misc")
configOffers = config.getConfigByElement(EVENT_WC_JS, "Offers")
configWCExtra = config.getConfigByElement(EXTRA_JS, "WCMission")
configTCLogic = config.getConfigByElement(EXTRA_JS, "TCLogicCoreGame")

showTime = configOtherInfo["openTime"] #- timeDelta
startTime = configOtherInfo["startTime"] #- timeDelta
endTime = configOtherInfo["finishTime"] #- timeDelta

def runEventWC(deviceId):
    runFunctions(fName, deviceId)
            
def runEventWC_1(dId):
    runFunctions(fName + "_1", deviceId)
    
def runEventWC_2(dId):
    runFunctions(fName + "_2", deviceId)

def runFunctions(name, deviceId):
    try:
        for fn in getFunctionNeedTest(name):
            print("Running Function: " + fn)
            eval(fn)
    except Exception as e:
        global arrRs
        crashTime = datetime.datetime.now()
        url = generateScreenshotName(deviceId, crashTime)
        img = snapshot(url)
        timeCrash = str(crashTime)[:str(crashTime).find('.')]
        periodTime = int(crashTime.timestamp()) - int(timeStart.timestamp())
        timeInterval = "Phút " + str(periodTime // 60) + ":" + str(periodTime % 60)
        arrRs.append({
            'content': "Crash when check " + name,
            'status': "CRASH",
            'image': url,
            'reason': repr(e),
            'time': timeCrash,
            'interval': timeInterval
        })
        traceback.print_exc() 
                
# ========================= Functions - Event WC ========================= 

def NextDayInTable(caseId):
    dayId = GetCurDayId()
    PlayGameOverNight()
    poco(TXT_TOTAL_POINT).wait_for_appearance()
    if dayId + 1 >= len(configChallenge): # Last Challenge Day
        CheckImgExists(caseId, "Last Day, Hide Event Progress In Table", poco(PROGRESS_IN_TABLE), True, False)
    else:
        CheckTxtExists(poco(PROGRESS_IN_TABLE).get_text(), "0/%s" %configChallenge[dayId + 1]["threshold"], caseId, "Next Day, Update Challenge In Table:")
    poco(BTN_PLAY).wait_for_appearance(ONE_HAND_MAX_TIME)
    sleep(SHOW_GUI_TIME)
    ClosePopups()
    if dayId >= len(configChallenge): # Last day
        WriteLogRunning(caseId, "End Event In Table, Back to Lobby Not Auto Show GUI Event", "", False, not CheckPopupVisible(EVENT_WC))
        WriteLogRunning(caseId, "End Event In Table, Back to Lobby Not Auto Show GUI Deal", "", False, not CheckPopupVisible(DEAL_WC))
        CheckShowBtnEvent(caseId, False)
    else:
        WriteLogRunning(caseId, "Next Day In Table, Back to Lobby Auto Show GUI Event", "", False, CheckPopupVisible(EVENT_WC))
        CheckAutoShowDeal(caseId)
    CheckShowChallengesData(caseId, dayId + 1)
    
def NextDayAtLobby(caseId, hasCheatTime = True):
    dayId = GetCurDayId()
    if hasCheatTime:
        CheatTime("0 23 59")
    sleep(timeDelta * 1.5)
    ClosePopups()
    if dayId >= len(configChallenge): # Last day
        WriteLogRunning(caseId, "End Event At Lobby, Not Auto Show GUI Event", "", False, not CheckPopupVisible(EVENT_WC))
        WriteLogRunning(caseId, "End Event At Lobby, Not Auto Show GUI Deal", "", False, not CheckPopupVisible(DEAL_WC))
    else:        
        WriteLogRunning(caseId, "Next Day At Lobby, Auto Show GUI Event", "", False, CheckPopupVisible(EVENT_WC))
        CheckAutoShowDeal(caseId)
        CheckShowChallengesData(caseId, dayId + 1)
    
def NextDayInGUIEvent(caseId, hasCheatTime = True):
    uId = GetCurUId()
    dayId = GetCurDayId()
    if hasCheatTime:
        CheatTime("0 23 59")
    poco(FEATURE_WC).click()
    sleep(timeDelta * 1.5)
    if poco(TITLE_GUI, text = TITLE_WC).exists():
        CheckData(caseId, dayId + 1, uId)
    WriteLogRunning(caseId, "Next Day In GUI Event, Not Auto Hide GUI Event", "", False, poco(TITLE_GUI, text = TITLE_WC).exists())
    ClosePopups()
    if dayId >= len(configChallenge): # Last day
        WriteLogRunning(caseId, "End Event In GUI Event, Auto Hide GUI Event When it's openning", "", False, not CheckPopupVisible(EVENT_WC))
        WriteLogRunning(caseId, "End Event In GUI Event, Not Auto Show GUI Deal Event", "", False, not CheckPopupVisible(DEAL_WC))
    else:
        CheckAutoShowDeal(caseId)

def NextDayInGUIDeal(caseId, hasCheatTime = True):
    dayId = GetCurDayId()
    if hasCheatTime:
        CheatTime("0 23 59")
    poco(BTN_DEAL_WC).click()
    sleep(timeDelta * 1.5)
    ClosePopups()
    if dayId >= len(configChallenge): # Last day
        WriteLogRunning(caseId, "End Event In GUI Deal, Auto Hide GUI Deal When it's openning", "", False, not CheckPopupVisible(DEAL_WC))
        WriteLogRunning(caseId, "End Event In GUI Deal, Not Auto Show GUI Event", "", False, not CheckPopupVisible(EVENT_WC))
    else:        
        CheckAutoShowDeal(caseId)
        CheckShowChallengesData(caseId, dayId + 1)

def CheckAutoShowDeal(caseId):
    uId = GetCurUId()
    dealStt = api_getModel(uId, WC_MODEL)["statusOffers"]
    isOutOfDeal = True
    for packId in range(len(configOffers)):
        if configOffers[packId]["quantityAvailable"] != dealStt[packId]:
            isOutOfDeal = False
            break
    if isOutOfDeal:
        WriteLogRunning(caseId, "Out Of Deal, Not Auto Show GUI Deal", "", False, not CheckPopupVisible(DEAL_WC))
    else: 
        WriteLogRunning(caseId, "Has Deal, Auto Show GUI Deal", "", False, CheckPopupVisible(DEAL_WC))
 
def CheckShowBtnEvent(caseId, isShow = True):
    if isShow:
        step = "Start Event, Show Btn"
    else:
        step = "End Event, Hide Btn"
    CheckImgExists(caseId, "%s Deal" %step, poco(BTN_DEAL_WC), True, isShow)
    CheckImgExists(caseId, "%s Event" %step, poco(FEATURE_WC), True, isShow)
       
def DoChallengesNotEnoughMoney(caseId):
    CheatGold(minGold - 1)
    poco(FEATURE_WC).click()
    if poco(TXT_ACTION, text = ACT_PLAY_NOW).exists():
        poco(BTN_ACTION).click()
        isShowNoti = poco(TITLE_GUI, text = NOTIFICATION).exists()
        if isShowNoti:
            poco(BTN_OK).click()
            poco(BTN_BACK).click()
        WriteLogRunning(caseId, "Play Now From GUI Event, But Not Enough Money", "", False, isShowNoti)
    
def ClaimRewards(caseId, isClaim = True):
    uId = GetCurUId()
    CheatGold(minGold)
    lastGold = minGold
    poco(FEATURE_WC).click()
    
    if not poco(TXT_ACTION, text = ACT_CLAIM).exists():
        WriteLogRunning(caseId, "Can not Claim Reward, Hide Btn Claim", "", False, True)
        return
    
    if not isClaim:
        poco(BTN_CLOSE).click()
        CheckUpdateGold(caseId, CompactGold(lastGold), "Close GUI Event, Not Receive Rewards")
        return
    
    dayId = GetCurDayId()
    totalTicket = int(poco(TXT_TOTAL_ITEM).get_text())
    
    poco(TXT_ACTION, text = ACT_CLAIM).click()
    sleep(COUNT_DOWN_TIME)
    CheckImgExists(caseId, "Claim Reward Day %s, Hide Btn Claim" %(dayId + 1), poco(TXT_ACTION, text = ACT_CLAIM), True, False)
    
    if dayId < len(configChallenge):
        slot = "%s%s" %(NODE_DAY, dayId)
        CheckImgExists(caseId, "Claim Reward Day %s, Show Tick Img" %(dayId + 1), poco(slot).child(IMG_COMPLETE))
        
        totalTicket += configChallenge[dayId]["ticketReward"]
        CheckTxtExists(poco(TXT_TOTAL_ITEM).get_text(), "%s" %totalTicket, caseId, "Claim Reward Day %s, Update Total Ticket Client:" %(dayId + 1))
        wcModel = api_getModel(uId, WC_MODEL)
        CheckTxtExists("%s" %wcModel["totalTicket"], "%s" %totalTicket, caseId, "Claim Reward Day %s, Update Total Ticket Server:" %(dayId + 1))
        
        lastGold += configChallenge[dayId]["goldReward"]
    else:
        lastGold += totalTicket * configOtherInfo["ticketPrice"]
        poco(BTN_CLOSE).click() # Touch out to receive
    poco(BTN_CLOSE).click()
    CheckUpdateGold(caseId, CompactGold(lastGold), "Claim Reward Day %s, Update Gold" %(dayId + 1))
   
def CheatChallengeComplete(caseId, almostComplete = False):
    poco(FEATURE_WC).click()
    if not poco(TXT_POINT).exists():
        poco(BTN_CHEAT).click()
    poco(TXT_POINT).click()
    dayId = GetCurDayId()
    for i in range(2):
        keyevent("KEYCODE_DEL")
    dayId = GetCurDayId()
    if not almostComplete:
        text(str(configChallenge[dayId]["threshold"]))
        poco(BTN_SEND).click()
        CheckImgExists(caseId, "Challenge is Completed, Show Btn Claim", poco(TXT_ACTION, text = ACT_CLAIM))
    else:
        text(str(int(configChallenge[dayId]["threshold"]) - 1))
        poco(BTN_SEND).click()
    poco(BTN_CHEAT).click()
    poco(BTN_CLOSE).click()
    
# Do mission everyday
def DoChallenges(caseId, tcLogicId, numDelay = 0):
    sleep(COUNT_DOWN_TIME * numDelay)
    uId = GetCurUId()
    uGold = api_getModel(uId, USER_MODEL)["gold"]
    if uGold < minGold:
        CheatGold(minGold)
        
    wcModel = api_getModel(uId, WC_MODEL)
    challengeStt = wcModel["statusChallenges"]
    
    dayId = GetCurDayId()
    point = wcModel["points"]  
    print("Point before: %s" %point)
    
    isCompletedNow = True # Mission was completed or not, while this function is running
    if point >= configChallenge[dayId]["threshold"]:
        isCompletedNow = False
    
    poco(FEATURE_WC).click()
    JoinTable(caseId, isCompletedNow)
    
    # Play logic test cases 
    CheatTestCaseLogic(configTCLogic[tcLogicId - 1]["id"])
    poco(EFFECT_WIN).wait_for_appearance(ONE_HAND_MAX_TIME) # Wait for ending point calculator

    txtTop = poco(TXT_TOP_POINT).get_text()
    txtMid = poco(TXT_MIDDLE_POINT).get_text()
    txtBot = poco(TXT_BOTTOM_POINT).get_text()
    pTop = pMid = pBot = 0
    if not txtTop == "":
        pTop = CaculatePoint(txtTop.split(" ")[1], configTCLogic[tcLogicId - 1]["competitor"])
    if not txtMid == "": 
        pMid = CaculatePoint(txtMid.split(" ")[1], configTCLogic[tcLogicId - 1]["competitor"])
    if not txtBot == "":
        pBot = CaculatePoint(txtBot.split(" ")[1], configTCLogic[tcLogicId - 1]["competitor"])
    pSum = int(poco(TXT_TOTAL_POINT).get_text().split(" ")[2])
    print ("pTop: %s, pMid: %s, pBot: %s, pSum: %s" %(pTop, pMid, pBot, pSum))
    
    if configChallenge[dayId]["challengeId"] == PLAY_GAME:
        point += 1
        print("Point Play Game: %s" %point)
    if pSum > 0 and configChallenge[dayId]["challengeId"] == WIN_POINT:
        point = point + pSum
        print("Point Win Point: %s" %point)
    if pTop > 0 and configChallenge[dayId]["challengeId"] == WIN_IN_TOP:
        point = point + pTop
        print("Point Win in Top: %s" %point)
    if pMid > 0 and configChallenge[dayId]["challengeId"] == WIN_IN_MIDDLE:
        point = point + pMid
        print("Point Win in Middle: %s" %point)
    if pBot > 0 and configChallenge[dayId]["challengeId"] == WIN_IN_BOTTOM:
        point = point + pBot
        print("Point Win in Bottom: %s" %point)
    if configChallenge[dayId]["challengeId"] == CATCH_OTHER: 
        point = point + configTCLogic[tcLogicId - 1]["catch"]
        print("Point Catch Other: %s" %point)
    if point >= configChallenge[dayId]["threshold"]:
        point = configChallenge[dayId]["threshold"]
    else:
        isCompletedNow = False
    print("Updated Point: %s" %point)
    
    poco(BTN_LEAVE_GAME).click()
    poco(BTN_PLAY).wait_for_appearance(ONE_HAND_MAX_TIME)
    sleep(COUNT_DOWN_TIME)
    ClosePopups()
    
    hasShowEvent = CheckPopupVisible(EVENT_WC)
    if point == configChallenge[dayId]["threshold"]:
        if isCompletedNow:
            wcModel = api_getModel(uId, WC_MODEL)
            CheckTxtExists(str(wcModel["lastDayCanClaim"]), "%s" %dayId, caseId, "Update Last Day Can Claim on Server:")
            CheckTxtExists(str(wcModel["statusChallenges"][dayId]), "1", caseId, "Update Challenge Complete on Server:")
            WriteLogRunning(caseId, "Challenge Complete, Auto Show GUI Event", "", False, hasShowEvent)
        else:
            WriteLogRunning(caseId, "Challenge Was Completed Before, Auto Show GUI Event", "", False, hasShowEvent)
    else:
        WriteLogRunning(caseId, "Challenge Haven't Completed Yet, Not Auto Show GUI Event", "", False, not hasShowEvent)
    if not hasShowEvent:
        poco(FEATURE_WC).click()
        CheckTxtExists(poco(TXT_PROGRESS).get_text(), "%s/%s" %(point, configChallenge[dayId]["threshold"]), caseId, "Update Progress In GUI Event:")
        poco(BTN_CLOSE).click()

def LeaveTableNotStarted(caseId):    
    uId = GetCurUId()
    uGold = api_getModel(uId, USER_MODEL)["gold"]
    if uGold < minGold:
        CheatGold(minGold)
        
    wcModel = api_getModel(uId, WC_MODEL)
    challengeStt = wcModel["statusChallenges"]
    
    dayId = GetCurDayId()
    point = wcModel["points"] 
    isCompletedNow = True # Mission was completed or not, while this function is running
    if point >= configChallenge[dayId]["threshold"]:
        isCompletedNow = False
    
    poco(FEATURE_WC).click()
    CheckTxtExists(poco(TXT_PROGRESS).get_text(), "%s/%s" %(point, configChallenge[dayId]["threshold"]), caseId, "Show Point Data:")
    JoinTable(caseId, isCompletedNow)
    
    if not poco(NODE_JACKPOT).exists():
        WriteLogRunning(caseId, "Play Now from GUI Event", "", False, False)
        return
    
    # Leave table when game is not started
    poco(BTN_LEAVE_GAME).click()
    ClosePopups()
    poco(FEATURE_WC).click()
    CheckTxtExists(poco(TXT_PROGRESS).get_text(), "%s/%s" %(point, configChallenge[dayId]["threshold"]), caseId, "Not Play Game, Not Update Progress:")
    poco(BTN_CLOSE).click()

# Check visible btn PlayNow in GUI Event
def JoinTable(caseId, isCompletedNow):
    if isCompletedNow:
        CheckImgExists(caseId, "Challenge has not Completed yet, Show Btn Play Now", poco(TXT_ACTION, text = ACT_PLAY_NOW))
        poco(BTN_ACTION).click()
    else:
        CheckImgExists(caseId, "Challenge was Completed, or Reward was Claimed, Hide Btn Play Now", poco(TXT_ACTION, text = ACT_PLAY_NOW), True, False)
        poco(BTN_CLOSE).click()
        poco(BTN_PLAY).click() # Cheat
    sleep(SHOW_GUI_TIME) # Wait for showing join table effect
    
def CaculatePoint(txtPoint, numPlayer):
    if txtPoint.count("(") <= 0:
        point = int(txtPoint)
    else:
        point = int(txtPoint.split("(")[0])
    point = int((point + numPlayer - 1)/2)
    print("Point: %s" %point)
    return point 
                    
# Receive data from server and then compare them with client    
def CheckShowChallengesData(caseId, dayId = -1):
    uId = GetCurUId()
    poco(FEATURE_WC).click()
    if dayId < 0:
        dayId = GetCurDayId()
    if poco(TXT_ACTION, text = ACT_CLAIM).exists():
        sleep(SHOW_GUI_TIME*3)    # Wait for auto claim reward
    CheckData(caseId, dayId, uId)
    poco(BTN_CLOSE).click()    
    
def CheckData(caseId, dayId, uId):
    wcModel = api_getModel(uId, WC_MODEL)
    challengeStt = wcModel["statusChallenges"]
    for i in range(len(challengeStt)):
        if i < len(challengeStt) - 1:   # Normal day
            slot = "%s%s" %(NODE_DAY, i)
            if i < dayId and challengeStt[i] <= 0:
                CheckImgExists(caseId, "Not Complete Day %s Challenge, Hide Tick Img" %(i + 1), poco(slot).child(IMG_COMPLETE), True, False)
                CheckImgExists(caseId, "Not Complete Day %s Challenge, Show End Img" %(i + 1), poco(slot).child(IMG_NOT_COMPLETE))
            if i <= dayId and challengeStt[i] > 0:  
                CheckImgExists(caseId, "Complete Day %s Challenge, Hide End Img" %(i + 1), poco(slot).child(IMG_NOT_COMPLETE), True, False)
                if i == dayId and wcModel["lastDayCanClaim"] == dayId:
                    CheckImgExists(caseId, "Today Challenge Completed, Reward Haven't Claimed Yet, Hide Tick Img", poco(slot).child(IMG_COMPLETE), True, False)
                    CheckImgExists(caseId, "Today Challenge, Show Btn Claim", poco(TXT_ACTION, text = ACT_CLAIM))
                else:
                    CheckImgExists(caseId, "Complete Day %s Challenge, Show Tick Img" %(i + 1), poco(slot).child(IMG_COMPLETE))
            if i > dayId:  
                CheckImgExists(caseId, "Next Day %s Challenge, Hide Tick Img" %(i + 1), poco(slot).child(IMG_COMPLETE), True, False)
                CheckImgExists(caseId, "Next Day %s Challenge, Hide End Img" %(i + 1), poco(slot).child(IMG_NOT_COMPLETE), True, False)
            if i == dayId and challengeStt[i] <= 0:
                CheckImgExists(caseId, "Today Challenge, Hide Tick Img", poco(slot).child(IMG_COMPLETE), True, False)
                CheckImgExists(caseId, "Today Challenge, Hide End Img", poco(slot).child(IMG_NOT_COMPLETE), True, False)
                CheckImgExists(caseId, "Today Challenge, Show Btn Play Now", poco(TXT_ACTION, text = ACT_PLAY_NOW))
        else:   # Last day
            totalItem = wcModel["totalTicket"]
            CheckTxtExists(poco(TXT_TOTAL_ITEM).get_text(), "%s" %totalItem, caseId, "Total item:")
            if dayId == i:
                if totalItem > 0:
                    txtGoldReward = RemoveSeparator(poco(TXT_GOLD_REWARD).get_text(), ",")
                    CheckTxtExists(CompactGold(int(txtGoldReward)), CompactGold(configOtherInfo["ticketPrice"] * totalItem), caseId, "Last day reward:")
                    CheckImgExists(caseId, "Last Day, Have Rewards, Show Btn Claim", poco(TXT_ACTION, text = ACT_CLAIM))
                else:
                    
                    CheckImgExists(caseId, "Last Day, Have No Rewards, Hide Btn Claim", poco(TXT_ACTION, text = ACT_CLAIM), True, False)
    CheckConfig(caseId, dayId, uId)
 
def CheckConfig(caseId, dayId, uId):
    if dayId >= len(configChallenge): # Last day
        return
    txtInGame = poco(TXT_DAY_CHALLENGE).get_text()
    CheckTxtExists(txtInGame, "Day %s challenge" %(dayId + 1), caseId, "")

    txtInGame = poco(TXT_MISSION_DETAIL).get_text()
    CheckTxtExists(txtInGame, configWCExtra[configChallenge[dayId]["challengeId"]].replace("-", str(configChallenge[dayId]["threshold"])), caseId, "Mission Detail:")

    wcModel = api_getModel(uId, WC_MODEL)
    txtInGame = poco(TXT_PROGRESS).get_text()
    CheckTxtExists(txtInGame, "%s/%s" %(wcModel["points"], configChallenge[dayId]["threshold"]), caseId, "Progress:")

    txtInGame = poco(TXT_ITEM_REWARD).get_text()
    CheckTxtExists(txtInGame, "%s" %configChallenge[dayId]["ticketReward"], caseId, "Day %s Item Reward:" %(dayId + 1))

    txtInGame = poco(TXT_GOLD_REWARD).get_text()
    CheckTxtExists(CompactGold(int(RemoveSeparator(txtInGame, ","))), CompactGold(configChallenge[dayId]["goldReward"]), caseId, "Day %s Gold Reward:" %(dayId + 1))
                
# Mua Deal, nhận và check kết quả
def BuyAllDeal(caseId):
    if not poco(BTN_DEAL_WC).exists():
        WriteLogRunning(caseId, "Can't buy Deal, because sold out or Don't have event", "", True, True) 
        return
    
    uId = GetCurUId()
    dealStt = api_getModel(uId, WC_MODEL)["statusOffers"]
    CheatGold(minGold)
    lastGold = minGold
    poco(BTN_DEAL_WC).click()
    
    for packId in range(len(configOffers)):
        for num in range(configOffers[packId]["quantityAvailable"]):
            slot = "%s%s" %(NODE_OFFER, packId)
            if dealStt[packId] >= configOffers[packId]["quantityAvailable"]:
                CheckImgExists(caseId, "Can't buy Deal %s because sold out" %(packId + 1), poco(slot).child(NODE_BOUGHT), True, False)
                break
            poco(slot).offspring(TXT_PRICE).click()
            poco(PAYMENT).click()
            if poco(CONGRATS).exists():
                # Buy successfully
                WriteLogRunning(caseId, "Buy Deal %s successfully" %(packId + 1), poco(CONGRATS), True, True)
                goldReceive = poco(NODE_GOLD_VPOINT).child(TXT_GOLD).get_text()
                goldReceive = RemoveSeparator(goldReceive.split("+")[1], ",")
                CheckTxtExists(CompactGold(int(goldReceive)), CompactGold(configOffers[packId]["gold"]), caseId, "Buy Deal %s, Gold Receive:" %(packId + 1))
                lastGold += int(goldReceive)
                txtCompare = CompactGold(lastGold)
                poco(BTN_RECEIVE).click()
                # Check deals remain
                dealRemain = configOffers[packId]["quantityAvailable"] - dealStt[packId] - 1
                if dealRemain > 0:
                    txtInGame = poco(slot).offspring(TXT_AVAILABLE).get_text()
                    CheckTxtExists(txtInGame, "%s/%s" %(dealRemain, configOffers[packId]["quantityAvailable"]), caseId, "Deal Remain Client:")
                else:
                    CheckImgExists(caseId, "Out of Deal %s" %(packId + 1), poco(slot).child(NODE_BOUGHT), True, False)
                dealRemain = dealStt[packId] + 1
                dealStt = api_getModel(uId, WC_MODEL)["statusOffers"]
                CheckTxtExists(str(dealStt[packId]), "%s" %dealRemain, caseId, "Deal Remain Server:")
            else:
                WriteLogRunning(caseId, "Buy Deal %s successfully" %(packId + 1), poco(CONGRATS), True, False) 
    poco(BTN_CLOSE).click()
    ClosePopups()
    CheckImgExists(caseId, "Buy All Deal, Hide Btn Deal At Lobby", poco(BTN_DEAL_WC), True, False)
    CheckUpdateGold(caseId, txtCompare, "Buy Deal %s Update Gold")
    
def GetCurDayId():
    aCurTime = GetCurTime().split("/")
    curTimeStamp = datetime.datetime(int(aCurTime[2]), int(aCurTime[1]), int(aCurTime[0]), int(aCurTime[3]), int(aCurTime[4])).timestamp()
    curDay = int((curTimeStamp - startTime)/24/3600)
    print ("Event Day: %s" %curDay)
    return curDay
    
# Định dạng lại start time: d/m/Y/H/M
def GetStartTime():
    dStart = datetime.datetime.fromtimestamp(startTime - timeDelta)
    return SeparateTime(dStart)
    
def CheckDealsConfig(caseId):
    poco(BTN_DEAL_WC).click()
    for i in range(len(configOffers)):
        slot = "%s%s" %(NODE_OFFER, i)
        txtInGame = poco(slot).offspring(TXT_BONUS).get_text()
        CheckTxtExists(txtInGame, "%s" % int(configOffers[i]["rate"] * 100) + "%", caseId, "Bonus of Deal %s:" %(i + 1))
        
        txtInGame = RemoveSeparator(poco(slot).child(TXT_GOLD).get_text(), ",")
        CheckTxtExists(CompactGold(int(txtInGame)), CompactGold(configOffers[i]["gold"]), caseId, "Bonus of Deal %s:" %(i + 1))
        
        txtInGame = RemoveSeparator(poco(slot).child(TXT_VPOINT).get_text(), ",")
        CheckTxtExists(txtInGame, "%s" %configOffers[i]["vPoint"], caseId, "Gold of Deal %s:" %(i + 1))
        
        txtInGame = poco(slot).offspring(TXT_PRICE).get_text()
        txtInGame = RemoveSeparator(txtInGame.split("Rp ")[1], ".")
        CheckTxtExists(txtInGame, "%s" %configOffers[i]["cost"], caseId, "Price of Deal %s:" %(i + 1))
        
        txtInGame = poco(slot).offspring(TXT_AVAILABLE).get_text()
        CheckTxtExists(txtInGame, "%s/%s" %(configOffers[i]["quantityAvailable"], configOffers[i]["quantityAvailable"]), caseId, "Quantity of Deal %s - " %(i + 1))
    poco(BTN_CLOSE).click()
        
def StartEventAtLobby(caseId):
    if showTime < startTime:    # Nếu event có config time show event trước khi start event
        dShow = datetime.datetime.fromtimestamp(showTime)
        timeCheat = SeparateTime(dShow)   
        CheatTime(timeCheat)
        sleep(COUNT_DOWN_TIME)
        ClosePopups()
        sleep(timeDelta)
        CheckImgExists(caseId, "Start event, auto show btn Event in Lobby", poco(FEATURE_WC))
        ClosePopups()
        CheckImgExists(caseId, "Start event, reload Lobby show btn Event", poco(FEATURE_WC))
        poco(FEATURE_WC).click()
        CheckImgExists(caseId, "Click btn event, show popup Event coming soon", poco(POPUP_WC))
    
    timeCheat = GetStartTime()
    print("timeStart %s" %timeCheat)
#     timeCheat = "12/7/2021/23/59"
    CheatTime(timeCheat)
    sleep(COUNT_DOWN_TIME)
    ClosePopups()
    sleep(timeDelta)
    ClosePopups(False, False)
    CheckStartEvent(caseId, "At Lobby")
    poco(FEATURE_WC).click()
    sleep(SHOW_GUI_TIME)
    CheckImgExists(caseId, "Click Btn Event, Show GUI Event", poco(TITLE_GUI, text = TITLE_WC))
    poco(BTN_CLOSE).click()
    
def StartEventInTable(caseId):
    if showTime < startTime:
        sleep(COUNT_DOWN_TIME)
        ClosePopups()
        sleep(timeDelta) # Play multi-device in case showTime < startTime
    sleep(COUNT_DOWN_TIME)
    ClosePopups()
    poco(BTN_PLAY).click([0.5,0.5])
    sleep(timeDelta)
    CheckImgExists(caseId, "Start Event In Table, Show Event Progress", poco(PROGRESS_IN_TABLE))
    poco(BTN_LEAVE_GAME).click()
    ClosePopups()
    CheckStartEvent(caseId, "In Table")
    
def StartEventInShop(caseId):
    if showTime < startTime:
        sleep(COUNT_DOWN_TIME)
        ClosePopups()
        sleep(timeDelta) # Play multi-device in case showTime < startTime
    sleep(COUNT_DOWN_TIME)
    ClosePopups()
    poco(BTN_SHOP).click([0.5,0.5])
    sleep(timeDelta)
    poco(BTN_BACK).click()  
    ClosePopups()
    CheckStartEvent(caseId, "In Shop")
    
def CheckStartEvent(caseId, posStart):
    WriteLogRunning(caseId, "Start Event %s, Auto Show Popup Event" %posStart, "", False, CheckPopupVisible(POPUP_EVENT_WC))
    WriteLogRunning(caseId, "Start Event %s, Auto Show GUI Event" %posStart, "", False, CheckPopupVisible(EVENT_WC))
    WriteLogRunning(caseId, "Start Event %s, Auto Show GUI Deal" %posStart, "", False, CheckPopupVisible(DEAL_WC))
    CheckImgExists(caseId, "Start Event %s, Auto Show Btn Event" %posStart, poco(FEATURE_WC))