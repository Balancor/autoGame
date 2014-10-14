from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice, MonkeyImage
from GlobalVariable import  GlobalEnvironment
from enum import Enum
import time
import gc
import threading
import thread
import traceback

State = Enum("State", 'Idle ReadyToEntryEndlessMode EndlessModeRankings EndlessModeAttacking EndlessModeReliveState EndlessModeGetGiftsState ContinueEndlessModeState')
"""
class BattlingThread(threading.Thread):
    def getSnapshotAndGotoNextState(self):
        shouldBeStop = False
        while not shouldBeStop:
            sourceImage = device.takeSnapshot()
            tempState = getStateFromImage(sourceImage)
            if tempState is State.EndlessModeReliveState:
                shouldBeStop = True
"""

SAME_AS_PRECENT = 0.9
#waitForConnection(timeout, deviceId)

packageName = "com.tencent.clover"
activityName = "com.tencent.clover.Clover"
"""
runComponent = packageName+'/'+activityName
if not device:
    device.startActivity(runComponent);
"""



def clickButton(globalEnvironment, buttonPosition):
    print "clickButton"
    print "will click position (",buttonPosition[0],buttonPosition[1],")"
    globalEnvironment.device.touch(buttonPosition[0], buttonPosition[1], MonkeyDevice.DOWN_AND_UP)

def gotoNextScenery(globalEnvironment, state):
    print "gotoNextScenery"
    print state
    if (state == State.Idle) or (state == State.ReadyToEntryEndlessMode):
        clickButton(globalEnvironment, globalEnvironment.endlessModeButtonPosition)
        return
    if state is State.EndlessModeRankings:
        clickButton(globalEnvironment, globalEnvironment.offenseButtonPosition)
        time.sleep(0.5)
        clickButton(globalEnvironment, globalEnvironment.offenseButtonPosition)
        time.sleep(0.5)
        clickButton(globalEnvironment, globalEnvironment.offenseButtonPosition)
        time.sleep(0.5)
        return
    if state is State.EndlessModeAttacking:
        if not isAttacking:
            thread.start_new_thread(battling)
        return
    if state is State.EndlessModeReliveState:
        clickButton(globalEnvironment, globalEnvironment.notRelivePosition)
        return
    if state is State.EndlessModeGetGiftsState:
        clickButton(globalEnvironment, globalEnvironment.getGiftsButtonPosition)
        return
    if state is State.ContinueEndlessModeState:
        gotoNextScenery(globalEnvironment, state)

def setCloverState(state):
    print "setcloverState"
    print state
    lock.acquire()
    cloverState = state
    lock.release()
    pass

def getStateFromImage(globalEnvironment, sourceImage):
    print "getStateFromImage"
    findBestState = False
    for i in range(0,7):
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

def battling():
#    battlingThread = BattlingThread()
#    battlingThread.start()
    shouldBeStop = False
    isAttacking = True
    while not shouldBeStop:
        print "battling"
        print cloverState
        time.sleep(5.0)
        if cloverState is State.EndlessModeReliveState:
            shouldBeStop = True
    isAttacking = False


def startGame(globalEnvironment):
    print "startGame"
    isAttacking = False
    while True:
        thread.start_new_thread(getStateFromImage, (gameGlobal, globalEnvironment.device.takeSnapshot()))
        print "in startGame"
        print cloverState
        gotoNextScenery(globalEnvironment, cloverState)
        time.sleep(0.5)


if __name__ == "__main__":
    gameGlobal = GlobalEnvironment()
    print gameGlobal.device
    if not gameGlobal.device:
        raise Exception("Cannot connect to device")
#    gameGlobal.initEnvironment()
#    gameGlobal.initAllResources()
#    gotoNextScenery(gameGlobal, cloverState)
    global isAttacking
    global cloverState
    global lock
    lock = threading.Lock()
    cloverState = State.Idle
    startGame(gameGlobal )
