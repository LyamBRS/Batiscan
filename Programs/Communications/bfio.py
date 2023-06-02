from Libraries.BRS_Python_Libraries.BRS.Utilities.bfio import Plane, NewArrival, VarTypes, Execution, Passenger, PassengerTypes, Debug, BFIO
from Libraries.BRS_Python_Libraries.BRS.Utilities.Information import Information
from Local.Drivers.Batiscan.Programs.Controls.controls import BatiscanControls
from Local.Drivers.Batiscan.Programs.Controls.updaters import BatiscanUpdaters
from Local.Drivers.Batiscan.Programs.Controls.values import BatiscanValues
from Libraries.BRS_Python_Libraries.BRS.Network.UDP.sender import UDPSender
################################################
def GetPing() -> list:
    """
        returns variable necessary to make the plane
        with the same name.
    """
    return [True]
################################################
def GetStatus() -> list:
    """
        returns variable necessary to make the plane
        with the same name.
    """
    return [1]
################################################
def GetHandshake() -> list:
    """
        returns variable necessary to make the plane
        with the same name.
    """
    return []
################################################
def GetErrorMessage() -> list:
    """
        returns variable necessary to make the plane
        with the same name.
    """
    return ["no errors"]
################################################
################################################
def GetType() -> list:
    """
        returns variable necessary to make the plane
        with the same name.
    """
    return [1]
################################################
def GetID() -> list:
    """
        GetIDPlane:
        =============
        Summary:
        --------
        Gets a plane that requests the other
        device to send their ID all the while
        you're sending an ID.

    """
    return [1234567890]
################################################
def GetRestartProtocol() -> list:
    """
        returns variable necessary to make the plane
        with the same name.
    """
    return []
################################################
def GetUniversalInfoUpdate() -> list:
    """
        returns variable necessary to make the plane
        with the same name.
    """
    return [
                    1234567890,                                     # unique device ID
                    1,                                              # BFIO version
                    1,                                              # Device type
                    1,                                              # Device status
                    "https://github.com/LyamBRS/BRS-Kontrol.git",   # Git repository of the device.
                    "Kontrol",
                    "Rev A"
                    # Information.name,                               # name of the device
                    # Information.softwareVersion                     # Software version of the device.
                ]
################################################
def GetHandlingError() -> list:
    """
        returns variable necessary to make the plane
        with the same name.
    """
    return []
################################################




################################################
def GetUpdateLights() -> list:
    """
        returns variable necessary to make the plane
        with the same name.
    """
    return [BatiscanControls.wantedLeftLight, BatiscanControls.wantedRightLight]
################################################
def GetUpdateServos() -> list:
    """
        returns variable necessary to make the plane
        with the same name.
    """
    return [BatiscanControls.wantedServoA, BatiscanControls.wantedServoB, BatiscanControls.wantedServoC, BatiscanControls.wantedServoD, BatiscanControls.wantedServoE]
################################################
def GetUpdateModes() -> Plane:
    """
        returns variable necessary to make the plane
        with the same name.
    """
    return [BatiscanControls.wantedMode, BatiscanControls.wantedTemperatureUnit]
################################################
def GetUpdateCamera() -> Plane:
    """
        returns variable necessary to make the plane
        with the same name.
    """
    return [BatiscanControls.wantedCameraStatus, BatiscanControls.wantedCameraAngle]
################################################
def GetAllState() -> Plane:
    """
        returns variable necessary to make the plane
        with the same name.
    """
    return []
################################################
def GetAllSensor() -> Plane:
    """
        returns variable necessary to make the plane
        with the same name.
    """
    return []
################################################
def GetUpdateNavigation() -> Plane:
    """
        returns variable necessary to make the plane
        with the same name.
    """
    return [BatiscanControls.wantedSpeed, BatiscanControls.wantedPitch, BatiscanControls.wantedRoll, BatiscanControls.wantedYaw, BatiscanControls.wantedCameraAngle]
################################################
def GetSetBallast() -> Plane:
    """
        returns variable necessary to make the plane
        with the same name.
    """
    return [BatiscanControls.wantedBallast]
################################################
def GetSurfaceNow() -> Plane:
    """
        returns variable necessary to make the plane
        with the same name.
    """
    return []


class PlaneIDs:
    ping:int = 0
    """Callsign 0"""
    status:int = 1
    """Callsign 1"""
    handshake:int = 2
    """Callsign 2"""
    errorMessage:int = 3
    """Callsign 3"""
    deviceType:int = 4
    """Callsign 4"""
    uniqueID:int = 5
    """Callsign 5"""
    restartProtocol:int = 6
    """Callsign 6"""
    universalInfo:int = 7
    """Callsign 7"""
    communicationError:int = 8
    """Callsign 8"""

    lightsUpdate:int = 20
    """Callsign 20"""
    servoUpdate:int = 21
    """Callsign 21"""
    modeUpdate:int = 22
    """Callsign 22"""
    cameraUpdate:int = 23
    """Callsign 23"""
    allStates:int = 24
    """Callsign 24"""
    allSensors:int = 25
    """Callsign 25"""
    navigationUpdate:int = 26
    """Callsign 26"""
    ballastUpdate:int = 27
    """Callsign 27"""
    surface:int = 28
    """Callsign 28"""

sentVarTypes = {
    PlaneIDs.ping               : [VarTypes.Bool],
    PlaneIDs.status             : [VarTypes.Unsigned.Char],
    PlaneIDs.handshake          : [],
    PlaneIDs.errorMessage       : [VarTypes.String],
    PlaneIDs.deviceType         : [VarTypes.Unsigned.Char],
    PlaneIDs.uniqueID           : [VarTypes.Unsigned.LongLong],
    PlaneIDs.restartProtocol    : [],
    PlaneIDs.universalInfo      : [VarTypes.Unsigned.LongLong, VarTypes.Unsigned.LongLong, VarTypes.Unsigned.Char, VarTypes.Unsigned.Char, VarTypes.String, VarTypes.String, VarTypes.String],
    PlaneIDs.communicationError : [],
    PlaneIDs.lightsUpdate       : [VarTypes.Bool, VarTypes.Bool],
    PlaneIDs.servoUpdate        : [VarTypes.Signed.Char, VarTypes.Signed.Char, VarTypes.Signed.Char, VarTypes.Signed.Char, VarTypes.Signed.Char, VarTypes.Signed.Char, VarTypes.Signed.Char],
    PlaneIDs.modeUpdate         : [VarTypes.Char, VarTypes.Char],
    PlaneIDs.cameraUpdate       : [VarTypes.Bool, VarTypes.Signed.Char],
    PlaneIDs.allStates          : [],
    PlaneIDs.allSensors         : [],
    PlaneIDs.navigationUpdate   : [VarTypes.Signed.Char, VarTypes.Signed.Char, VarTypes.Signed.Char, VarTypes.Signed.Char, VarTypes.Signed.Char],
    PlaneIDs.ballastUpdate      : [VarTypes.Bool],
    PlaneIDs.surface            : [],
}

receivedVarTypes = {
    PlaneIDs.ping               : [VarTypes.Bool],
    PlaneIDs.status             : [VarTypes.Unsigned.Char],
    PlaneIDs.handshake          : [],
    PlaneIDs.errorMessage       : [VarTypes.String],
    PlaneIDs.deviceType         : [VarTypes.Unsigned.Char],
    PlaneIDs.uniqueID           : [VarTypes.Unsigned.LongLong],
    PlaneIDs.restartProtocol    : [],
    PlaneIDs.universalInfo      : [VarTypes.Unsigned.LongLong, VarTypes.Unsigned.LongLong, VarTypes.Unsigned.Char, VarTypes.Unsigned.Char, VarTypes.String, VarTypes.String, VarTypes.String],
    PlaneIDs.communicationError : [],
    PlaneIDs.lightsUpdate       : [VarTypes.Bool, VarTypes.Bool],
    PlaneIDs.servoUpdate        : [VarTypes.Signed.Char, VarTypes.Signed.Char, VarTypes.Signed.Char, VarTypes.Signed.Char, VarTypes.Signed.Char, VarTypes.Signed.Char, VarTypes.Signed.Char],
    PlaneIDs.modeUpdate         : [VarTypes.Char, VarTypes.Char],
    PlaneIDs.cameraUpdate       : [VarTypes.Bool, VarTypes.Signed.Char],
    PlaneIDs.allStates          : [VarTypes.Bool, VarTypes.Bool, VarTypes.Bool, VarTypes.Bool, VarTypes.Bool,VarTypes.Bool, VarTypes.Bool, VarTypes.Bool],
    PlaneIDs.allSensors         : [VarTypes.Int,        # Pressure
                                   VarTypes.Signed.Char, # temperature
                                   VarTypes.Signed.Char, # pitch
                                   VarTypes.Signed.Char, # roll
                                   VarTypes.Signed.Char, # yaw
                                   VarTypes.Signed.Char, # speed
                                   VarTypes.Unsigned.Char], # battery
    PlaneIDs.navigationUpdate   : [VarTypes.Signed.Char, VarTypes.Signed.Char, VarTypes.Signed.Char, VarTypes.Signed.Char, VarTypes.Signed.Char],
    PlaneIDs.ballastUpdate      : [VarTypes.Bool],
    PlaneIDs.surface            : [VarTypes.Bool],
}

getters = {
    PlaneIDs.ping               : GetPing,
    PlaneIDs.status             : GetStatus,
    PlaneIDs.handshake          : GetHandshake,
    PlaneIDs.errorMessage       : GetErrorMessage,
    PlaneIDs.deviceType         : GetType,
    PlaneIDs.uniqueID           : GetID,
    PlaneIDs.restartProtocol    : GetRestartProtocol,
    PlaneIDs.universalInfo      : GetUniversalInfoUpdate,
    PlaneIDs.communicationError : GetHandlingError,
    PlaneIDs.lightsUpdate       : GetUpdateLights,
    PlaneIDs.servoUpdate        : GetUpdateServos,
    PlaneIDs.modeUpdate         : GetUpdateModes,
    PlaneIDs.cameraUpdate       : GetUpdateCamera,
    PlaneIDs.allStates          : GetAllState,
    PlaneIDs.allSensors         : GetAllSensor,
    PlaneIDs.navigationUpdate   : GetUpdateNavigation,
    PlaneIDs.ballastUpdate      : GetSetBallast,
    PlaneIDs.surface            : GetSurfaceNow,
}


def _PlaneIsNotOk(newArrival:NewArrival, wantedPlaneID:int):
    """
        _PlaneIsNotOk:
        ==============
        Summary:
        --------
        Private local function that checks
        if a received plane from UDP isn't right
        to use in Batiscan's specific functions.
    """
    Debug.Start("_PlaneIsNotOk")

    if(not newArrival.passedTSA):
        Debug.Error("Specified plane didn't pass TSA")
        Debug.End()
        return True

    if(newArrival.planeID != wantedPlaneID):
        Debug.Error("Specified plane isn't of the right ID")
        Debug.End()
        return True

    Debug.End()
    return False

################################################
def SetUpdateLights(newArrival:NewArrival) -> Execution:
    """
    """
    if(_PlaneIsNotOk(newArrival, PlaneIDs.lightsUpdate)):
        return Execution.Failed

    BatiscanValues.leftLight = newArrival.GetParameter(0)
    BatiscanValues.rightLight = newArrival.GetParameter(1)

    BatiscanUpdaters.UpdateLeftLightState()
    BatiscanUpdaters.UpdateRightLightState()

    return Execution.Passed
################################################
def SetUpdateServos(newArrival:NewArrival) -> Execution:
    """
        Updates saved values of Batiscan<s driver with new
        servo values received from the real Batiscan.
    """

    if(_PlaneIsNotOk(newArrival, PlaneIDs.servoUpdate)):
        return Execution.Failed

    BatiscanValues.servoA = newArrival.GetParameter(0)
    BatiscanValues.servoB = newArrival.GetParameter(1)
    BatiscanValues.servoC = newArrival.GetParameter(2)
    BatiscanValues.servoD = newArrival.GetParameter(3)
    BatiscanValues.servoE = newArrival.GetParameter(4)

    BatiscanUpdaters.UpdateServoA()
    BatiscanUpdaters.UpdateServoB()
    BatiscanUpdaters.UpdateServoC()
    BatiscanUpdaters.UpdateServoD()
    BatiscanUpdaters.UpdateServoE()

    return Execution.Passed
################################################
def SetUpdateModes(newArrival:NewArrival) -> Execution:
    """
    """

    if(_PlaneIsNotOk(newArrival, PlaneIDs.modeUpdate)):
        return Execution.Failed

    BatiscanValues.navigationMode = newArrival.GetParameter(0)
    BatiscanValues.temperatureUnit = newArrival.GetParameter(1)

    BatiscanUpdaters.UpdateNavigationMode()
    BatiscanUpdaters.UpdateTemperature()

    return Execution.Passed
################################################
def SetUpdateCamera(newArrival:NewArrival) -> Execution:
    """
    """

    if(_PlaneIsNotOk(newArrival, PlaneIDs.cameraUpdate)):
        return Execution.Failed

    BatiscanValues.cameraStatus = newArrival.GetParameter(0)
    BatiscanValues.cameraAngle = newArrival.GetParameter(1)

    BatiscanUpdaters.UpdateCameraState()
    BatiscanUpdaters.UpdateCameraAngle()

    return Execution.Passed
################################################
def SetAllState(newArrival:NewArrival) -> Execution:
    """
    """

    if(_PlaneIsNotOk(newArrival, PlaneIDs.allStates)):
        return Execution.Failed

    BatiscanValues.waterDetected = newArrival.GetParameter(0)
    BatiscanValues.cameraStatus = newArrival.GetParameter(1)
    BatiscanValues.lowBattery = newArrival.GetParameter(2)
    BatiscanValues.leftLight = newArrival.GetParameter(3)
    BatiscanValues.rightLight = newArrival.GetParameter(4)
    BatiscanValues.inEmergency = newArrival.GetParameter(5)
    BatiscanValues.ballast = newArrival.GetParameter(6)
    BatiscanValues.isCommunicating = newArrival.GetParameter(7)

    BatiscanUpdaters.UpdateWaterDetected()
    BatiscanUpdaters.UpdateCameraState()
    BatiscanUpdaters.UpdateLowBattery()
    BatiscanUpdaters.UpdateLeftLightState()
    BatiscanUpdaters.UpdateRightLightState()
    BatiscanUpdaters.UpdateInEmergency()
    BatiscanUpdaters.UpdateBallast()
    BatiscanUpdaters.UpdateIsCommunicating()

    return Execution.Passed
################################################
def SetAllSensor(newArrival:NewArrival) -> Execution:
    """
    """

    if(_PlaneIsNotOk(newArrival, PlaneIDs.allSensors)):
        return Execution.Failed

    BatiscanValues.pressure         = newArrival.GetParameter(0)
    BatiscanValues.temperature      = newArrival.GetParameter(1)
    BatiscanValues.pitch            = newArrival.GetParameter(2)
    BatiscanValues.roll             = newArrival.GetParameter(3)
    BatiscanValues.yaw              = newArrival.GetParameter(4)
    BatiscanValues.speed            = newArrival.GetParameter(5)
    BatiscanValues.battery          = newArrival.GetParameter(6)

    BatiscanUpdaters.UpdatePressure()
    # BatiscanUpdaters.UpdatePitch()
    # BatiscanUpdaters.UpdateRoll()
    # BatiscanUpdaters.UpdateYaw()
    BatiscanUpdaters.UpdateSubmarineAngles()
    BatiscanUpdaters.UpdateSpeed()
    BatiscanUpdaters.UpdateBattery()
    BatiscanUpdaters.UpdateTemperature()

    return Execution.Passed
################################################
def SetUpdateNavigation(newArrival:NewArrival) -> Execution:
    """
    """

    if(_PlaneIsNotOk(newArrival, PlaneIDs.navigationUpdate)):
        return Execution.Failed

    BatiscanValues.speed            = newArrival.GetParameter(0)
    BatiscanValues.pitch            = newArrival.GetParameter(1)
    BatiscanValues.roll             = newArrival.GetParameter(2)
    BatiscanValues.yaw              = newArrival.GetParameter(3)
    BatiscanValues.cameraAngle      = newArrival.GetParameter(4)

    BatiscanUpdaters.UpdateSpeed()
    # BatiscanUpdaters.UpdatePitch()
    # BatiscanUpdaters.UpdateRoll()
    # BatiscanUpdaters.UpdateYaw()
    BatiscanUpdaters.UpdateSubmarineAngles()

    return Execution.Passed
################################################
def SetSetBallast(newArrival:NewArrival) -> Execution:
    """
    """

    if(_PlaneIsNotOk(newArrival, PlaneIDs.ballastUpdate)):
        return Execution.Failed

    BatiscanValues.ballast = newArrival.GetParameter(0)
    BatiscanUpdaters.UpdateBallast()

    return Execution.Passed
################################################
def SetSurfaceNow(newArrival:NewArrival) -> Execution:
    """
    """

    if(_PlaneIsNotOk(newArrival, PlaneIDs.surface)):
        return Execution.Failed

    return Execution.Passed


updaters = {
    PlaneIDs.lightsUpdate       : SetUpdateLights,
    PlaneIDs.servoUpdate        : SetUpdateServos,
    PlaneIDs.modeUpdate         : SetUpdateModes,
    PlaneIDs.cameraUpdate       : SetUpdateCamera,
    PlaneIDs.allStates          : SetAllState,
    PlaneIDs.allSensors         : SetAllSensor,
    PlaneIDs.navigationUpdate   : SetUpdateNavigation,
    PlaneIDs.ballastUpdate      : SetSetBallast,
    PlaneIDs.surface            : SetSurfaceNow,
}



def SendUDPMessage(ip_address, port, message:str):
    try:
        import socket
        # Create a UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Send the message
        sock.sendto(message.encode('utf-8'), (ip_address, port))

        # Close the socket
        sock.close()
        return True
    except Exception as e:
        Debug.Error("FAILED TO SEND SOCKET")
        return False

def MakeAPlaneOutOfArrivedBytes(bytesToDecode:bytes) -> NewArrival:
    """
        MakeAPlaneOutOfArrivedBytes:
        ============================
        Summary:
        --------
        Creates a plane out of a list of bytes.
        Will return errors as Execution if the
        plane couldn't be created.

        The bytes needs to be in groupes of 2 bytes
        being in the order of identifiant then luggage.
        Batiscan works through UDP and that protocol
        only uses bytes.

        Arguments:
        ----------
        - `bytes:bytes` a list of bytes
    """

    passengers = BFIO.GetPassengersFromDualBytes(bytesToDecode)

    pilot:Passenger = passengers[0]
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

import socket
class StupidFuckingPythonIsRetardedAndGayAFWithMemoryManagement:
    listOfIntegers = []

def SendAPlaneOnUDP(functionID:int, Getters) -> Execution:
    """
        SendAPlaneOnUDP:
        ================
        Summary:
        --------
        Sends a plane on the UDP made of given parameters
    """
    # try:
    planeToSend = Plane(functionID, Getters[functionID](), sentVarTypes[functionID], DontDebug=True)
    if(not planeToSend.passedTSA):
        whateverItUsed = Getters[functionID]()
        raise Exception(f"A plane failed its TSA check. The plane was built using callsign {functionID} and its getter returned {whateverItUsed}")
    # except:
        # Debug.Error("FAILED TO CREATE PLANE BRUH")
        # print("BATISCAN FAILED SendAPlaneOnUDP")
        # return Execution.Failed

    listOfIntegers = []
    for passenger in planeToSend.passengers:
        # Send the message
        valA = passenger.value_8bits[0]#.encode('utf-8')
        valB = passenger.value_8bits[1]#.encode('utf-8')
        listOfIntegers.append(valA)
        listOfIntegers.append(valB)

    bytesToSend = bytes(listOfIntegers)
    Debug.Log(f"Sending {listOfIntegers}")
    UDPSender.SendThing(bytesToSend)

    return Execution.Passed