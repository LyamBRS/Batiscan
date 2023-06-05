#====================================================================#
# File Information
#====================================================================#
"""
    UDP.py
    ======
    This file contains a rxThread class much like UDP, LeftBrSpand,
    Accelerometer and so on. This rxThread class's purpose is to handle
    receptions and transmissions of UDP data to and from Batiscan
    in threads to avoid lag.
"""
#====================================================================#
# Loading Logs
#====================================================================#
from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog import LoadingLog
from Libraries.BRS_Python_Libraries.BRS.Network.UDP.sender import UDPSender
from Libraries.BRS_Python_Libraries.BRS.PnP.controls import Controls
from Local.Drivers.Batiscan.Programs.Communications.planes import ExecuteArrivedPlane
LoadingLog.Start("UDP.py")
#====================================================================#
# Imports
#====================================================================#
#region ------------------------------------------------------ Python
LoadingLog.Import("Python")
import time
import threading

#endregion
#region --------------------------------------------------------- BRS
LoadingLog.Import("Libraries")
# from Libraries.BRS_Python_Libraries.BRS.Utilities.bfio import BFIO
from Libraries.BRS_Python_Libraries.BRS.Utilities.Enums import Execution
# from Libraries.BRS_Python_Libraries.BRS.Utilities.Information import Information
from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog import Debug
from Libraries.BRS_Python_Libraries.BRS.Network.UDP.receiver import UDPReader
from Libraries.BRS_Python_Libraries.BRS.Utilities.LanguageHandler import _
#endregion
#region -------------------------------------------------------- Kivy
LoadingLog.Import("KivyMD")
from kivymd.uix.dialog import MDDialog
from kivy.clock import Clock
#endregion
#region ------------------------------------------------------ Batiscan
LoadingLog.Import('Batiscan')
from Local.Drivers.Batiscan.Programs.Communications.bfio import PlaneIDs, SendAPlaneOnUDP, getters
from Local.Drivers.Batiscan.Programs.Controls.actions import BatiscanActions
from Libraries.BRS_Python_Libraries.BRS.Hardware.Neopixel.rgbDriverHandler import RGB, RGBModes
#endregion
#====================================================================#
# Functions
#====================================================================#
def StartUDP() -> Execution:
    """
        StartUDP:
        =========
        Summary:
        --------
        Starts UDP threads. Will return an Execution value to
        indicate how the start went. If UDP can't start, you can't
        communicate with Batiscan.

        This starts UDP reader as well.

        Returns:
        --------
        - `Execution.Passed` = UDP is started and working.
        - `Execution.Failed` = Random failure occured and UDP couldn't start.
        - `Execution.NoConnection` = UDP reader or sender could not start.
    """
    Debug.Start("StartUDP")

    UDPReader.timeoutInSeconds = 0.5
    UDPReader.port = 4211
    UDPSender.port = 4210
    UDPSender.ipAddress = "192.168.4.2"

    result = UDPReader.StartDriver()
    if(result != Execution.Passed):
        Debug.Error("Failed to start UDPReader. We won't be able to receive data from Batiscan.")
        Debug.End()
        return Execution.NoConnection

    result = UDPSender.StartDriver()
    if(result != Execution.Passed):
        Debug.Error("Failed to start UDPSender. We won't be able to send data to Batiscan.")
        Debug.End()
        return Execution.NoConnection

    result = BatiscanUDP.StartDriver()
    if(result != Execution.Passed):
        Debug.Error("Failed to start BatiscanUDP. We won't be able to send data to Batiscan.")
        Debug.End()
        return Execution.NoConnection

    # from Programs.Communications.bfio import GetUniversalInfoUpdate
    # BatiscanUDP

    Debug.End()
    return Execution.Passed

def StopUDP() -> Execution:
    """
        StopUDP:
        ========
        Summary:
        --------
        Stops all UDP threads running for Batiscan.
        This is called when the Device Driver exits to ensure
        that no stray threads are still running.
    """
    Debug.Start("StopUDP")

    result = BatiscanUDP.StopDriver()
    if(result != Execution.Passed):
        Debug.Error("Failed to stop BatiscanUDP.")
        Debug.End()
        return Execution.NoConnection

    result = UDPReader.StopDriver()
    if(result != Execution.Passed):
        Debug.Error("Failed to stop UDPReader.")
        Debug.End()
        return Execution.NoConnection

    result = UDPSender.StopDriver()
    if(result != Execution.Passed):
        Debug.Error("Failed to stop UDPSender.")
        Debug.End()
        return Execution.NoConnection
    
    Debug.End()
    return Execution.Passed
#====================================================================#
# Classes
#====================================================================#
class BatiscanUDP:
    """
        BatiscanUDP:
        ========
        Summary:
        --------
        Class made to create a rxThread
        that handles :ref:`UDPReader` and :ref:`UDPSender` for
        Batiscan to use for their things.

        This class will parse incoming planes, generate outgoing
        planes and much more.
    """

    rxThread = None
    """ private thread object from :ref:`Threading`."""
    txThread = None
    """ private thread object from :ref:`Threading`."""
    stop_event = threading.Event()
    isStarted: bool = False
    rxLock = threading.Lock()
    txLock = threading.Lock()

    NoConnectionDialog = MDDialog()
    ConnectionFoundDialog = MDDialog()
    noConnectionCounter = 0
    dialogShown:bool = False

    @staticmethod
    def _RXThread(udpClass, ExecutePlane, Getters, Controls:Controls, StateFlippers:BatiscanActions, kontrolRGB:RGB):

        from Local.Drivers.Batiscan.Programs.Communications.planes import MakeAPlaneOutOfArrivedBytes

        while True:
            if udpClass.stop_event.is_set():
                break
            ##################################################
            arrivals:list = []
            while True:
                oldestMessage = UDPReader.GetOldestMessage()
                if(oldestMessage != None):
                    for sender,message in oldestMessage.items():
                        # Debug.Log(f"New plane from {sender}:")
                        arrivals.append(MakeAPlaneOutOfArrivedBytes(message))
                else:
                    break
            ##################################################
            if udpClass.stop_event.is_set():
                break

            try:
                with udpClass.rxLock:
                    arrived:bool = False

                    if(arrivals != None):
                        if(len(arrivals) > 0):
                            for arrival in arrivals:
                                if(arrival != None):
                                    arrived = True
                                    ExecutePlane(arrival)
                    if not arrived:
                        udpClass.noConnectionCounter = udpClass.noConnectionCounter + 1
                    else:
                        udpClass.noConnectionCounter = 0

                    if(udpClass.noConnectionCounter == 5):
                        udpClass._NoConnection()

                    if udpClass.noConnectionCounter > 5 and arrived:
                        udpClass._ConnectionFound()
       
                    arrivals.clear()
            except:
                pass
        udpClass.isStarted = False

    @staticmethod
    def _TXThread(udpClass, ExecutePlane, Getters, Controls:Controls, StateFlippers:BatiscanActions, kontrolRGB:RGB):

        count:int = 0
        planeToSend = None
        from Libraries.BRS_Python_Libraries.BRS.PnP.controls import SoftwareAxes, SoftwareButtons

        batiscanAxesActions = {
            SoftwareAxes.pitch_up    : 0,
            SoftwareAxes.pitch_down  : 0,
            SoftwareAxes.roll_left   : 0,
            SoftwareAxes.roll_right  : 0,
            SoftwareAxes.yaw_left    : 0,
            SoftwareAxes.yaw_right   : 0,
            SoftwareAxes.up          : 0,
            SoftwareAxes.down        : 0
        }
        """
            A list of all the software axes being used by Batiscan when its
            GUI is loaded and going and their associated descriptions. 
            The names within this list are extracted from :ref:`Controls`. 
            :ref:`SoftwareAxis` and this dictionary is used to keep old
            values to avoid useless updates and planes sent to Batiscan.
        """

        batiscanButtonsActions = {
        SoftwareButtons.fill         : False,
        SoftwareButtons.empty        : False,
        SoftwareButtons.reset        : False,
        SoftwareButtons.forward      : False,
        SoftwareButtons.backward     : False,
        SoftwareButtons.up           : False,
        SoftwareButtons.down         : False,
        SoftwareButtons.left         : False,
        SoftwareButtons.right        : False,
        SoftwareButtons.on           : False,
        SoftwareButtons.off          : False,
        SoftwareButtons.custom_1     : False,
        SoftwareButtons.custom_2     : False
        }
        """
            A list of all the software buttons being used by Batiscan when its
            GUI is loaded and going and their associated descriptions. 
            The names within this list are extracted from :ref:`Controls`. 
            :ref:`SoftwareButtons`
        """

        def CurrentButtonValue(name:str) -> bool:
            """
                CurrentButtonValue:
                ===================
                Summary:
                --------
                Allows you to quickly get the
                real button value. False is returned
                if the button in question isn't
                binded.

                Returns:
                --------
                - `None` = Software button is not binded or binded but getter is `None`.
                - `(bool)` = Button is binded and that's their current state.
            """
            if(Controls._buttons[name]["binded"]):
                if(Controls._buttons[name]["getter"] != None):
                    newValue = Controls._buttons[name]["getter"]()
                    return newValue
            return None

        def Handle_Button(SoftwareName:str, stateFlippersFunction:BatiscanActions, planeID:PlaneIDs):
            """
                Handler_Button:
                ===============
                Summary:
                --------
                This function's purpose is to
                handle the sending of a specific
                plane on UDP if a specific software
                button is pressed.

                The plane is sent if the button is
                `True` and was `False` previously.
                The current value is saved in 
                `batiscanButtonsActions`
            """
            currentButtonState = CurrentButtonValue(SoftwareName)
            if(currentButtonState != None):
                if(batiscanButtonsActions[SoftwareName] != currentButtonState): # State of the button changed
                    batiscanButtonsActions[SoftwareName] = currentButtonState
                    if(currentButtonState == True):
                        # with udpClass.rxLock:
                            # print("locked-C")
                        stateFlippersFunction()
                        SendAPlaneOnUDP(planeID, Getters)
                        time.sleep(0.030)

        def _GetAxis(softwareName:str, associatedButtonName:str = None) -> float:
            """
                returns a float value from 0 to 1.
                returns `None` if the axis is not binded
                in :ref:`Controls`.
            """
            pressed:bool = None
            if(associatedButtonName != None):
                pressed = CurrentButtonValue(associatedButtonName)

                # The button is pressed, we bypass the axis reading.
                if(pressed):
                    return 1

            if(Controls._axes[softwareName]["binded"] == True):
                return Controls._axes[softwareName]["getter"]()
            else:
                # The axis is not binded, maybe the button was?
                if(pressed == False):
                    # Button is binded and released, so 0 is returned
                    return 0
                else:
                    # No button, no axis, no bitches is binded to this axis.
                    return None

        def Handle_NavigationAxis(softwareNamePositive:str, softwareNameNegative:str, softwareNameButtonPositive:str, softwareNameButtonNegative:str, axisUpdateFunction):
            """
                Handle_NavigationAxis:
                ======================
                Summary:
                --------
                This function handles the setting of a wanted
                specific submarine axis such as yaw, pitch, roll,
                camera angle and speed. It needs 2 software axis.
                One for the positive aspect of that axis and one
                for the negative aspect of that axis. Optionally,
                it can also take software buttons which will
                bypass software axis if their current state is
                `True`.

                Arguments:
                ----------
                Please note that all software buttons and software axes within the following list
                are strings located either in `SoftwareAxes` or in `SoftwareButtons`. Both of which
                are listed in BRS_Python_Libraries in `BRS/PnP/controls.py`

                - `softwareNamePositive:str` = name of the software axis that is used to make that axis go in the positive.
                - `softwareNameNegative:str` = name of the software axis that is used to make that axis go in the negative.
                - `softwareNameButtonPositive:str` = Optional button that bypasses the positive axis and makes it go full positive when their current state is `True`.
                - `softwareNameButtonNegative:str` = Optional button that bypasses the negative axis and makes it go full negative when their current state is `True`.
                - `axisUpdateFunction:str` = Function taken from :ref:`BatiscanActions` that sets a new wantedValue for an axis.
            """
            positiveValue:float = None
            negativeValue:float = None

            positiveValue = _GetAxis(softwareNamePositive, softwareNameButtonPositive)
            negativeValue = _GetAxis(softwareNameNegative, softwareNameButtonNegative)

            if(positiveValue != None and negativeValue != None):
                if(positiveValue > negativeValue):
                    # with udpClass.rxLock:
                        # print("locked-B-P")
                    axisUpdateFunction(positiveValue)
                    return
                else:
                    # with udpClass.rxLock:
                        # print("locked-B-N")
                    axisUpdateFunction(-negativeValue)
                    return
            return

        def HandleAddons():
            """
                HandleAddons:
                =============
                Summary:
                --------
                Handles the sending of planes
                related to addons getters.
                See Batiscan's controls for
                more informations about this
                one.
            """
            Handle_Button(SoftwareButtons.on, StateFlippers.LightsWantedOn, PlaneIDs.lightsUpdate)
            Handle_Button(SoftwareButtons.off, StateFlippers.LightsWantedOff, PlaneIDs.lightsUpdate)
            Handle_Button(SoftwareButtons.fill, StateFlippers.BallastWantedFull, PlaneIDs.ballastUpdate)
            Handle_Button(SoftwareButtons.empty, StateFlippers.BallastWantedEmpty, PlaneIDs.ballastUpdate)
            Handle_Button(SoftwareButtons.custom_1, StateFlippers.BallastWantedEmpty, PlaneIDs.surface)
            Handle_Button(SoftwareButtons.custom_2, StateFlippers.CameraStateFlipWanted, PlaneIDs.cameraUpdate)

        def HandleAndSendNavigation():
            Handle_NavigationAxis(SoftwareAxes.forward,
                                    SoftwareAxes.backward,
                                    SoftwareButtons.forward,
                                    SoftwareButtons.backward,
                                    StateFlippers.SetNewSpeed)

            Handle_NavigationAxis(SoftwareAxes.yaw_right,
                                    SoftwareAxes.yaw_left,
                                    SoftwareButtons.left,
                                    SoftwareButtons.right,
                                    StateFlippers.SetNewYaw)

            Handle_NavigationAxis(SoftwareAxes.roll_right,
                                    SoftwareAxes.roll_left,
                                    None,
                                    None,
                                    StateFlippers.SetNewRoll)

            Handle_NavigationAxis(SoftwareAxes.pitch_up,
                                    SoftwareAxes.pitch_down,
                                    SoftwareButtons.up,
                                    SoftwareButtons.down,
                                    StateFlippers.SetNewPitch)

            Handle_NavigationAxis(SoftwareAxes.up,
                                    SoftwareAxes.down,
                                    None,
                                    None,
                                    StateFlippers.SetNewCameraAngle)

            SendAPlaneOnUDP(PlaneIDs.navigationUpdate, Getters)
            time.sleep(0.030)

        while True:
            if udpClass.stop_event.is_set():
                break
            ##################################################
            HandleAndSendNavigation()

            if(count == 3):
                # kontrolRGB.SetAttributes(lerpDelta=1, rgbMode=RGBModes.static, colors=[[0,0,0],[0,0,0],[255,255,255]])
                count = 0

            if(count == 2):
                # kontrolRGB.SetAttributes(lerpDelta=1, rgbMode=RGBModes.static, colors=[[0,0,0],[255,255,255],[0,0,0]])
                HandleAddons()
                count = 3

            if(count == 1):
                # kontrolRGB.SetAttributes(lerpDelta=1, rgbMode=RGBModes.static, colors=[[255,255,255],[0,0,0],[0,0,0]])
                SendAPlaneOnUDP(PlaneIDs.allSensors, Getters)
                time.sleep(0.030)
                count = 2

            if(count == 0):
                # kontrolRGB.SetAttributes(lerpDelta=1, rgbMode=RGBModes.static, colors=[[0,0,0],[0,0,0],[0,0,0]])
                SendAPlaneOnUDP(PlaneIDs.allStates, Getters)
                time.sleep(0.030)
                count = 1

            if(planeToSend != None):
                # kontrolRGB.SetAttributes(lerpDelta=1, rgbMode=RGBModes.static, colors=[[255,255,255],[255,255,255],[255,255,255]])
                SendAPlaneOnUDP(planeToSend, Getters)
                time.sleep(0.030)
                planeToSend = None

            if udpClass.stop_event.is_set():
                break

            try:
                with udpClass.txLock:
                    planeToSend = BatiscanUDP._thingToSend
                    BatiscanUDP._thingToSend = None
            except:
                pass
        udpClass.isStarted = False


    @staticmethod
    def StartDriver():
        """
            StartDriver:
            ============
            Summary:
            --------
            Starts the UDP threads
            handled by Batiscan. returns
            Execution.Passed if successful.

            This needs to be done after you
            started :ref:`UDPReader` and :ref:`UDPSender`
        """
        Debug.Start("BatiscanUDP -> StartDriver")
        if (BatiscanUDP.isStarted == False):
            if (not BatiscanUDP.rxThread or not BatiscanUDP.rxThread.is_alive()):
                BatiscanUDP.noConnectionCounter = 0
                BatiscanUDP.stop_event.clear()
                BatiscanUDP.rxThread = threading.Thread(target=BatiscanUDP._RXThread, args=(BatiscanUDP, ExecuteArrivedPlane, getters, Controls, BatiscanActions, RGB))
                BatiscanUDP.rxThread.daemon = True
                BatiscanUDP.rxThread.start()
                BatiscanUDP.isStarted = True
                Debug.Log("BatiscanUDP is started.")
                Debug.End()
                return Execution.Passed
            
            if (not BatiscanUDP.txThread or not BatiscanUDP.txThread.is_alive()):
                BatiscanUDP.noConnectionCounter = 0
                BatiscanUDP.stop_event.clear()
                BatiscanUDP.txThread = threading.txThread(target=BatiscanUDP._TXThread, args=(BatiscanUDP, ExecuteArrivedPlane, getters, Controls, BatiscanActions, RGB))
                BatiscanUDP.txThread.daemon = True
                BatiscanUDP.txThread.start()
                BatiscanUDP.isStarted = True
                Debug.Log("BatiscanUDP is started.")
                Debug.End()
                return Execution.Passed
        else:
            Debug.Error("rxThread is already started. You cannot start more than one.")
            Debug.End()
            return Execution.Failed
        Debug.Log("BatiscanUDP is now started")
        Debug.End()
        return Execution.Passed

    @staticmethod
    def StopDriver():
        """
            StopDriver:
            ============
            Summary:
            --------
            Stops the driver from sending anymore
            UDP stuff. DOES NOT CLEAR THE BUFFER
            OF THIS CLASS
        """
        Debug.Start("BatiscanUDP -> StopDriver")
        BatiscanUDP.stop_event.set()
        if BatiscanUDP.rxThread and BatiscanUDP.rxThread.is_alive():
            BatiscanUDP.rxThread.join()
        if BatiscanUDP.txThread and BatiscanUDP.txThread.is_alive():
            BatiscanUDP.txThread.join()
        Debug.Log("rxThread is stopped.")
        Debug.End()
        return Execution.Passed

    @staticmethod
    def _NoConnection(*args):
        """
            _NoConnection:
            ==============
            Summary:
            --------
            Function executed internally
            when its been several loops that
            the UDP reader did not read any
            received UDP planes. This function
            calls an MDDialog pop up which is
            then displayed to the user.
        """
        if(not BatiscanUDP.NoConnectionDialog._is_open):
            Clock.schedule_once(BatiscanUDP.DisplayNoConnectionPopUp, 0.1)

    @staticmethod
    def _ConnectionFound(*args):
        """
            _ConnectionFound:
            =================
            Summary:
            --------
            Function executed internally
            when its been several loops that
            the UDP reader did read some
            received UDP planes after not receiving
            any for a while. This function
            calls an MDDialog pop up which is
            then displayed to the user.
        """
        if(not BatiscanUDP.ConnectionFoundDialog._is_open):
            Clock.schedule_once(BatiscanUDP.DisplayConnectionFoundPopUp, 0.1)


    def DisplayNoConnectionPopUp(*args):
        if(BatiscanUDP.ConnectionFoundDialog._is_open):
            BatiscanUDP.ConnectionFoundDialog.dismiss()

        if(BatiscanUDP.NoConnectionDialog._is_open == False):
            BatiscanUDP.NoConnectionDialog = MDDialog(
                title = _("Submarine lost"),
                text = _("It appears like Batiscan stopped / never sent any data back to Kontrol in response to Kontrol's requests to do so. If this is not normal, please immediately fetch your submarine as fast as possible.")
            )
            BatiscanUDP.NoConnectionDialog.open()
            BatiscanUDP.dialogShown = True

    def DisplayConnectionFoundPopUp(*args):
        if(BatiscanUDP.NoConnectionDialog._is_open):
            BatiscanUDP.NoConnectionDialog.dismiss()

        if(BatiscanUDP.ConnectionFoundDialog._is_open == False):
            BatiscanUDP.ConnectionFoundDialog = MDDialog(
                title = _("Submarine found"),
                text = _("Kontrol started receiving data from Batiscan. If you see these pop ups constantly, please go near Batiscan as you may currently be too far away for a proper solid connection to be established.")
            )
            BatiscanUDP.ConnectionFoundDialog.open()
            BatiscanUDP.dialogShown = True

    @staticmethod
    def SendThing(thingToSend) -> Execution:
        """
            SendThing:
            ==========
            Summary:
            --------
            Sets what to send on the UDP.
            It will be set back to `None` once
            its sent.
        """
        Debug.Start("SendThing")

        if(BatiscanUDP.isStarted):
            with BatiscanUDP.txLock:
                BatiscanUDP._thingToSend = thingToSend
            Debug.Log("New thing to send has been specified.")
        else:
            Debug.Log("txThread IS NOT STARTED. NO UDP MESSAGES CAN BE RETURNED")
            Debug.End()
            return Execution.Failed

        Debug.End()
#====================================================================#
LoadingLog.End("driver.py")