#====================================================================#
# File Information
#====================================================================#

#====================================================================#
from Libraries.BRS_Python_Libraries.BRS.Debug.LoadingLog import LoadingLog
from Libraries.BRS_Python_Libraries.BRS.Utilities.Information import Information
from Local.Drivers.Batiscan.Programs.Communications.UDP import BatiscanUDP
from Local.Drivers.Batiscan.Programs.Communications.bfio import PlaneIDs, getters
from Local.Drivers.Batiscan.Programs.Controls.controls import BatiscanControls
LoadingLog.Start("BatiscanMenu.py")
#====================================================================#
# Imports
#====================================================================#
#region ------------------------------------------------------ Python
LoadingLog.Import("Python")
import os
#endregion
#region --------------------------------------------------------- BRS
LoadingLog.Import("Libraries")
from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog import Debug
from Libraries.BRS_Python_Libraries.BRS.Utilities.AppScreenHandler import AppManager
from Libraries.BRS_Python_Libraries.BRS.Utilities.FileHandler import AppendPath
from Libraries.BRS_Python_Libraries.BRS.Utilities.LanguageHandler import _
from Libraries.BRS_Python_Libraries.BRS.GUI.Utilities.references import Shadow, Rounding
from Libraries.BRS_Python_Libraries.BRS.Utilities.Enums import Execution
from Libraries.BRS_Python_Libraries.BRS.GUI.Utilities.colors import GetAccentColor, GetPrimaryColor, GetMDCardColor
from Libraries.BRS_Python_Libraries.BRS.PnP.controls import Controls, SoftwareAxes, SoftwareButtons
from Libraries.BRS_Python_Libraries.BRS.GUI.ObjectViewer.objectView import ObjViewer
#endregion
#region -------------------------------------------------------- Kivy
LoadingLog.Import("Kivy")
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.clock import Clock
from kivy.uix.image import Image
#endregion
#region ------------------------------------------------------ KivyMD
LoadingLog.Import("KivyMD")
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.spinner import MDSpinner

#endregion
#region ------------------------------------------------------ Kontrol
LoadingLog.Import("Local")
from Programs.Local.Hardware.RGB import KontrolRGB
from Local.Drivers.Batiscan.Programs.GUI.joystick import Joystick
from Local.Drivers.Batiscan.Programs.Communications.bfio import BatiscanValues, BatiscanUpdaters
from Local.Drivers.Batiscan.Programs.Controls.actions import BatiscanActions
# from Programs.Local.GUI.Cards import ButtonCard, DeviceDriverCard
# from Programs.Pages.PopUps import PopUpsHandler, PopUps_Screens, PopUpTypeEnum
#endregion
#====================================================================#
# Functions
#====================================================================#
def EmptyFunction():
    """
        EmptyFunction:
        ==============
        Summary:
        --------
        Used to reset BatiscanUpdaters
        so they don't crash nothing by trying
        to update inexisting values and shit.
    """
    pass

def WeNeedLeftJoystick() -> bool:
    """
        WeNeedLeftJoystick:
        =====================
        Summary:
        --------
        This function's goal is to
        tell the screen if we need to
        build a left joystick card
        so that the application can drive
        the submarine.

        It returns `True` if both axis
        are not binded to anything in the
        :ref:`Controls` class. If any axis
        is binded, `False` is returned and
        a Joystick card needs to be built.
    """
    Debug.Start("WeNeedLeftJoystick")

    forwardIsBinded:bool = Controls._axes[SoftwareAxes.forward]["binded"] or Controls._buttons[SoftwareButtons.forward]["binded"]
    backwardIsBinded:bool = Controls._axes[SoftwareAxes.backward]["binded"] or Controls._buttons[SoftwareButtons.backward]["binded"]
    speedIsBinded:bool = forwardIsBinded and backwardIsBinded

    yawLeftIsBinded:bool = Controls._axes[SoftwareAxes.yaw_left]["binded"] or Controls._buttons[SoftwareButtons.left]["binded"]
    yawRightIsBinded:bool = Controls._axes[SoftwareAxes.yaw_right]["binded"] or Controls._buttons[SoftwareButtons.right]["binded"]
    turningIsBinded:bool = yawLeftIsBinded and yawRightIsBinded

    Debug.Log("Checking Y axis bindings")
    if(speedIsBinded):
        if(turningIsBinded):
            Debug.Log("Screen joystick is not needed")
            Debug.End()
            return False

    Debug.Log("Screen joystick is needed")
    Debug.End()
    return True

def WeNeedRightJoystick() -> bool:
    """
        WeNeedRightJoystick:
        =====================
        Summary:
        --------
        This function's goal is to
        tell the screen if we need to
        build a right joystick card
        so that the application can drive
        the submarine.

        It returns `True` if both axis
        are not binded to anything in the
        :ref:`Controls` class. If any axis
        is binded, `False` is returned and
        a Joystick card needs to be built.
    """
    Debug.Start("WeNeedRightJoystick")

    rollLeftIsBinded:bool = Controls._axes[SoftwareAxes.roll_left]["binded"]
    rollRightIsBinded:bool = Controls._axes[SoftwareAxes.roll_right]["binded"]
    rollingIsBinded:bool = rollLeftIsBinded and rollRightIsBinded

    pitchUpisBinded:bool = Controls._axes[SoftwareAxes.pitch_up]["binded"] or Controls._buttons[SoftwareButtons.up]["binded"]
    pitchDownisBinded:bool = Controls._axes[SoftwareAxes.pitch_down]["binded"] or Controls._buttons[SoftwareButtons.down]["binded"]
    pitchIsBinded:bool = pitchUpisBinded and pitchDownisBinded

    if(pitchIsBinded and rollingIsBinded):
        Debug.Log("Screen joystick is not needed")
        Debug.End()
        return False

    Debug.Log("Screen joystick is needed")
    Debug.End()
    return True

def ConvertBatiscanAnglesToDegrees(angleToConvert:int) -> int:
    """
        Takes a value from -127 to 127 and converts it
        to degrees. It also accounts for the -60 offset

        First, 60 is added to compensate batiscan's 0 being -60
        Then, the function adds 127 to the angle.
        This makes it be from 0 to 254 (minus the offset).
        Then, the function makes a cross product to transpose the 0-254 to 0-360.
    """
    newValue = ((((angleToConvert + 60) + 127) * 360) / 254)
    return newValue 
#====================================================================#
# Screen class
#====================================================================#
LoadingLog.Class("BatiscanMenu_Screens")
class BatiscanMenu_Screens:
    """
        BatiscanMenu_Screens:
        ================
        Summary:
        --------
        This class allows the handling of the transitional screen
        :class:`BatiscanMenu`.

        Description:
        ------------
        This class holds the different types of callers of the AppLoading
        screen as well as the different exit screens that this transitional
        screen can go to. You must specify the names of the wanted exit screens
        prior to calling the transition function.

        An exit screen is basically which screens should be loaded if something
        happens in the transition screen.
    """
    #region ---- Members
    _exitClass = None
    _callerClass = None

    _callerName = None
    _exitName = None

    _callerTransition = SlideTransition
    _exitTransition = SlideTransition

    _callerDirection = "up"
    _exitDirection = "up"

    _callerDuration = 0.5
    _exitDuration = 0.5
    #endregion
    #region ---- Methods
    def SetExiter(screenClass, screenName:str, transition=SlideTransition, duration:float=0.5, direction:str="up") -> bool:
        """
            Function which sets the screen that this screen should transition to on exit.
            This allows transitional screens to be reused by any screens at any time.

            Args:
                `screenClass (_type_)`: The screen class of the screen this handler should transition to on exit.
                `screenName (str)`: The name of the screen class. It needs to be the same as :ref:`screenClass`.
                `transition`: Optional kivy transition class. Defaults as `WipeTransition`
                `duration (float)`: Optional specification of the transition's duration. Defaults to 0.5 seconds
                `direction (str)`: Optional direction which the transition should go. Defaults as `"up"`.

            Returns:
                bool: `True`: Something went wrong. `False`: Success
        """
        # Attempt to add the screen class as a widget of the AppManager
        BatiscanMenu_Screens._exitClass = screenClass
        BatiscanMenu_Screens._exitName  = screenName

        BatiscanMenu_Screens._exitTransition = transition
        BatiscanMenu_Screens._exitDuration = duration
        BatiscanMenu_Screens._exitDirection = direction
        return False

    def SetCaller(screenClass, screenName:str, transition=SlideTransition, duration:float=0.5, direction:str="up") -> bool:
        """
            Function which sets the screen to load if an error occured. This is used to "go back" to whoever attempted
            to call this screen.

            Args:
                `screenClass (_type_)`: The screen class of the screen that wants to transition to this one.
                `screenName (str)`: The name of the screen class. It needs to be the same as :ref:`screenClass`.
                `transition`: Optional kivy transition class. Defaults as `WipeTransition`
                `duration (float)`: Optional specification of the transition's duration. Defaults to 0.5 seconds
                `direction (str)`: Optional direction which the transition should go. Defaults as `"up"`.

            Returns:
                bool: `True`: Something went wrong. `False`: Success
        """
        # Attempt to add the screen class as a widget of the AppManager
        BatiscanMenu_Screens._callerClass = screenClass
        BatiscanMenu_Screens._callerName  = screenName

        BatiscanMenu_Screens._callerTransition = transition
        BatiscanMenu_Screens._callerDuration = duration
        BatiscanMenu_Screens._callerDirection = direction
        return False

    def _Exit(*args) -> Execution:
        """
            Attempt to go to the specified screen that was set using :ref:`SetExiter`.

            Returns:
                bool: `True`:  Something went wrong and the wanted exiter screen can't be loaded. `False`: Success
        """
        Debug.Start("BatiscanMenu_Screens -> _Exit()")
        # Attempt to add the screen class as a widget of the AppManager
        try:
            # Check if exit class was specified
            Debug.Log("Checking exit class")
            if(BatiscanMenu_Screens._exitClass == None):
                Debug.Error("Attempted to call exit while no exit class were specified")
                Debug.End()
                return True

            Debug.Log("Checking exit name")
            if(BatiscanMenu_Screens._exitName == None):
                Debug.Error("Attempted to call exit while no exit name were specified")
                Debug.End()
                return True

            Debug.Log("Checking exit class Call()")
            try:
                Debug.Log("Trying to call exit class caller.")
                BatiscanMenu_Screens._exitClass.Call()
                Debug.Log("Success")
                Debug.End()
                return False
            except:
                Debug.Log("Class specified wasn't an _Screen class.")
                AppManager.manager.add_widget(BatiscanMenu_Screens._exitClass(name=BatiscanMenu_Screens._exitName))
        except:
            Debug.Error("AppLoading -> Exception occured.")
            Debug.End()
            return True

        # Attempt to call the added screen
        AppManager.manager.transition = BatiscanMenu_Screens._exitTransition()
        AppManager.manager.transition.duration = BatiscanMenu_Screens._exitDuration
        AppManager.manager.transition.direction = BatiscanMenu_Screens._exitDirection

        # try:
        AppManager.manager.current = BatiscanMenu_Screens._exitName
        # except:
            # return True
        Debug.End()
        return False

    def Call(*args) -> Execution:
        """
            Attempt to go to the main screen that is being handled by this class.

            Returns:
                Execution
        """
        Debug.Start("BatiscanMenu_Screens -> Call()")
        # Attempt to add the screen class as a widget of the AppManager
        try:
            # Check if caller class was specified
            Debug.Log("Checking caller class")
            if(BatiscanMenu_Screens._callerClass == None):
                Debug.Error("No caller class specified.")
                Debug.End()
                return True

            Debug.Log("Checking caller name")
            if(BatiscanMenu_Screens._callerName == None):
                Debug.Error("No caller name specified.")
                Debug.End()
                return True

            Debug.Log("Attempting to add widget")
            AppManager.manager.add_widget(BatiscanMenu(name="BatiscanMenu"))
        except:
            Debug.Error("Exception occured while handling Call()")
            Debug.End()
            return True

        # Attempt to call the added screen
        AppManager.manager.transition = BatiscanMenu_Screens._callerTransition()
        AppManager.manager.transition.duration = BatiscanMenu_Screens._callerDuration
        AppManager.manager.transition.direction = BatiscanMenu_Screens._callerDirection

        # try:
        AppManager.manager.current = "BatiscanMenu"
        Debug.Log("Screen successfully changed")
        # except:
            # Debug.Error("Failed to add AppLoading as current screen.")
            # Debug.End()
            # return True
        Debug.End()
        return False
    #endregion
#====================================================================#
# Classes
#====================================================================#

LoadingLog.Class("NavigationButton")
class NavigationButton(MDIconButton):
    """
        NavigationButton:
        =================
        Summary:
        --------
        This is a custom widget class which was
        made to be put in a bottom card acting as
        a sort of bottom navigation.
    """
    def __init__(self, **kwargs):
        super(NavigationButton, self).__init__(**kwargs)
        self.valign = "center"
        self.halign = "center"
        self.pos_hint = {"center_x":0.5, "center_y":0.5}
        self.size_hint = (1,1)
        self.icon_size = self.size[1]

LoadingLog.Class("InfoDisplayText")
class InfoDisplayText(MDLabel):
    """
        InfoDisplayText:
        =================
        Summary:
        --------
        This is a custom widget class which was
        made to be put in a TopInformationHolder card 
        acting as a label.
    """
    def __init__(self, **kwargs):
        super(InfoDisplayText, self).__init__(**kwargs)
        self.valign = "center"
        self.halign = "center"
        self.pos_hint = {"center_x":0.5, "center_y":0.5}
        self.size_hint = (1,1)
        self.font_style = "H4"

LoadingLog.Class("BottomButtons")
class BottomButtons(MDCard):
   """
        BottomButtons:
        ==============
        Summary:
        --------
        This class is an MDCard spinoff
        that is made to hold :ref:`NavigationButton`
   """
   def __init__(self, **kwargs):
        super(BottomButtons, self).__init__(**kwargs)
        self.shadow_softness = Shadow.Smoothness.default
        self.elevation = Shadow.Elevation.default
        self.shadow_radius = Shadow.Radius.default
        self.radius = Rounding.default

LoadingLog.Class("TopInformation")
class TopInformationHolder(MDCard):
   """
        TopInformationHolder:
        =====================
        Summary:
        --------
        This class is an MDCard spinoff
        that is made to hold :ref:`NavigationButton`
   """
   def __init__(self, **kwargs):
        super(TopInformationHolder, self).__init__(**kwargs)
        self.shadow_softness = Shadow.Smoothness.default
        self.elevation = Shadow.Elevation.default
        self.shadow_radius = Shadow.Radius.default
        self.radius = Rounding.default

LoadingLog.Class("TopInformation")
class CameraCardWidget(MDCard):
    """
        CameraCardWidget:
        ================
        Summary:
        --------
        This class is an MDCard spinoff
        that is made to hold a camera gotten
        from batiscan's data feed.
    """
    streaming:bool = False

    def TurnOff(self, *args):
        """
            TurnOff:
            =======
            Summary:
            --------
            Turns off the camera widget.
            A video off icon is displayed
            until you want to turn it on
            again.
        """
        if self.streaming:
            self.Layout.remove_widget(self.MiddleWidget) # Removing old widget

            if(Information.platform == "Windows"):
                path:str = os.getcwd()

                pathToObj = AppendPath(path, "/Local/Drivers/Batiscan/Pages/submarine.obj")
                pathToGlsl = AppendPath(path, "/Local/Drivers/Batiscan/Pages/submarine.glsl")

                self.MiddleWidget = ObjViewer(pathToOBJ = pathToObj,
                                            pathToglsl = pathToGlsl,
                                            updateIntervals = 1/20,
                                            diffusedLight = (1,-10,0.8),
                                            updatedManually = False)
            else:
                self.MiddleWidget = MDIconButton(icon_color = GetMDCardColor("Light"), pos_hint = {"center_x" : 0.5, "center_y" : 0.5}, size_hint = (0.25,0.25), icon = "video-off", ripple_color = [0,0,0], icon_size = 75)
                self.MiddleWidget.theme_icon_color = "Custom"
                self.MiddleWidget.icon_color = GetMDCardColor("Light")
            self.Layout.add_widget(self.MiddleWidget)
            self.streaming = False

    def TurnOn(self, *args):
        """
            TurnOn:
            =======
            Summary:
            --------
            Turns on the camera widget.
            A spinner is displayed until video
            feed can be received.
        """
        if not self.streaming:
            self.Layout.remove_widget(self.MiddleWidget) # Removing camera icon.

            self.MiddleWidget = MDSpinner(active = True, pos_hint={"center_x" : 0.5, "center_y":0.5})
            self.MiddleWidget.size_hint = (0.25, 0.25)
            self.MiddleWidget.palette = [GetAccentColor(), GetPrimaryColor()]
            self.Layout.add_widget(self.MiddleWidget)
            self.streaming = True

    def DisplayMonkey(self, *args):
        self.Layout.remove_widget(self.MiddleWidget) # Removing camera icon.
        self.streaming = True

        self.MiddleWidget = Image()
        self.MiddleWidget.allow_stretch = True
        self.MiddleWidget.anim_delay = 0.05
        self.MiddleWidget.keep_ratio = False
        self.MiddleWidget.source = "Local/Drivers/Batiscan/Pages/sea-monkey.gif"
        self.MiddleWidget.pos_hint = {"center_x" : 0.5, "center_y" : 0.5}
        self.MiddleWidget.size_hint = (0.95,0.95)
        self.Layout.add_widget(self.MiddleWidget)

    def __init__(self, **kwargs):
        super(CameraCardWidget, self).__init__(**kwargs)
        self.shadow_softness = 0
        self.elevation = 0
        self.shadow_radius = 0
        self.radius = Rounding.default

        self.Layout = MDFloatLayout()

        self.md_bg_color = GetMDCardColor("Dark")
        self.bg_color = GetMDCardColor("Dark")

        if(Information.platform == "Windows"):
            path:str = os.getcwd()
            pathToObj = AppendPath(path, "/Local/Drivers/Batiscan/Pages/submarine.obj")
            pathToGlsl = AppendPath(path, "/Local/Drivers/Batiscan/Pages/submarine.glsl")
            self.MiddleWidget = ObjViewer(pathToOBJ = pathToObj,
                                            pathToglsl = pathToGlsl,
                                            updateIntervals = 1/20,
                                            diffusedLight = (1,10,0.8),
                                            updatedManually = False)
        else:
            self.MiddleWidget = MDIconButton(icon_color = GetMDCardColor("Light"), pos_hint = {"center_x" : 0.5, "center_y" : 0.5}, size_hint = (0.25,0.25), icon = "video-off", ripple_color = [0,0,0], icon_size = 75)
            self.MiddleWidget.theme_icon_color = "Custom"
            self.MiddleWidget.icon_color = GetMDCardColor("Light")

        self.Layout.add_widget(self.MiddleWidget)
        self.add_widget(self.Layout)
        self.streaming = False

LoadingLog.Class("JoystickCard")
class JoystickCard(MDCard):
   joystick:Joystick = None
   def __init__(self, **kwargs):
        super(JoystickCard, self).__init__(**kwargs)
        Debug.Start("JoystickCard")
        self.joystick = Joystick(size_hint = (1.25, 1.25), pos_hint = {"center_x":0.5, "center_y":0.5})
        self.joystick.outer_size                = 0.9/1.25
        self.joystick.inner_size                = 0.55/1.25
        self.joystick.pad_size                  = 0.68/1.25
        self.joystick.outer_line_width          = 0.00
        self.joystick.inner_line_width          = 0.01
        self.joystick.pad_line_width            = 0.01
        self.joystick.outer_background_color    = GetAccentColor("200")#(0.75, 0.75, 0.75, 1)
        self.joystick.outer_line_color          = GetAccentColor("700")#(0.25, 0.25, 0.25, 1)
        self.joystick.inner_background_color    = GetAccentColor("400")#(0.5,  0.5,  0.5,  1)
        self.joystick.inner_line_color          = GetAccentColor("300")#(0.7,  0.7,  0.7,  1)
        self.joystick.pad_background_color      = GetAccentColor("600")#(0.3,  0.3,  0.3,  1)
        self.joystick.pad_line_color            = GetAccentColor("500")#(0.4,  0.4,  0.4,  1)

        self.shadow_softness = Shadow.Smoothness.default
        self.elevation = Shadow.Elevation.default
        self.shadow_radius = Shadow.Radius.default
        self.radius = Rounding.default

        self.add_widget(self.joystick)
        Debug.End()

LoadingLog.Class("BatiscanMenu")
class BatiscanMenu(Screen):
    """
        BatiscanMenu:
        -----------
        This class handles the screen of the Batiscan which shows
        the user the potential things they can debug about their
        Kontrol application.
    """
    #region   --------------------------- MEMBERS
    #endregion
    #region   --------------------------- CONSTRUCTOR
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Debug.Start("BatiscanMenu -> __init__")
        Debug.End()
        #endregion
# ------------------------------------------------------------------------
    def on_pre_enter(self, *args):
        """
        """
        Debug.Start("BatiscanMenu -> on_pre_enter")
        KontrolRGB.FastLoadingAnimation()
        self.padding = 0
        self.spacing = 0

        #region ---------------------------- Background
        from Libraries.BRS_Python_Libraries.BRS.GUI.Utilities.Application_Themes import GetBackgroundImage
        path = os.getcwd()
        background = GetBackgroundImage(AppendPath(path, "/Local/Drivers/Batiscan/Libraries/Backgrounds/Menu/Dark.png"),
                                        AppendPath(path, "/Local/Drivers/Batiscan/Libraries/Backgrounds/Menu/Light.png"))
        #endregion

        #region ---------------------------- Layouts
        self.Layout = MDFloatLayout()
        self.RightJoystickLayout = MDBoxLayout(size_hint = (0.25, 0.25), pos_hint = {'center_x': 0.125,'center_y': 0.25})
        self.LeftJoystickLayout = MDBoxLayout(size_hint = (0.25, 0.25), pos_hint = {'center_x': 0.875,'center_y': 0.25})
        self.ActionButtonCardLayout = MDBoxLayout(size_hint = (1,0.125))
        self.TopInformationLayout = MDBoxLayout(size_hint = (1,0.125), pos_hint = {'center_x': 0.5,'center_y': 0.85})
        self.CameraLayout = MDBoxLayout(size_hint = (0.5,1), pos_hint = {'center_x': 0.5,'center_y': 0.5})
        #endregion

        #region ---------------------------- Buttons
        self.FillBallastButton  = NavigationButton(icon = "basket-fill",       on_release = self._FillPressed)
        self.LightButton        = NavigationButton(icon = "lightbulb-outline",    on_release = self._LightPressed)
        self.SurfaceButton      = NavigationButton(icon = "waves-arrow-up",    on_release = self._SurfacePressed)
        self.CameraButton       = NavigationButton(icon = "video-off",         on_release = self._CameraPressed)
        self.EmptyBallastButton = NavigationButton(icon = "basket-unfill",     on_release = self._EmptyPressed)
        #endregion

        #region ---------------------------- Bottom Action Buttons
        self.ActionButtonsCard = BottomButtons()
        self.ActionButtonsCard.add_widget(self.FillBallastButton)
        self.ActionButtonsCard.add_widget(self.LightButton)
        self.ActionButtonsCard.add_widget(self.SurfaceButton)
        self.ActionButtonsCard.add_widget(self.CameraButton)
        self.ActionButtonsCard.add_widget(self.EmptyBallastButton)
        self.ActionButtonCardLayout.add_widget(self.ActionButtonsCard)
        #endregion

        #region ---------------------------- Top Action Information
        self.TemperatureLabel = InfoDisplayText(text = _("Loading"))
        self.PressureLabel = InfoDisplayText(text = _("Loading"))
        self.BatteryLabel = InfoDisplayText(text =_("Loading"))

        self.TopInformationCard = TopInformationHolder()
        self.TopInformationCard.add_widget(self.TemperatureLabel)
        self.TopInformationCard.add_widget(self.PressureLabel)
        self.TopInformationCard.add_widget(self.BatteryLabel)
        self.TopInformationLayout.add_widget(self.TopInformationCard)
        #endregion

        #region ---------------------------- ToolBar
        from Local.Drivers.Batiscan.Programs.GUI.Navigation import DebugNavigationBar
        self.ToolBar = DebugNavigationBar(pageTitle=_("Batiscan"))
        #endregion

        #region ---------------------------- Joystick
        if(WeNeedLeftJoystick()):
            self.LeftJoystickCard = JoystickCard()
            self.LeftJoystickCard.joystick.bind(pad = self._LeftJoystickMoved)
            self.LeftJoystickLayout.add_widget(self.LeftJoystickCard)

        if(WeNeedRightJoystick()):
            self.RightJoystickCard = JoystickCard()
            self.RightJoystickCard.joystick.bind(pad = self._RightJoystickMoved)
            self.RightJoystickLayout.add_widget(self.RightJoystickCard)
        #endregion

        #region ---------------------------- Camera Display
        self.CameraWidget = CameraCardWidget(size_hint = (0.5,0.5), pos_hint={"center_x":0.5, "center_y":0.5})
        self.CameraLayout.add_widget(self.CameraWidget)
        #endregion

        self.Layout.add_widget(self.TopInformationLayout)
        self.Layout.add_widget(self.ActionButtonCardLayout)
        self.Layout.add_widget(self.LeftJoystickLayout)
        self.Layout.add_widget(self.CameraLayout)
        self.Layout.add_widget(self.RightJoystickLayout)
        self.Layout.add_widget(self.ToolBar.ToolBar)
        self.Layout.add_widget(self.ToolBar.NavDrawer)
        self.add_widget(background)
        self.add_widget(self.Layout)
        Debug.End()
# ------------------------------------------------------------------------
    def on_enter(self, *args):
        """
            Function called when the screen is fully entered in view.
            In this case, once the view is fully loaded, the cards
            will slowly elevate to the wanted value.
        """
        Debug.Start("BatiscanMenu -> on_enter")
        KontrolRGB.DisplayDefaultColor()

        #FIX-ME: This is needed to start updating on screen values.
        BatiscanUDP.SendThing(PlaneIDs.lightsUpdate)

        try:
            self._UpdateArrowAngles()
        except:
            pass

        #region ---------------------------- Updaters
        BatiscanUpdaters.UpdateLeftLightState = self._UpdateLights
        BatiscanUpdaters.UpdateRightLightState = self._UpdateLights
        BatiscanUpdaters.UpdateCameraState = self._UpdateCamera
        BatiscanUpdaters.UpdateBattery = self._UpdateBattery
        BatiscanUpdaters.UpdatePressure = self._UpdatePressure
        BatiscanUpdaters.UpdateTemperature = self._UpdateTemperature
        BatiscanUpdaters.UpdateBallast = self._UpdateFill
        BatiscanUpdaters.UpdateSubmarineAngles = self._UpdateArrowAngles
        #endregion

        Debug.End()
# ------------------------------------------------------------------------
    def on_pre_leave(self, *args):
        """
            Function called before the screen is fully left. This gives
            us time to animate the screen leaving before destroying the
            objects and instances it created.
        """
        Debug.Start("BatiscanMenu -> on_pre_leave")

        BatiscanUpdaters.UpdateLeftLightState = EmptyFunction
        BatiscanUpdaters.UpdateRightLightState = EmptyFunction
        BatiscanUpdaters.UpdateCameraState = EmptyFunction
        BatiscanUpdaters.UpdateBattery = EmptyFunction
        BatiscanUpdaters.UpdatePressure = EmptyFunction
        BatiscanUpdaters.UpdateTemperature = EmptyFunction
        BatiscanUpdaters.UpdateBallast = EmptyFunction
        BatiscanUpdaters.UpdateSubmarineAngles = EmptyFunction

        Debug.End()
# ------------------------------------------------------------------------
    def on_leave(self, *args):
        """
            Function called when the screen is fully out of view.
        """
        Debug.Start("ProfileMenu -> on_leave")
        Debug.Log("Attempting to remove self from AppManager's widgets")
        self.clear_widgets()
        AppManager.manager.remove_widget(self)
        Debug.End()
        self.clear_widgets()
# ------------------------------------------------------------------------
    def _Animating(self, *args):
        """
            Call back function called each time an animation tick happens.
            We use it to add/remove the shadow of cards when entering or
            leaving the application.
        """
        pass
# ------------------------------------------------------------------------
    def _CameraPressed(self, *args):
        Debug.Start("_CameraPressed")
        self.CameraButton.icon = "reload"
        self.CameraButton.disabled = True
        Clock.unschedule(self._CheckOnCamera)

        BatiscanControls.wantedCameraStatus = not BatiscanValues.cameraStatus
        if(BatiscanControls.wantedCameraStatus):
            self.CameraWidget.TurnOn()
        else:
            self.CameraWidget.TurnOff()   
        BatiscanUDP.SendThing(PlaneIDs.cameraUpdate)

        Clock.schedule_once(self._CheckOnCamera, 3)
        Debug.End()
# ------------------------------------------------------------------------
    def _SurfacePressed(self, *args):
        Debug.Start("_SurfacePressed")
        BatiscanControls.wantedSurface = not BatiscanControls.wantedSurface
        BatiscanUDP.SendThing(PlaneIDs.surface)
        Debug.End()
# ------------------------------------------------------------------------
    def _LightPressed(self, *args):
        Debug.Start("_LightPressed")
        self.LightButton.icon = "reload"
        self.LightButton.disabled = True
        Clock.unschedule(self._CheckOnLight)

        BatiscanControls.wantedLeftLight = not BatiscanValues.leftLight
        BatiscanControls.wantedRightLight = not BatiscanValues.rightLight
        BatiscanUDP.SendThing(PlaneIDs.lightsUpdate)

        Clock.schedule_once(self._CheckOnLight, 3)
        Debug.End()
# ------------------------------------------------------------------------
    def _EmptyPressed(self, *args):
        Debug.Start("_EmptyPressed")
        self.EmptyBallastButton.icon = "reload"
        self.EmptyBallastButton.disabled = True
        Clock.unschedule(self._CheckOnBallast)

        BatiscanControls.wantedBallast = False
        BatiscanUDP.SendThing(PlaneIDs.ballastUpdate)

        Clock.schedule_once(self._CheckOnBallast, 6)
        Debug.End()
# ------------------------------------------------------------------------
    def _FillPressed(self, *args):
        Debug.Start("_FillPressed")
        self.FillBallastButton.icon = "reload"
        self.FillBallastButton.disabled = True
        Clock.unschedule(self._CheckOnBallast)

        BatiscanControls.wantedBallast = True
        BatiscanUDP.SendThing(PlaneIDs.ballastUpdate)

        Clock.schedule_once(self._CheckOnBallast, 6)
        Debug.End()
# ------------------------------------------------------------------------
    def _LeftJoystickMoved(self, *args):
        """
            _LeftJoystickMoved:
            ==================
            Summary:
            --------
            Callback function for when the
            left joystick moves.
        """
        yaw   = self.LeftJoystickCard.joystick.pad[0]
        speed = self.LeftJoystickCard.joystick.pad[1]

        BatiscanActions.SetNewSpeed(speed)
        BatiscanActions.SetNewYaw(yaw)
# ------------------------------------------------------------------------
    def _RightJoystickMoved(self, *args):
        """
            _RightJoystickMoved:
            ====================
            Summary:
            --------
            Callback function for when the
            right joystick moves.
        """
        roll   = self.RightJoystickCard.joystick.pad[0]
        pitch = self.RightJoystickCard.joystick.pad[1]

        BatiscanActions.SetNewPitch(pitch)
        BatiscanActions.SetNewRoll(roll)
# ------------------------------------------------------------------------
    def _UpdateCamera(self, *args):
        # Debug.Start("_UpdateCamera")
        if(BatiscanControls.currentCameraStatus != BatiscanValues.cameraStatus):
            Clock.unschedule(self._CheckOnCamera)
            BatiscanControls.currentCameraStatus = BatiscanValues.cameraStatus

            if(BatiscanValues.cameraStatus):
                self.CameraButton.icon = "video"
                # self.CameraWidget.TurnOn()
                self.CameraWidget.streaming = True
                Clock.schedule_once(self._TurnOnMonkey, 0.5)
            else:
                self.CameraButton.icon = "video-off"
                Clock.schedule_once(self.CameraWidget.TurnOff, 0.5)
            self.CameraButton.disabled = False
        # Debug.End()
# ------------------------------------------------------------------------
    def _UpdateSurface(self, *args):
        # Debug.Start("_UpdateSurface")
        # Debug.End()
        pass
# ------------------------------------------------------------------------
    def _UpdateLights(self, *args):
        # Debug.Start("_UpdateLights")
        if(BatiscanControls.currentLeftLight != BatiscanValues.leftLight or BatiscanControls.currentRightLight != BatiscanValues.rightLight):
            Clock.unschedule(self._CheckOnLight)
            self.LightButton.disabled = False
            BatiscanControls.currentLeftLight = BatiscanValues.leftLight
            BatiscanControls.currentRightLight = BatiscanValues.rightLight

            if(BatiscanValues.leftLight or BatiscanValues.rightLight):
                self.LightButton.icon = "lightbulb"
            else:
                self.LightButton.icon = "lightbulb-outline"

        # Debug.End()
# ------------------------------------------------------------------------
    def _UpdateTemperature(self, *args):
        # Debug.Start("_UpdateTemperature")
        if(BatiscanValues.temperature != BatiscanControls.currentTemperature):
            BatiscanControls.currentTemperature = BatiscanValues.temperature
            self.TemperatureLabel.text = str(BatiscanValues.temperature) + BatiscanValues.temperatureUnit
        # Debug.End()
# ------------------------------------------------------------------------
    def _UpdatePressure(self, *args):
        # Debug.Start("_UpdatePressure")
        if(BatiscanValues.pressure != BatiscanControls.currentPressure):
            BatiscanControls.currentPressure = BatiscanValues.pressure
            printed = f"{((BatiscanValues.pressure/10000)-10):.2f}"
            self.PressureLabel.text = printed + " m"
        # Debug.End()
# ------------------------------------------------------------------------
    def _UpdateBattery(self, *args):
        # Debug.Start("_UpdateBattery")
        if(BatiscanValues.battery != BatiscanControls.currentBattery):
            BatiscanControls.currentBattery = BatiscanValues.battery
            self.BatteryLabel.text = str(BatiscanValues.battery) + "%"
        # Debug.End()
# ------------------------------------------------------------------------
    def _UpdateEmpty(self, *args):
        # Debug.Start("_UpdateEmpty")

        if(BatiscanValues.ballast != BatiscanControls.currentBallast):
            BatiscanControls.currentBallast = BatiscanValues.ballast
            Clock.unschedule(self._CheckOnBallast)
            self.EmptyBallastButton.icon = "basket-unfill"
            self.FillBallastButton.icon = "basket-fill"
            if(BatiscanValues.ballast == True):
                self.FillBallastButton.disabled = True
                self.EmptyBallastButton.disabled = False
            else:
                self.FillBallastButton.disabled = False
                self.EmptyBallastButton.disabled = True         
        # Debug.End()
# ------------------------------------------------------------------------
    def _UpdateFill(self, *args):
        # Debug.Start("_UpdateFill")
        if(BatiscanValues.ballast != BatiscanControls.currentBallast):
            BatiscanControls.currentBallast = BatiscanValues.ballast
            Clock.unschedule(self._CheckOnBallast)
            self.EmptyBallastButton.icon = "basket-unfill"
            self.FillBallastButton.icon = "basket-fill"
            if(BatiscanValues.ballast == True):
                self.FillBallastButton.disabled = True
                self.EmptyBallastButton.disabled = False
            else:
                self.FillBallastButton.disabled = False
                self.EmptyBallastButton.disabled = True   
        # Debug.End()
# ------------------------------------------------------------------------
    def _UpdateArrowAngles(self, *args):
        """
            _UpdateArrowAngles:
            ===================
            Summary:
            --------
            Updates the arrow in the middle widget
            that represents
        """
        Clock.schedule_once(self._ChangeValues)
# ------------------------------------------------------------------------
    def _CheckOnLight(self, *args):
        """
            _CheckOnLight:
            ==============
            Summary:
            --------
            Checks if the light icon was updated after
            1 second of being pressed.
        """
        theSame:bool = True

        if(BatiscanValues.leftLight != BatiscanControls.wantedLeftLight):
            BatiscanControls.wantedLeftLight = BatiscanValues.leftLight
            theSame = False

        if(BatiscanValues.rightLight != BatiscanControls.wantedRightLight):
            BatiscanControls.wantedRightLight = BatiscanValues.rightLight
            theSame = False

        if(not theSame):
            BatiscanControls.wantedRightLight = BatiscanValues.rightLight
            BatiscanControls.wantedLeftLight = BatiscanValues.leftLight

            if(BatiscanValues.leftLight or BatiscanValues.rightLight):
                self.LightButton.icon = "lightbulb"
            else:
                self.LightButton.icon = "lightbulb-outline"
        self.LightButton.disabled = False
# ------------------------------------------------------------------------
    def _CheckOnCamera(self, *args):
        """
            _CheckOnCamera:
            ==============
            Summary:
            --------
            Checks if the light icon was updated after
            1 second of being pressed.
        """
        if(BatiscanValues.cameraStatus != BatiscanControls.wantedCameraStatus):
            BatiscanControls.wantedCameraStatus = BatiscanValues.cameraStatus

            if(BatiscanValues.cameraStatus):
                self.CameraButton.icon = "video"
                self.CameraWidget.TurnOn()
            else:
                self.CameraButton.icon = "video-off"
                self.CameraWidget.TurnOff()
        self.CameraButton.disabled = False
# ------------------------------------------------------------------------
    def _CheckOnBallast(self, *args):
        """
            _CheckOnBallast:
            ==============
            Summary:
            --------
            Checks if the light icon was updated after
            1 second of being pressed.
        """
        if(BatiscanValues.ballast != BatiscanControls.wantedBallast):
            BatiscanControls.wantedBallast = BatiscanValues.ballast

        self.FillBallastButton.icon = "basket-fill"
        self.EmptyBallastButton.icon = "basket-unfill"

        if(BatiscanValues.ballast):
            self.FillBallastButton.disabled = True
            self.EmptyBallastButton.disabled = False
        else:
            self.FillBallastButton.disabled = False
            self.EmptyBallastButton.disabled = True
# ------------------------------------------------------------------------
    def _TurnOnMonkey(self, *args):
        self.CameraWidget.DisplayMonkey()
# ------------------------------------------------------------------------
    def _ChangeValues(self, *args):
        if(not self.CameraWidget.streaming and Information.platform == "Windows"):
            pitch = ConvertBatiscanAnglesToDegrees(BatiscanValues.pitch)
            yaw = ConvertBatiscanAnglesToDegrees(BatiscanValues.yaw) + 180
            roll = ConvertBatiscanAnglesToDegrees(BatiscanValues.roll)
            self.CameraWidget.MiddleWidget.SetNewAngles(-pitch, -roll, yaw)
LoadingLog.End("BatiscanMenu.py")