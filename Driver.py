#====================================================================#
# File Information
#====================================================================#
"""
    Driver.py
    =============
    This file is the generic, universal Device Driver; Driver.py.
"""
#====================================================================#
# Loading Logs
#====================================================================#
from Libraries.BRS_Python_Libraries.BRS.Debug.LoadingLog import LoadingLog
from Local.Drivers.Batiscan.Programs.Communications.UDP import StartUDP, StopUDP
from Programs.Pages.DriverMenu import DriverMenu_Screens
LoadingLog.Start("Driver.py")
#====================================================================#
# Imports
#====================================================================#
#region ------------------------------------------------------ Python
LoadingLog.Import("Python")
#endregion
#region --------------------------------------------------------- BRS
LoadingLog.Import("Libraries")
from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog import Debug
from Libraries.BRS_Python_Libraries.BRS.Utilities.Enums import Execution, FileIntegrity
#endregion
#region -------------------------------------------------------- Kivy
LoadingLog.Import("Kivy")
#endregion
#region ------------------------------------------------------ KivyMD
LoadingLog.Import('KivyMD')
#endregion
#====================================================================#
# Variables
#====================================================================#
class variables:
    errorMessage:str = None
#====================================================================#
# Functions
#====================================================================#
def CheckIntegrity() -> FileIntegrity:
    """
        CheckIntegrity:
        ===============
        Summary:
        -------
        This function checks this device driver for any default
        or missing file(s). As the name says, it checks for the
        integrity of itself and returns the resulted integrity.
    """
    Debug.Start("Batiscan -> CheckIntegrity")

    #region ------------------------------------------- [0]
    Debug.Log("[0]: Importing dependencies")
    import os
    from Local.Drivers.Batiscan.Programs.FileHandler.SelfCheck import CheckContent
    #endregion
    #region ------------------------------------------- [1]
    Debug.Log("[1]: Checking folders")
    integrity = CheckContent()
    #endregion
    Debug.End()
    return integrity
# -------------------------------------------------------------------
def Launch() -> Execution:
    """
        Launch:
        =======
        Summary:
        -------
        attempts to launch the GUI of your device driver.
        It loads a Screen into the ScreenManager.

        It will return a value within the Execution enum.
    """
    Debug.Start("Batiscan -> Launch")
    #region [0]---------------------------------------- [IMPORT]
    Debug.Log("[0]: Importing dependencies")
    from Local.Drivers.Batiscan.Pages.BatiscanMenu import BatiscanMenu_Screens
    #endregion
    #region [1]---------------------------------------- [SCREEN SETUP]
    Debug.Log("[1]: Setting up DriverMenu for launch")
    BatiscanMenu_Screens.SetCaller(BatiscanMenu_Screens, "BatiscanMenu")
    BatiscanMenu_Screens.SetExiter(BatiscanMenu_Screens, "BatiscanMenu")
    #endregion

    #region [2]---------------------------------------- [UDP setup]
    result = StartUDP()
    if(result != Execution.Passed):
        Debug.Error("UDP DRIVERS COULD NOT BE STARTED")
        Debug.End()
        return Execution.NoConnection
    #endregion

    #region [3]---------------------------------------- [LAUNCH]
    Debug.Log("[2]: Launching DriverMenu")
    BatiscanMenu_Screens.Call()
    #endregion
    Debug.End()
    return Execution.Passed
# -------------------------------------------------------------------
def Update() -> Execution:
    """
        Update:
        =======
        Summary:
        -------
        This function attempts to update the device driver to it's
        latest version. It will return an Execution value depending
        on what happens.
    """
    Debug.Start("Batiscan -> Update")
    Debug.End()
    return Execution.ByPassed
# -------------------------------------------------------------------
def Uninstall() -> Execution:
    """
        Uninstall:
        =======
        Summary:
        -------
        Completely uninstall this device driver without leaving any
        traces of it's existence in Kontrol's Software.
    """
    Debug.Start("Batiscan -> Uninstall")
    Debug.End()
    return Execution.ByPassed
# -------------------------------------------------------------------
def ClearProfileCache(profileName:str) -> Execution:
    """
        ClearProfileCache:
        ==================
        Summary:
        -------
        Removes cached data of a specific profile. This is called
        when a profile is deleted, thus all it's cached information
        needs to be deleted as well.

        The name of the profile is given as a parameter. The function
        will return an Execution enum value.
    """
    Debug.Start("Batiscan -> ClearProfileCache")
    Debug.End()
    return Execution.ByPassed
# -------------------------------------------------------------------
def GetErrorMessage() -> str:
    """
        GetErrorMessage:
        ===============
        Summary:
        -------
        Function used to get the error message of the Device Driver.
        If it crashes or cannot load, the message as to why something
        wrong happened is stored and can be accessed through this
        function.

        if there is no error to return, `None` is returned.
    """
    Debug.Start("Batiscan -> GetErrorMessage")
    Debug.End()
    return variables.errorMessage
# -------------------------------------------------------------------
def Quit() -> Execution:
    """
        Quit:
        =====
        Summary:
        -------
        Function used to quit and close the device driver and return
        to Kontrol's GUI.
    """
    Debug.Start("Batiscan -> Quit")
    from Programs.Pages.PopUps import PopUpsHandler, PopUps_Screens, PopUpTypeEnum
    from Libraries.BRS_Python_Libraries.BRS.Utilities.LanguageHandler import _
    from Programs.Pages.DriverMenu import DriverMenu_Screens
    from Local.Drivers.Batiscan.Pages.BatiscanMenu import BatiscanMenu_Screens

    Debug.Log("Creating pop up message.")
    PopUpsHandler.Clear()
    PopUpsHandler.Add(PopUpTypeEnum.Question,
                      Message = _("Do you really want to quit this device driver?"),
                      ButtonAText = _("Yes"),
                      ButtonBText = _("No"),
                      ButtonAHandler = _Stop,
                      ButtonBHandler = BatiscanMenu_Screens.Call
                      )
    PopUps_Screens.SetCaller(BatiscanMenu_Screens, "BatiscanMenu")
    PopUps_Screens.SetExiter(None, None)
    PopUps_Screens.Call()

    Debug.End()
    return None
#====================================================================#
# Classes
#====================================================================#
def _Stop(*args):
    """
        _Stop():
        ========
        Summary:
        --------
        Called when the user 
    """

    result = StopUDP()
    if(result != Execution.Passed):
        Debug.Error("UDP DRIVERS COULD NOT BE STOPPED")
        Debug.End()
        return Execution.NoConnection
    
    DriverMenu_Screens.Call()
#====================================================================#
LoadingLog.End("Driver.py")