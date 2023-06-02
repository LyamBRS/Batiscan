#====================================================================#
# File Information
#====================================================================#
"""
    updaters.py
    =============
    This file's purpose is to update the various saved information
    of Batiscan. Whenever a button is pressed, or data is received,
    the updater functions can be called to update the data saved
    inside of Batiscan's stuff.
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
class BatiscanUpdaters:
    #region   --------------------------- DOCSTRING
    """
        BatiscanUpdaters:
        =================
        Summary:
        ========
        Holds methods that are called by
        the communication processes when a specific
        plane is received. These methods are overwritten
        when GUI is created. They are replaced by widget
        icons updaters and so on.
    """
    #endregion
    #region   --------------------------- MEMBERS
    #endregion
    #region   --------------------------- METHODS
    def UpdateTemperature(*args):
        """
            UpdateTemperature:
            ==================
            Summary:
            --------
            NEEDS TO BE OVERWRITTEN.
        """
        pass

    def UpdateNavigationMode(*args):
        """
            UpdateNavigationMode:
            =====================
            Summary:
            --------
            NEEDS TO BE OVERWRITTEN.
        """
        pass

    def UpdateBattery(*args):
        """
            UpdateBattery:
            ==============
            Summary:
            --------
            NEEDS TO BE OVERWRITTEN.
        """
        pass

    def UpdateSpeed(*args):
        """
            UpdateSpeed:
            ============
            Summary:
            --------
            NEEDS TO BE OVERWRITTEN.
        """
        pass

    def UpdateSubmarineAngles(*args):
        """
            UpdateYaw:
            ============
            Summary:
            --------
            NEEDS TO BE OVERWRITTEN.

            IS USED TO UPDATE YAW, ROLL, PITCH
            AT ONCE.
        """
        pass

    def UpdateYaw(*args):
        """
            UpdateYaw:
            ============
            Summary:
            --------
            NEEDS TO BE OVERWRITTEN.
        """
        pass

    def UpdateRoll(*args):
        """
            UpdateRoll:
            ============
            Summary:
            --------
            NEEDS TO BE OVERWRITTEN.
        """
        pass

    def UpdatePitch(*args):
        """
            UpdatePitch:
            ============
            Summary:
            --------
            NEEDS TO BE OVERWRITTEN.
        """
        pass

    def UpdateServoA(*args):
        """
            UpdateServoA:
            ============
            Summary:
            --------
            NEEDS TO BE OVERWRITTEN.
        """
        pass

    def UpdateServoB(*args):
        """
            UpdateServoB:
            ============
            Summary:
            --------
            NEEDS TO BE OVERWRITTEN.
        """
        pass

    def UpdateServoC(*args):
        """
            UpdateServoA:
            ============
            Summary:
            --------
            NEEDS TO BE OVERWRITTEN.
        """
        pass

    def UpdateServoD(*args):
        """
            UpdateServoD:
            ============
            Summary:
            --------
            NEEDS TO BE OVERWRITTEN.
        """
        pass

    def UpdateServoE(*args):
        """
            UpdateServoE:
            ============
            Summary:
            --------
            NEEDS TO BE OVERWRITTEN.
        """
        pass

    def UpdateWaterDetected(*args):
        """
            UpdateWaterDetected:
            ====================
            Summary:
            --------
            NEEDS TO BE OVERWRITTEN.
        """
        pass

    def UpdateLowBattery(*args):
        """
            UpdateLowBattery:
            =================
            Summary:
            --------
            NEEDS TO BE OVERWRITTEN.
        """
        pass

    def UpdateLeftLightState(*args):
        """
            UpdateLeftLightState:
            =================
            Summary:
            --------
            NEEDS TO BE OVERWRITTEN.
        """
        pass

    def UpdateRightLightState(*args):
        """
            UpdateLeftLightState:
            =================
            Summary:
            --------
            NEEDS TO BE OVERWRITTEN.
        """
        pass

    def UpdateInEmergency(*args):
        """
            UpdateInEmergency:
            =================
            Summary:
            --------
            NEEDS TO BE OVERWRITTEN.
        """
        pass

    def UpdateIsCommunicating(*args):
        """
            UpdateIsCommunicating:
            ======================
            Summary:
            --------
            NEEDS TO BE OVERWRITTEN.
        """
        pass

    def UpdateBallast(*args):
        """
            UpdateBallast:
            ==============
            Summary:
            --------
            NEEDS TO BE OVERWRITTEN.
        """
        pass

    def UpdateIsCommunicating(*args):
        """
            UpdateIsCommunicating:
            ==============
            Summary:
            --------
            NEEDS TO BE OVERWRITTEN.
        """
        pass

    def UpdatePressure(*args):
        """
            UpdatePressure:
            ==============
            Summary:
            --------
            NEEDS TO BE OVERWRITTEN.
        """
        pass

    def UpdatePressure(*args):
        """
            UpdatePressure:
            ==============
            Summary:
            --------
            NEEDS TO BE OVERWRITTEN.
        """
        pass

    def UpdateCameraState(*args):
        """
            UpdateCameraState:
            ==================
            Summary:
            --------
            NEEDS TO BE OVERWRITTEN.
        """
        pass

    def UpdateCameraAngle(*args):
        """
            UpdateCameraAngle:
            ==================
            Summary:
            --------
            NEEDS TO BE OVERWRITTEN.
        """
        pass

    #endregion
    #region   --------------------------- CONSTRUCTOR
    #endregion
    pass
#====================================================================#
LoadingLog.End("AppLoading.py")