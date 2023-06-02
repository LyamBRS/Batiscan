#====================================================================#
# File Information
#====================================================================#
"""
    controls.py
    =============
    This file's purpose is to handle the various controls and bindings
    of Batiscan's GUI. It has callbacks and various other functions
    called and checked.
"""
#====================================================================#
# Loading Logs
#====================================================================#
from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog import LoadingLog
LoadingLog.Start("controls.py")
#====================================================================#
# Imports
#====================================================================#
#region ------------------------------------------------------ Python
LoadingLog.Import("Python")
#endregion
#region --------------------------------------------------------- BRS
# LoadingLog.Import("Libraries")
#endregion
#region -------------------------------------------------------- Kivy
# LoadingLog.Import("Kivy")
#endregion
#region ------------------------------------------------------ KivyMD
# LoadingLog.Import('KivyMD')
#endregion
#====================================================================#
# Functions
#====================================================================#

#====================================================================#
# Classes
#====================================================================#
LoadingLog.Class("BatiscanControls")
class BatiscanControls:
    #region   --------------------------- DOCSTRING
    """
        BatiscanControls:
        =================
        Summary:
        ========
        Holds each possible controls that can
        be read or sent to Batiscan.
    """
    #endregion
    #region   --------------------------- MEMBERS
    wantedLeftLight:bool = False
    wantedRightLight:bool = False

    wantedSurface:bool = False
    currentSurface:bool = False

    wantedBallast:bool = False
    currentBallast:bool = False

    currentLeftLight:bool = False
    currentRightLight:bool = False
    # -----------------------------------
    currentCameraStatus:bool = False
    wantedCameraStatus:bool = False
    # -----------------------------------
    currentCameraAngle:int = 0
    wantedCameraAngle:int = 0

    currentBattery:int = 0
    currentTemperature:int = 0
    currentPressure:int = 0

    currentMode:str = "N"
    wantedMode:str = "N"

    waterDetected:bool = False
    lowBattery:bool = False
    inEmergency:bool = False
    isCommunicating:bool = False

    pressure:int = 0
    temperature:int = 0

    currentTemperatureUnit:str = "C"
    wantedTemperatureUnit:str = "C"

    currentXAxis:int = -60
    currentYAxis:int = -60
    currentZAxis:int = -60
    currentPitch:int = 0
    currentRoll:int = 0
    currentYaw:int = 0

    wantedPitch:float = 0
    wantedRoll:float = 0
    wantedYaw:float = 0
    wantedSpeed:float = 0
    currentSpeed:float = 0

    currentServoA:int = 0
    currentServoB:int = 0
    currentServoC:int = 0
    currentServoD:int = 0
    currentServoE:int = 0

    wantedServoA:int = 0
    wantedServoB:int = 0
    wantedServoC:int = 0
    wantedServoD:int = 0
    wantedServoE:int = 0

    #endregion
    #region   --------------------------- METHODS
    #endregion
    #region   --------------------------- CONSTRUCTOR
    #endregion
    pass
#====================================================================#
LoadingLog.End("AppLoading.py")