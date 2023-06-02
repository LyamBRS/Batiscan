#====================================================================#
# File Information
#====================================================================#
"""
    actions.py
    =============
    This file's purpose is to hold all the actions that Batiscan can
    execute from :ref:`Controls` in BRS_Python_Libraries. This
    includes functions and methods to extract values from binders as
    well as threads to constantly read from them and execute changes
    if something changes in them.
"""
#====================================================================#
# Loading Logs
#====================================================================#
from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog import LoadingLog
LoadingLog.Start("actions.py")
#====================================================================#
# Imports
#====================================================================#
#region ------------------------------------------------------ Python
# LoadingLog.Import("Python")
#endregion
#region --------------------------------------------------------- BRS
LoadingLog.Import("Libraries")
from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog import Debug
from Libraries.BRS_Python_Libraries.BRS.PnP.controls import SoftwareAxes, SoftwareButtons
from Local.Drivers.Batiscan.Programs.Controls.controls import BatiscanControls
#endregion
#region -------------------------------------------------------- Kivy
# LoadingLog.Import("Kivy")
#endregion
#region ------------------------------------------------------ KivyMD
# LoadingLog.Import('KivyMD')
#endregion
#====================================================================#
# Variables
#====================================================================#
batiscanAxesActions = {
    SoftwareAxes.pitch_up    : {"description" : "Pitch upwards"},
    SoftwareAxes.pitch_down  : {"description" : "Pitch downwards"},
    SoftwareAxes.roll_left   : {"description" : "Roll left"},
    SoftwareAxes.roll_right  : {"description" : "Roll right"},
    SoftwareAxes.yaw_left    : {"description" : "Turn left"},
    SoftwareAxes.yaw_right   : {"description" : "Turn right"},
    SoftwareAxes.up          : {"description" : "Pitch camera up"},
    SoftwareAxes.down        : {"description" : "Pitch camera down"},
    SoftwareAxes.forward     : {"description" : "Throttle forwards"},
    SoftwareAxes.backward    : {"description" : "Throttle backwards"}
}
"""
    A list of all the software axes being used by Batiscan when its
    GUI is loaded and going and their associated descriptions. 
    The names within this list are extracted from :ref:`Controls`. 
    :ref:`SoftwareAxis`

    "name" : {"description" : "description text"}
"""

batiscanButtonsActions = {
   SoftwareButtons.fill         : {"description" : "Fills the ballast"},
   SoftwareButtons.empty        : {"description" : "Empty the ballast"},
   SoftwareButtons.reset        : {"description" : "Resets batiscasn"},
   SoftwareButtons.forward      : {"description" : "Full speed forward"},
   SoftwareButtons.backward     : {"description" : "Full speed backward"},
   SoftwareButtons.up           : {"description" : "Pitch up"},
   SoftwareButtons.down         : {"description" : "Pitch down"},
   SoftwareButtons.left         : {"description" : "Yaw left"},
   SoftwareButtons.right        : {"description" : "Yaw right"},
   SoftwareButtons.on           : {"description" : "Turn On lights"},
   SoftwareButtons.off          : {"description" : "Turn Off lights"},
   SoftwareButtons.custom_1     : {"description" : "Surface immediately"},
   SoftwareButtons.custom_2     : {"description" : "Turn on/off camera"},
}
"""
    A list of all the software buttons being used by Batiscan when its
    GUI is loaded and going and their associated descriptions. 
    The names within this list are extracted from :ref:`Controls`. 
    :ref:`SoftwareButtons`

    "name" : {"description" : "description text"}
"""
#====================================================================#
# Classes
#====================================================================#
# LoadingLog.Class("BatiscanValues")
class BatiscanActions:
    # region   --------------------------- DOCSTRING
    """
        BatiscanActions:
        ================
        Summary:
        ========
        Class that contains method that are called
        by threads to update current wanted values
        based off the changes in states of hardware
        that might be binded to batiscan.
    """
    # endregion
    # region   --------------------------- MEMBERS

    # endregion
    # region   --------------------------- METHODS
    def _ClampValueToSignedChar(valueToClamp) -> int:
        """
            Makes it so the value cannot go
            below -127 and above 127
        """
        if(valueToClamp > 127):
            return 127
        if(valueToClamp < -127):
            return -127
        return valueToClamp

    def LightsWantedOn():
        BatiscanControls.wantedLeftLight = True
        BatiscanControls.wantedRightLight = True

    def LightsWantedOff():
        BatiscanControls.wantedLeftLight = False
        BatiscanControls.wantedRightLight = False

    def BallastWantedEmpty():
        BatiscanControls.wantedBallast = False

    def BallastWantedFull():
        BatiscanControls.wantedBallast = True

    def SurfaceImmediatelyWanted():
        BatiscanControls.wantedSurface = True

    def CameraStateFlipWanted():
        if(BatiscanControls.currentCameraStatus):
            BatiscanControls.wantedCameraStatus = False
        else:
            BatiscanControls.wantedCameraStatus = True      

    def SetNewYaw(floatValue:float):
        value = (floatValue*127)
        value = BatiscanActions._ClampValueToSignedChar(value)
        BatiscanControls.wantedYaw = int(value)

    def SetNewCameraAngle(floatValue:float):
        value = (floatValue*127)
        value = BatiscanActions._ClampValueToSignedChar(value)
        BatiscanControls.wantedCameraAngle = int(value)

    def SetNewRoll(floatValue:float):
        value = (floatValue*127)
        value = BatiscanActions._ClampValueToSignedChar(value)
        BatiscanControls.wantedRoll = int(value)

    def SetNewPitch(floatValue:float):
        value = (floatValue*127)
        value = BatiscanActions._ClampValueToSignedChar(value)
        BatiscanControls.wantedPitch = int(value)

    def SetNewSpeed(floatValue:float):
        value = (floatValue*127)
        value = BatiscanActions._ClampValueToSignedChar(value)
        BatiscanControls.wantedSpeed = int(value)
        print(BatiscanControls.wantedSpeed)
    # endregion
    # region   --------------------------- CONSTRUCTOR
    # endregion
    pass
#====================================================================#
LoadingLog.End("values.py")