from CloverGame import GlobalVariable as Global


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



def clickButton(buttonPosition):
    Global.device.touch(buttonPosition[0], buttonPosition[1], MonkeyDevice.DOWN_AND_UP)





def getStateFromImage(MonkeyImage sourceImage):
    findBestState = False
    for i in range(0,7):
        notReliveButtonImage = sourceImage.getSubImage(Global.notReliveButtonRect)
        if notReliveButtonImage.sameAs(Global.NotReliveButtonImageOrign, SAME_AS_PRECENT):
            cloverState = State.EndlessModeReliveState
            break
        endlessModeImage = sourceImage.getSubImage(Global.endlessModeRect)
        if endlessModeImage.sameAs(Global.EndlessModeButtonImageOrign, SAME_AS_PRECENT):
            cloverState = State.ReadyToEntryEndlessMode
            break
        offenseButtonImage = sourceImage.getSubImage(Global.offenseButtonRect)
        if offenseButtonImage.sameAs(Global.OffenseButtonImageOrign, SAME_AS_PRECENT):
            cloverState = State.EndlessModeRankings
            break
        getGiftsButtonImage = sourceImage.getSubImage(Global.getGiftsButtonRect)
        if getGiftsButtonImage.sameAs(Global.GetGiftsButtonImageOrign, SAME_AS_PRECENT):
            cloverState = State.EndlessModeGetGiftsState
            break;
        continueButtonImage = sourceImage.getSubImage(Global.continueButtonRect)
        if continueButtonImage.sameAs(Global.ContinueButtonImageOrign):
            cloverState = State.ContinueEndlessModeState
            break
    gotoNextScenery(cloverState)
    return cloverState

def gotoNextScenery(cloverState):
    print cloverState
    if cloverState is State.Idle:
        getStateFromImage(Global.device.takeSnapshot())
        return
    if cloverState is State.ReadyToEntryEndlessMode:
        clickButton(Global.endlessModeButtonPosition)
        cloverState = State.EndlessModeRankings
        getStateFromImage(Global.device.takeSnapshot())
        return
    if cloverState is State.EndlessModeRankings:
        clickButton(Global.offenseButtonPosition)
        cloverState = State.EndlessModeSelectComradInArms
        getStateFromImage(Global.device.takeSnapshot())
        return
    if cloverState is State.EndlessModeSelectComradInArms:
        clickButton(Global.offenseButtonPosition)
        cloverState = State.EndlessModeBuyWeapon
        getStateFromImage(Global.device.takeSnapshot())
        return
    if cloverState is State.EndlessModeBuyWeapon:
        clickButton(Global.offenseButtonPosition)
        cloverState = State.EndlessModeAttacking
        getStateFromImage(Global.device.takeSnapshot())
        return
    if cloverState is State.EndlessModeAttacking:
        battling()
        return
    if cloverState is State.EndlessModeReliveState:
        clickButton(Global.notRelivePosition)
        cloverState = State.EndlessModeGetGiftsState
        getStateFromImage(Global.device.takeSnapshot())
        return
    if cloverState is State.EndlessModeGetGiftsState:
        clickButton(Global.getGiftsButtonPosition)
        cloverState = State.ContinueEndlessModeState
        getStateFromImage(Global.device.takeSnapshot())
        return
    if cloverState is State.ContinueEndlessModeState:
        cloverState = State.ReadyToEntryEndlessMode
        gotoNextScenery(cloverState)

def battling():
#    battlingThread = BattlingThread()
#    battlingThread.start()
    shouldBeStop = False
    while not shouldBeStop:
        tempState = getStateFromImage(Global.device.takeSnapshot)
        if tempState is State.EndlessModeReliveState:
            shouldBeStop = True

if __name__ == "__main__":
    initEnvironment()
    initAllResources()
    cloverState = State.Idle
    gotoNextScenery(cloverState)
