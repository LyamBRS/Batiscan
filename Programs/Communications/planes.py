#====================================================================#
# File Information
#====================================================================#
"""
    planes.py
    =========
    This file contains functions that build planes specifically for
    Batiscan's BFIO specific functions. These planes are sent to
    Batiscan in order for it to execute functions and return
    answers.
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
from Libraries.BRS_Python_Libraries.BRS.Utilities.bfio import BFIO, NewArrival, Passenger, PassengerTypes, Execution
#endregion
#region -------------------------------------------------------- Kivy
# LoadingLog.Import("Kivy")
#endregion
#region ------------------------------------------------------ Batiscan
LoadingLog.Import('Batiscan')
from Local.Drivers.Batiscan.Programs.Communications.bfio import receivedVarTypes, sentVarTypes, PlaneIDs, getters, updaters
#endregion
#====================================================================#
# Functions
#====================================================================#
def MakeAPlaneOutOfArrivedBytes(bytesToDecode:bytes) -> NewArrival:
    """
        MakeAPlaneOutOfArrivedBytes:
        ============================
        Summary:
        --------
        Creates a plane out of a list of bytes.
        Will return errors as Execution if the
        plane couldn't be created.

        The bytes needs to be in groups of 2 bytes
        being in the order of identifiant then luggage.
        Batiscan works through UDP and that protocol
        only uses bytes.

        Arguments:
        ----------
        - `bytes:bytes` a list of bytes
    """

    if(bytesToDecode == None):
        return None

    passengers = BFIO.GetPassengersFromDualBytes(bytesToDecode)

    if(passengers == None):
        return None
    
    if(len(passengers) < 2):
        return None

    # Checking if the first passenger is a pilot. Otherwise, the plane is discarded.
    try:
        pilot:Passenger = passengers[0]
    except:
        Debug.Error("FAILED TO GET PILOT. EPIC FAIL")
        print(passengers)
        return None

    if(pilot.type != PassengerTypes.Pilot):
        Debug.Error("Err first passenger isn't a pilot mate...")
        return Execution.Failed

    planeID = pilot.value_8bits[1]
    # try:
    newArrival = NewArrival(passengers, receivedVarTypes[planeID])
    return newArrival
    # except:
        # Debug.Error("PLANE DOES NOT EXIST / ISN'T SUPPORTED")
        # return Execution.Failed

def ExecuteArrivedPlane(newArrival:NewArrival) -> Execution:
    """
        ExecuteArrivedPlane:
        ====================
        Summary:
        --------
        This function executes an arrived plane's
        updater

        Return:
        --------
        - `Execution.Unecessary` =  Plane is empty.
        - `Execution.Incompatibility` =  Plane isn't of a valid call sign for this function.
        - `Execution.Failed` =  Plane isn't of a valid call sign for this function.
    """

    if(newArrival == None):
        return Execution.Unecessary

    planeID = newArrival.planeID

    try:
        updater = updaters[planeID]
    except:
        return Execution.Incompatibility

    result = updater(newArrival)
    if(result != Execution.Passed):
        return Execution.Failed

#====================================================================#
# Classes
#====================================================================#
LoadingLog.Class("BatiscanControls")
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

        BatiscanValues.pitch = 0
        BatiscanValues.yaw  = 0
        BatiscanValues.roll = 0
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