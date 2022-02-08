# -*- encoding=utf8 -*-
__author__ = "LinhDNA"

from airtest.core.api import *
from poco.drivers.cocosjs import CocosJsPoco

auto_setup(__file__)
poco = CocosJsPoco()

# =========================== General =========================== 

NOTIFICATION = "NOTIFICATIONS"
BTN_CLOSE = "btnClose"
BTN_OK = "btnOk"
TITLE_GUI = "lbTitle"
TXT_GOLD = "lbGold"
# List payment
PAYMENT = "lvPayment"
# UI nhận quà chung
CONGRATS = "congrats"
NODE_GOLD_VPOINT = "nodeGoldVPoint"
BTN_RECEIVE = "btnReceive"
BTN_BACK = "btnBack"
BTN_EXIT = "btnExit"

# =========================== Login =========================== 

BTN_GUEST = "btnGuest"
BOX_NAME = "ebLoginUsername"
BOX_PASS = "ebLoginPass"
BTN_LOGINZ = "btnLogin"
BTN_REGISTER = "btnRegister"
TXT_ACC_EXISTS = "Akun sudah ada."
TXT_ACC_INCORRECT = "Nama pengguna/Kata sandi salah,"
BTN_OUT_LOGINZ = "btnBack"
loginFB = Template(r"tpl1609905107210.png", record_pos=(-0.006, -0.104), resolution=(1280, 720))

# =========================== Logout =========================== 

BTN_LOG_OUT = "btnLogout"

# =========================== Lobby =========================== 

BTN_VIP = "spineVip"
BTN_SELECT_TABLE = "spineJoinTable"
BTN_PLAY = "spinePlayNow"
NODE_AVATAR = "avatarPlayer"
AVATAR = "sprite"
BTN_SHOP = "spineShop"
BTN_MAIL = "btnMail"
BTN_RANKING = "btnRanking"
FEATURE_WC = "FeatureWeeklyChallenge"
BTN_DEAL_WC = "events/weekly_challenge/event_wc_join"
FEATURE_DB = "FeatureDailyBonus"
BTN_FEATURE = "btnClick"
BTN_SETTING = "btnSetting"
BTN_TUTORIAL = "btnTut"
TXT_GOLD_LOBBY = "lbGold"

# =========================== Profile =========================== 

TXT_USER_ID = 'lbID'

# =========================== In Table ===========================

BTN_LEAVE_GAME = "btnExit"
HAND_START = "table_start"
NODE_JACKPOT = "nodeJackpot"

NODE_SCORE = "nodeScore"
TXT_TOP_POINT = "lbText0"
TXT_MIDDLE_POINT = "lbText1"
TXT_BOTTOM_POINT = "lbText2"
TXT_TOTAL_POINT = "lbTextTotal"

EFFECT_WIN = "table_winner_glow"

# =========================== Tutorial =========================== 

BTN_GO = "btnCallBack"
BTN_SKIP = "btnSkip"
IMG_HAND = "hand.png"

# =========================== Support =========================== 

SUPPORT = "SOPORTE" # Text in popup Gold Support
BTN_CLAIM_SUPPORT = "btnGet"

# =========================== Daily Bonus =========================== 

TXT_DAY_BONUS = "lbDay"
TXT_TIME_REMAIN = "lbTimeRemain"
BTN_CLAIM_BONUS = "fx_btn_collect"
SLOT_DAY = "nodeDay" #imgDay1-7
IMG_TICK = "imgTick"
EFFECT_TODAY = "imgFxLight"
TXT_TODAY = "Today"

# =========================== Event WC =========================== 

# TITLE_GUI = 'lbTitle'
POPUP_WC = "imgTouch"
BTN_ACTION = "spineBtnAction"
BTN_WC_IN_TABLE = 'WCProgressTable'
PROGRESS_IN_TABLE = "lbPercent"

TITLE_WC = "Weekly challenge" 
NODE_DAY = "nodeDay"
TXT_DAY_MISSION = "_lbDay"
IMG_NOT_COMPLETE = "_imgEnd"
IMG_COMPLETE = "_imgTick"
TXT_TOTAL_ITEM = "lbTotalItem"

TXT_DAY_CHALLENGE = "lbDayChallenge"
TXT_MISSION_DETAIL = "lbMissionDetail"
TXT_PROGRESS = "lbProgress"
TXT_ITEM_REWARD = "lbItem"
TXT_GOLD_REWARD = "lbGoldReward"
TXT_ACTION = "lbAction"
ACT_PLAY_NOW = "Play Now"
ACT_CLAIM = "Claim"
TXT_THANK = "lbThankYou"

TITLE_DEAL = "Sweet deals" 
NODE_OFFER = "nodeOffer"
TXT_VPOINT = "lbVpoint"
TXT_BONUS = "lbBonus"
TXT_AVAILABLE = "lbAvailable"
TXT_TIME_LEFT = "lbTimeLeft"
TXT_PRICE = "lbPrice"
NODE_BOUGHT = "nodeBought"

# =========================== Popup Claim Gold =========================== 

BG_REASON = 'bgReason'
TXT_REASON = 'lbReason'
GOOD_LUCK = "Buena suerte" # Text in popup claim reward's new user
BUY_SUCCESS = "Compra existosa"
IMG_GOLD = "imgGold"
# TXT_GOLD = "lbGold"
BTN_CLAIM_REWARD = 'btnClaim'

# =========================== Ranking =========================== 

TXT_CLAIM = "lbtextClaim"
TOP_CONGRAT = "¡Muy Bien! ¡sigues asi!"
GUI_RANKING = "Power hand Ranking"
GUI_END_RANKING = "features/ranking_power/ranking_power_title"
BTN_CONFIRM = "btnConfirm"

# =========================== Offers =========================== 

GUI_OFFER_1ST = "imgTitleBanner"
BTN_BUY = "btnBuy"
BTN_SHOP_NOW = "btnShopNow"

GUI_OFFER_NEW_USER = Template(r"tpl1611715298105.png", record_pos=(0.013, -0.18), resolution=(1600, 720))

# =========================== Shop - VIP =========================== 

GUI_SHOP = "lvShop"

# Node vị trí quyền lợi VIP
POS_VIP = ["imgSilkNone", "imgSilkBroze", "imgSilkSliver", "imgSilkGold"]
TXT_BENEFIT = "lbBenefit" # Text các quyền lợi VIP
# TXT_PRICE = "lbBtnBroze"
BTN_BUY = ["","btnBuyBroze","btnBuySilver","btnBuyGold"]

TXT_BTN_EXTEND = 'textClaim'
BTN_PARTICIPATE = "Participamos juntos"  # Text in popup Almost Extend VIP
BTN_EXTEND = "Extender" # Text in popup Extend VIP
THANK_VIP = "VIP" # Text in popup claim gold tribute VIP
BTN_OK_EXTEND = 'btnOk'

BTN_TAB_VIP = 'btnVip' # Tab VIP trong shop
BTN_OUT_VIP = 'btnClose' # Thoát GUI VIP
BTN_CLAIM = "btnClaim" # Nhận gold sau khi mua VIP

LIST_ITEMS = "listViewInteraction"
ITEMS_TYPE = "lbType"
ITEM = "btnInteraction_"
TOOLTIP = "lbToolTip"
userVIP = [Template(r"tpl1611130909528.png", record_pos=(0.163, -0.081), resolution=(1600, 720)),Template(r"tpl1605090605831.png", record_pos=(0.185, -0.088), resolution=(2220, 1079)),Template(r"tpl1605090498049.png", record_pos=(0.189, -0.089), resolution=(2220, 1079)),Template(r"tpl1605090530530.png", record_pos=(0.167, -0.089), resolution=(2220, 1079))]
nameVIP = [Template(r"tpl1606887698654.png", record_pos=(0.081, -0.044), resolution=(1920, 1080)),Template(r"tpl1606887712097.png", record_pos=(0.082, -0.043), resolution=(1920, 1080)),Template(r"tpl1606887729969.png", record_pos=(0.083, -0.044), resolution=(1920, 1080))]
btnClose = Template(r"tpl1606888648129.png", record_pos=(0.239, -0.167), resolution=(1920, 1080))
btnCancel = Template(r"tpl1606888660369.png", record_pos=(-0.101, 0.096), resolution=(1920, 1080))
btnOK = Template(r"tpl1606888670489.png", record_pos=(0.098, 0.095), resolution=(1920, 1080))
confirmBuyGG = [Template(r"tpl1606890070577.png", record_pos=(-0.277, 0.031), resolution=(1920, 1080)),Template(r"tpl1606892441305.png", record_pos=(-0.245, -0.256), resolution=(1920, 1080))]
itemThrow = Template(r"tpl1606893239210.png", record_pos=(-0.236, 0.147), resolution=(1920, 1080))

# =========================== Cheat =========================== 

BTN_CHEAT = 'CheatButton'
BTN_CHEAT_PLAYER = "CheatPlayer"
BTN_CHEAT_2M = "2M"
CHEAT_GOLD = "cheat gold"
BTN_CHEAT_PRIVATE = "Cheat"
BOX_GOLD = 'ebGold'
BTN_SEND_CHEAT = 'btnSendCheatPlayer'
BTN_ADD_BOT = "AddBot" 
TXT_TIME_SERVER = "TimeServer"
BTN_ZACC = "Zacc"
TXT_TC_ID = "___tcId___"
BTN_CHEAT_TC = "TestCase"
TXT_POINT = "cheat point"
BTN_SEND = "Send"