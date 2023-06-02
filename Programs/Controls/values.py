#====================================================================#
# File Information
#====================================================================#
"""
    values.py
    =============
    This file's purpose is to hold a class that holds the globally
    accessed values used by the application to display things
    like speed, battery, lights and so on. These values are updated
    through updaters.
"""
#====================================================================#
# Loading Logs
#====================================================================#
from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog import LoadingLog
LoadingLog.Start("values.py")
#====================================================================#
# Imports
#====================================================================#
#region ------------------------------------------------------ Python
# LoadingLog.Import("Python")
#endregion
#region --------------------------------------------------------- BRS
LoadingLog.Import("Libraries")
from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog import Debug
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
LoadingLog.Class("BatiscanValues")
class BatiscanValues:
    #region   --------------------------- DOCSTRING
    """
        BatiscanValues:
        ===============
        Summary:
        ========
        Class that contains members that represents
        Batiscan's current values. It contains the
        last received values and statuses from
        Batiscan which were received through UDP
        protocol.
    """
    #endregion
    #region   --------------------------- MEMBERS
    battery:int = 0
    """
        value from 0 to 100 representing the
        battery level of Batiscan.
        Defaults to 0.
    """
    pressure:int = 0
    """
        Value from X to Y representing the
        pressure level from Batiscan.
        Defaults to 0.
    """
    temperature:int = 0
    """
        The current temperature returned from
        Batiscan.
        Defaults to 0.
    """

    ballast:bool = False

    leftLight:bool = False
    rightLight:bool = False
    # -----------------------------------
    cameraStatus:bool = False
    cameraAngle:int = 0
    # -----------------------------------
    waterDetected:bool = False
    lowBattery:bool = False
    inEmergency:bool = False
    isCommunicating:bool = False

    pitch:int = 0
    """ The last pitch value returned from Batiscan. Defaults to 0."""
    roll:int = 0
    """ The last roll value returned from Batiscan. Defaults to 0."""
    yaw:int = 0
    """ The last yaw value returned from Batiscan. Defaults to 0."""

    speed:int = 0
    """ The last speed value returned from Batiscan. Defaults to 0."""

    navigationMode:str = "N"
    """ NOT DONE """

    temperatureUnit:str = "C"
    """ NOT DONE """

    servoA:int = 0
    servoB:int = 0
    servoC:int = 0
    servoD:int = 0
    servoE:int = 0
    #endregion
    #region   --------------------------- METHODS
    def Reset():
        """
            Reset:
            ======
            Summary:
            --------
            Resets all the members of this class
            back to their default values. This is used
            when you quit the driver, or launch it in
            order to nullify any data that could be
            left from previous communications.
        """
        Debug.Start("Reset")

        BatiscanValues.battery = 0
        BatiscanValues.pressure = 0
        BatiscanValues.temperature = 0

        BatiscanValues.cameraAngle = 0
        BatiscanValues.cameraStatus = False

        BatiscanValues.waterDetected = False
        BatiscanValues.lowBattery = False
        BatiscanValues.isCommunicating = False

        BatiscanValues.ballast = False

        BatiscanValues.pitch = -60
        BatiscanValues.yaw  = -60
        BatiscanValues.roll = -60
        BatiscanValues.speed = 0

        BatiscanValues.rightLight = False
        BatiscanValues.leftLight = False

        BatiscanValues.servoA = 0
        BatiscanValues.servoB = 0
        BatiscanValues.servoC = 0
        BatiscanValues.servoD = 0
        BatiscanValues.servoE = 0

        Debug.End()
    #endregion
    #region   --------------------------- CONSTRUCTOR
    #endregion
    pass
#====================================================================#
LoadingLog.End("values.py")