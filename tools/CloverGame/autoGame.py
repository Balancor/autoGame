from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice, MonkeyImage
import threading
import timer

class Enum(tuple): __getattr__ = tuple.index
 
State = Enum([  'Idle'
                'ReadyToConnectNetworState',
                'ReadyToStartClover',
                'AnouncementShowed',
                'ReadyToEntryEndlessMode',
                'EndlessModeRankings',
                'EndlessModeSelectComradInArms',
                'EndlessModeBuyWeapon',
                'EndlessModeAttacking'
                'EndlessModeReliveState',
                'EndlessModeGetGiftsState'
                'ContinueEndlessModeState',
            ])
class BattlingThread(threading.Thread):
    def getSnapshotAndGotoNextState(self):
        shouldBeStop = False
        while not shouldBeStop:
            sourceImage = device.takeSnapshot()
            tempState = getStateFromImage(sourceImage)
            if tempState is State.EndlessModeReliveState:
                shouldBeStop = True

networkConnectionTimeout = 25
#seconds
deviceConnectedToHostTimeout = 5
myNexus5DeviceId = "0443370a22087dec"
SAME_AS_PRECENT = 0.9
#waitForConnection(timeout, deviceId)

packageName = "com.tencent.clover"
activityName = "com.tencent.clover.Clover"

runComponent = packageName+'/'+activityName
if not device:
    device.startActivity(runComponent);

def initEnvironment():
    device = MonkeyRunner.waitForConnection(deviceConnectedToHostTimeout, myNexus5DeviceId)

def clickButton(buttonPosition):
    device.touch(buttonPosition[0], buttonPosition[1], MonkeyDevice.DOWN_AND_UP)


def initAllResources():
    AnouncementImageOrign = MonkeyRunner.loadImageFromFile("anouncementImage_orign.png")
    ContinueButtonImageOrign = MonkeyRunner.loadImageFromFile("continueButtonImage_orign.png")
    EndlessModeButtonImageOrign = MonkeyRunner.loadImageFromFile("endlessModeButtonImage_orign.png")
    GetGiftsButtonImageOrign = MonkeyRunner.loadImageFromFile("getGiftsButtonImage_orign.png")
    NotReliveButtonImageOrign = MonkeyRunner.loadImageFromFile("notReliveButtonImage_orign.png")
    OffenseButtonImageOrign = MonkeyRunner.loadImageFromFile("offenseButtonImage_orign.png")

    offenseButtonPosition = (520, 1700)
    endlessModeButtonPosition = (300, 1700)
    battleplaneoOrignalPosition = (540, 1600)
    notRelivePosition = (350,1020)
    getGiftsButtonPosition = (520, 1320)
    continueButtonPosition = (300, 1630)
    iKnownThisAnouncementPosition =(378, 222)

    endlessModeRect = (80, 1640, 300, 90)
    offenseButtonRect = (460, 1670, 170, 80)
    notReliveButtonRect = (280, 990, 150, 60)
    getGiftsButtonRect = (460, 1280, 150, 70)
    continueButtonRect = (220, 1590, 150, 60)
    cloverAnouncementRect = (344,160, 386, 60)

def getStateFromImage(MonkeyImage sourceImage):
    findBestState = False
    for i in range(0,7):
        notReliveButtonImage = sourceImage.getSubImage(notReliveButtonRect)
        if notReliveButtonImage.sameAs(NotReliveButtonImageOrign, SAME_AS_PRECENT):
            cloverState = State.EndlessModeReliveState
            break
        endlessModeImage = sourceImage.getSubImage(endlessModeRect)
        if endlessModeImage.sameAs(EndlessModeButtonImageOrign, SAME_AS_PRECENT):
            cloverState = State.ReadyToEntryEndlessMode
            break
        offenseButtonImage = sourceImage.getSubImage(offenseButtonRect)
        if offenseButtonImage.sameAs(OffenseButtonImageOrign, SAME_AS_PRECENT):
            cloverState = State.EndlessModeRankings
            break
        getGiftsButtonImage = sourceImage.getSubImage(getGiftsButtonRect)
        if getGiftsButtonImage.sameAs(GetGiftsButtonImageOrign, SAME_AS_PRECENT):
            cloverState = State.EndlessModeGetGiftsState
            break;
        continueButtonImage = sourceImage.getSubImage(continueButtonRect)
        if continueButtonImage.sameAs(ContinueButtonImageOrign):
            cloverState = State.ContinueEndlessModeState
            break
    gotoNextScenery(cloverState)
    return cloverState

def gotoNextScenery(cloverState)
    print cloverState
    if cloverState is State.Idle:
        getStateFromImage(device.takeSnapshot())
        return
    if cloverState is State.ReadyToEntryEndlessMode:
        clickButton(endlessModeButtonPosition)
        cloverState = State.EndlessModeRankings
        getStateFromImage(device.takeSnapshot())
        return
    if cloverState is State.EndlessModeRankings:
        clickButton(offenseButtonPosition)
        cloverState = State.EndlessModeSelectComradInArms
        getStateFromImage(device.takeSnapshot())
        return
    if cloverState is State.EndlessModeSelectComradInArms:
        clickButton(offenseButtonPosition)
        cloverState = State.EndlessModeBuyWeapon
        getStateFromImage(device.takeSnapshot())
        return
    if cloverState is State.EndlessModeBuyWeapon:
        clickButton(offenseButtonPosition)
        cloverState = State.EndlessModeAttacking
        getStateFromImage(device.takeSnapshot())
        return
    if cloverState is State.EndlessModeAttacking:
        battling()
        return
    if cloverState is State.EndlessModeReliveState:
        clickButton(notRelivePosition)
        cloverState = State.EndlessModeGetGiftsState
        getStateFromImage(device.takeSnapshot())
        return
    if cloverState is State.EndlessModeGetGiftsState:
        clickButton(getGiftsButtonPosition)
        cloverState = State.ContinueEndlessModeState
        getStateFromImage(device.takeSnapshot())
        return
    if cloverState is State.ContinueEndlessModeState:
        cloverState = State.ReadyToEntryEndlessMode
        gotoNextScenery(cloverState)


def battling():
    battlingThread = BattlingThread()
    battlingThread.start()

if __name__ == "__main__":
    initEnvironment()
    initAllResources()
    cloverState = State.Idle
    gotoNextScenery(cloverState)
