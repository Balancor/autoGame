__author__ = 'haiming'
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice, MonkeyImage

class GlobalEnvironment:

    def initAllResources(self):
        self.AnouncementImageOrign = MonkeyRunner.loadImageFromFile("anouncementImage_orign.png")
        self.ContinueButtonImageOrign = MonkeyRunner.loadImageFromFile("continueButtonImage_orign.png")
        self.EndlessModeButtonImageOrign = MonkeyRunner.loadImageFromFile("endlessModeButtonImage_orign.png")
        self.GetGiftsButtonImageOrign = MonkeyRunner.loadImageFromFile("getGiftsButtonImage_orign.png")
        self.NotReliveButtonImageOrign = MonkeyRunner.loadImageFromFile("notReliveButtonImage_orign.png")
        self.OffenseButtonImageOrign = MonkeyRunner.loadImageFromFile("offenseButtonImage_orign.png")

        self.offenseButtonPosition = (520, 1700)
        self.endlessModeButtonPosition = (300, 1700)
        self.battleplaneoOrignalPosition = (540, 1600)
        self.notRelivePosition = (350,1020)
        self.getGiftsButtonPosition = (520, 1320)
        self.continueButtonPosition = (300, 1630)
        self.iKnownThisAnouncementPosition =(378, 222)

        self.endlessModeRect = (80, 1640, 300, 90)
        self.offenseButtonRect = (460, 1670, 170, 80)
        self.notReliveButtonRect = (280, 990, 150, 60)
        self.getGiftsButtonRect = (460, 1280, 150, 70)
        self.continueButtonRect = (220, 1590, 150, 60)
        self.cloverAnouncementRect = (344,160, 386, 60)

    def initEnvironment(self):
        pass

    def __init__(self):
        self.networkConnectionTimeout = 25
        self.deviceConnectedToHostTimeout = 5
        self.myNexus5DeviceId = "0443370a22087dec"
        try:
            self.device = MonkeyRunner.waitForConnection(self.deviceConnectedToHostTimeout, self.myNexus5DeviceId)
        except :
            print "Cannot connect to the device"
            raise  RuntimeError("Cannot connect to device")
        self.initAllResources()

