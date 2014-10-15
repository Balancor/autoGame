from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice, MonkeyImage
from GlobalVariable import  GlobalEnvironment
from enum import Enum
import time
import gc
import threading
import thread
import traceback
import random

State = Enum("State", 'Idle ReadyToEntryEndlessMode EndlessModeRankings EndlessModeAttacking EndlessModeReliveState EndlessModeGetGiftsState ContinueEndlessModeState')
cloverState = State.Idle

SAME_AS_PRECENT = 0.9

packageName = "com.tencent.clover"
activityName = "com.tencent.clover.Clover"


def clickButton(buttonPosition):
    global globalEnvironment
    print "clickButton (",buttonPosition[0],buttonPosition[1],")"
    globalEnvironment.device.touch(buttonPosition[0], buttonPosition[1], MonkeyDevice.DOWN_AND_UP)

def gotoNextScenery():
    global globalEnvironment
    global  cloverState
    print "gotoNextScenery", cloverState
    if (cloverState == State.Idle) or (cloverState == State.ReadyToEntryEndlessMode):
        time.sleep(0.5)
        clickButton(globalEnvironment.endlessModeButtonPosition)
        return
    if cloverState is State.EndlessModeRankings:
        time.sleep(0.5)
        clickButton(globalEnvironment.offenseButtonPosition)
        return
    if cloverState is State.EndlessModeReliveState:
        time.sleep(0.5)
        clickButton(globalEnvironment.notRelivePosition)
        return
    if cloverState is State.EndlessModeGetGiftsState:
        time.sleep(0.5)
        clickButton(globalEnvironment.getGiftsButtonPosition)
        return
#    if cloverState is State.ContinueEndlessModeState:
#        gotoNextScenery()

def setCloverState(state):
    global  cloverState
    print "setcloverState ", state
    cloverState = state


def getStateFromImage():
    global globalEnvironment
    sourceImage = globalEnvironment.device.takeSnapshot()
    for i in range(0,7):
        heBombsImage = sourceImage.getSubImage(globalEnvironment.HEBombsRect)
        if heBombsImage.sameAs(globalEnvironment.HEBombsImageOrign, 0.2):
            setCloverState(State.EndlessModeAttacking)
            break
        notReliveButtonImage = sourceImage.getSubImage(globalEnvironment.notReliveButtonRect)
        if notReliveButtonImage.sameAs(globalEnvironment.NotReliveButtonImageOrign, SAME_AS_PRECENT):
            setCloverState(State.EndlessModeReliveState)
            break
        endlessModeImage = sourceImage.getSubImage(globalEnvironment.endlessModeRect)
        if endlessModeImage.sameAs(globalEnvironment.EndlessModeButtonImageOrign, SAME_AS_PRECENT):
            setCloverState(State.ReadyToEntryEndlessMode)
            break
        offenseButtonImage = sourceImage.getSubImage(globalEnvironment.offenseButtonRect)
        if offenseButtonImage.sameAs(globalEnvironment.OffenseButtonImageOrign, SAME_AS_PRECENT):
            setCloverState(State.EndlessModeRankings)
            break
        getGiftsButtonImage = sourceImage.getSubImage(globalEnvironment.getGiftsButtonRect)
        if getGiftsButtonImage.sameAs(globalEnvironment.GetGiftsButtonImageOrign, SAME_AS_PRECENT):
            setCloverState(State.EndlessModeGetGiftsState)
            break;
        continueButtonImage = sourceImage.getSubImage(globalEnvironment.continueButtonRect)
        if continueButtonImage.sameAs(globalEnvironment.ContinueButtonImageOrign):
            setCloverState(State.ContinueEndlessModeState)
            break
    del sourceImage
    gc.collect()

def avoidBombs():
    print "avoidBombs"
    moveToRight = False
    xPosition = 550
    yPositon = 1560
    for i in range(0,50):
        xoffset = random.randint(20, 200)
        yoffset = random.randint(10,100)
        if moveToRight:
            xPositionEnd = xPosition+ xoffset
            yPositonEnd = yPositon + yoffset
        else:
            xPositionEnd = xPosition - xoffset
            yPositonEnd = yPositon - yoffset
            if xPositionEnd < 0 or yPositonEnd < 0:
                xPosition = 550
                yPositon = 1560
        print  "moveToRight",moveToRight, "start (",xPosition,",",yPositon,").  EndPosition (",xPositionEnd,",",yPositonEnd,")"
        globalEnvironment.device.drag((xPosition, yPositon), (xPositionEnd, yPositonEnd),0.5, 100)
        if xPositionEnd > 900:
            moveToRight = False
        elif xPosition < 300:
            moveToRight = True
        xPosition = xPositionEnd
        yPositon = yPositonEnd

def battling():
    global globalEnvironment
    global  cloverState
    shouldBeStop = False
    time.sleep(15)
    while True:
        print "battling", cloverState
        getStateFromImage()
        if cloverState != State.EndlessModeAttacking:
            break
        avoidBombs()


def startGame():
    global globalEnvironment
    global  cloverState
    isAttacking = False
    while True:
        getStateFromImage()
        time.sleep(2)
        print "in startGame", cloverState
        if cloverState is State.EndlessModeAttacking:
            battling()
        if cloverState is State.ContinueEndlessModeState:
            gotoNextScenery()
            break
        gotoNextScenery()
#    if cloverState is State.EndlessModeAttacking:
#        thread.start_new_thread(battling, (globalEnvironment))
#        return


if __name__ == "__main__":
    global isAttacking
    global cloverState
    global globalEnvironment
    globalEnvironment = GlobalEnvironment()
    if not globalEnvironment.device:
        raise Exception("Cannot connect to device")
    cloverState = State.Idle
    startGame()
