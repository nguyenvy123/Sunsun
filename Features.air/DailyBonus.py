# -*- encoding=utf8 -*-
__author__ = "LinhDNA"

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

auto_setup(__file__)
fName = "Daily Bonus"

def runDailyBonus():
    log_r = open(log_running, "w")
    log_r.write("\nStart test " + fName + ":\n")
    log_r.close()
    
    global arrRs
    global testCaseName
    if lastCheckPoint:
        try:
            StartGame("1", "acctest1")
            
        except:
            url = generateScreenshotName(fName)
            img = snapshot(filename=url)
            arrRs.append({
                'content': "Crash when check " + fName,
                'status': "CRASH",
                'image': url,
                'reason': ""
            })