#====================================================================#
# File Information
#====================================================================#

#====================================================================#
from Libraries.BRS_Python_Libraries.BRS.Debug.LoadingLog import LoadingLog
LoadingLog.Start("AboutMenu.py")
#====================================================================#
# Imports
#====================================================================#
#region ------------------------------------------------------ Python
LoadingLog.Import("Python")
#endregion
#region --------------------------------------------------------- BRS
LoadingLog.Import("Libraries")
from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog import Debug
from Libraries.BRS_Python_Libraries.BRS.Utilities.AppScreenHandler import AppManager
from Libraries.BRS_Python_Libraries.BRS.Utilities.LanguageHandler import _
# from Libraries.BRS_Python_Libraries.BRS.GUI.Utilities.references import Shadow, Rounding
from Libraries.BRS_Python_Libraries.BRS.Utilities.Enums import Execution
from Libraries.BRS_Python_Libraries.BRS.PnP.controls import Controls
from Local.Drivers.Batiscan.Programs.GUI.Navigation import DebugNavigationBar
#endregion
#region -------------------------------------------------------- Kivy
LoadingLog.Import("Kivy")
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.recyclegridlayout import RecycleGridLayout
#endregion
#region ------------------------------------------------------ KivyMD
LoadingLog.Import("KivyMD")
# from kivymd.uix.button import MDIconButton
# from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.list import ThreeLineRightIconListItem, IconRightWidget
from kivymd.uix.recycleview import RecycleView
#endregion
#region ------------------------------------------------------ Kontrol
LoadingLog.Import("Local")
from Programs.Local.Hardware.RGB import KontrolRGB
from Local.Drivers.Batiscan.Programs.Controls.actions import batiscanAxesActions, batiscanButtonsActions
# from Local.Drivers.Batiscan.Programs.GUI.joystick import Joystick
# from Programs.Local.GUI.Cards import ButtonCard, DeviceDriverCard
# from Programs.Pages.PopUps import PopUpsHandler, PopUps_Screens, PopUpTypeEnum
#endregion
#====================================================================#
# Functions
#====================================================================#
from kivy.properties import StringProperty
class CustomThreeLineIconListItem(ThreeLineRightIconListItem):
    """
        CustomThreeLineIconListItem:
        ============================
        Summary:
        --------
        This is used to display a widget
        in the debugger menu that when clicked,
        tried to send an UDP message to Batiscan.
    """
    icon = StringProperty()

    def __init__(self, **kwargs):
        super(CustomThreeLineIconListItem, self).__init__(**kwargs)
        self.icon_widget = IconRightWidget(icon="trash-can")
        self.ids._right_container.add_widget(self.icon_widget)
        self.icon_widget.bind(on_release=lambda x: self.on_icon_press(x))

    def on_icon_press(self, *args):
        Debug.Start("on_icon_press")

        Debug.Log("Gathering informations...")
        textFromLine1 = self.text
        textFromLine2 = self.secondary_text
        textFromLine3 = self.tertiary_text

        Debug.Log(f">>> line1: {textFromLine1}")
        Debug.Log(f">>> line2: {textFromLine2}")
        Debug.Log(f">>> line3: {textFromLine3}")

        Debug.End()

#====================================================================#
# Screen class
#====================================================================#
LoadingLog.Class("AboutMenu_Screens")
class AboutMenu_Screens:
    """
        AboutMenu_Screens:
        ================
        Summary:
        --------
        This class allows the handling of the transitional screen
        :class:`AboutMenu`.

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
        AboutMenu_Screens._exitClass = screenClass
        AboutMenu_Screens._exitName  = screenName

        AboutMenu_Screens._exitTransition = transition
        AboutMenu_Screens._exitDuration = duration
        AboutMenu_Screens._exitDirection = direction
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
        AboutMenu_Screens._callerClass = screenClass
        AboutMenu_Screens._callerName  = screenName

        AboutMenu_Screens._callerTransition = transition
        AboutMenu_Screens._callerDuration = duration
        AboutMenu_Screens._callerDirection = direction
        return False

    def _Exit(*args) -> Execution:
        """
            Attempt to go to the specified screen that was set using :ref:`SetExiter`.

            Returns:
                bool: `True`:  Something went wrong and the wanted exiter screen can't be loaded. `False`: Success
        """
        Debug.Start("AboutMenu_Screens -> _Exit()")
        # Attempt to add the screen class as a widget of the AppManager
        try:
            # Check if exit class was specified
            Debug.Log("Checking exit class")
            if(AboutMenu_Screens._exitClass == None):
                Debug.Error("Attempted to call exit while no exit class were specified")
                Debug.End()
                return True

            Debug.Log("Checking exit name")
            if(AboutMenu_Screens._exitName == None):
                Debug.Error("Attempted to call exit while no exit name were specified")
                Debug.End()
                return True

            Debug.Log("Checking exit class Call()")
            try:
                Debug.Log("Trying to call exit class caller.")
                AboutMenu_Screens._exitClass.Call()
                Debug.Log("Success")
                Debug.End()
                return False
            except:
                Debug.Log("Class specified wasn't an _Screen class.")
                AppManager.manager.add_widget(AboutMenu_Screens._exitClass(name=AboutMenu_Screens._exitName))
        except:
            Debug.Error("AppLoading -> Exception occured.")
            Debug.End()
            return True

        # Attempt to call the added screen
        AppManager.manager.transition = AboutMenu_Screens._exitTransition()
        AppManager.manager.transition.duration = AboutMenu_Screens._exitDuration
        AppManager.manager.transition.direction = AboutMenu_Screens._exitDirection

        # try:
        AppManager.manager.current = AboutMenu_Screens._exitName
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
        Debug.Start("AboutMenu_Screens -> Call()")
        # Attempt to add the screen class as a widget of the AppManager
        try:
            # Check if caller class was specified
            # Debug.Log("Checking caller class")
            # if(AboutMenu_Screens._callerClass == None):
                # Debug.Error("No caller class specified.")
                # Debug.End()
                # return True
# 
            # Debug.Log("Checking caller name")
            # if(AboutMenu_Screens._callerName == None):
                # Debug.Error("No caller name specified.")
                # Debug.End()
                # return True

            Debug.Log("Attempting to add widget")
            AppManager.manager.add_widget(AboutMenu(name="AboutMenu"))
        except:
            Debug.Error("Exception occured while handling Call()")
            Debug.End()
            return True

        # Attempt to call the added screen
        AppManager.manager.transition = AboutMenu_Screens._callerTransition()
        AppManager.manager.transition.duration = AboutMenu_Screens._callerDuration
        AppManager.manager.transition.direction = AboutMenu_Screens._callerDirection

        # try:
        AppManager.manager.current = "AboutMenu"
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
BFIO_Functions = {
    "Ping":                     {"Callsign": 0},
    "Exchange status":          {"Callsign": 1},
    "Handshake":                {"Callsign": 2},
    "Exchange error message":   {"Callsign": 3},
    "Exchange types":           {"Callsign": 4},
    "Exchange IDs":             {"Callsign": 5},
    "Restart Protocol":         {"Callsign": 6},
    "Exchange Universal Infos": {"Callsign": 7},
    "Send error":               {"Callsign": 8},
    "Update Lights":            {"Callsign": 20},
    "Update Servos":            {"Callsign": 21},
    "Update Modes":             {"Callsign": 22},
    "Update Camera":            {"Callsign": 23},
    "Get all states":           {"Callsign": 24},
    "Update navigation":        {"Callsign": 25}
}


LoadingLog.Class("AboutMenu")
class AboutMenu(Screen):
    """
        AboutMenu:
        -----------
        This class handles the screen of the account menu which shows
        to the user some actions that they can do with their user profiles
    """
    #region   --------------------------- MEMBERS
    ToolBar:DebugNavigationBar = None
    #endregion
    #region   --------------------------- CONSTRUCTOR
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Debug.Start("ControlMenu -> __init__")
        Debug.End()
        #endregion
# ------------------------------------------------------------------------
    def on_pre_enter(self, *args):
        """
        """
        Debug.Start("AboutMenu -> on_pre_enter")
        KontrolRGB.FastLoadingAnimation()
        self.padding = 0
        self.spacing = 0

        #region ---- Background
        import os
        from Libraries.BRS_Python_Libraries.BRS.GUI.Utilities.Application_Themes import GetBackgroundImage
        from Libraries.BRS_Python_Libraries.BRS.Utilities.FileHandler import AppendPath
        path = os.getcwd()

        background = GetBackgroundImage(AppendPath(path, "/Libraries/Backgrounds/Menus/Dark.png"),
                                        AppendPath(path, "/Libraries/Backgrounds/Menus/Light.png"))
        #endregion

        #region ---------------------------- Layouts
        self.Layout = MDFloatLayout()
        # Add widgets
        self.add_widget(background)
        #endregion
        #region ---------------------------- ToolBar
        self.ToolBar = DebugNavigationBar(pageTitle=_("About Batiscan"))
        #endregion

        self.create_layouts()

        self.Layout.add_widget(self.ToolBar.ToolBar)
        self.Layout.add_widget(self.ToolBar.NavDrawer)
        self.add_widget(self.Layout)
        Debug.End()
# ------------------------------------------------------------------------
    def on_enter(self, *args):
        """
            Function called when the screen is fully entered in view.
            In this case, once the view is fully loaded, the cards
            will slowly elevate to the wanted value.
        """
        Debug.Start("AboutMenu -> on_enter")
        KontrolRGB.DisplayDefaultColor()
        Debug.End()
# ------------------------------------------------------------------------
    def on_pre_leave(self, *args):
        """
            Function called before the screen is fully left. This gives
            us time to animate the screen leaving before destroying the
            objects and instances it created.
        """
        Debug.Start("AboutMenu -> on_pre_leave")
        Debug.End()
# ------------------------------------------------------------------------
    def on_leave(self, *args):
        """
            Function called when the screen is fully out of view.
        """
        Debug.Start("AboutMenu -> on_leave")
        Debug.Log("Attempting to remove self from AppManager's widgets")
        self.clear_widgets()
        AppManager.manager.remove_widget(self)
        Debug.End()
        self.clear_widgets()
# ------------------------------------------------------------------------
    def create_layouts(self,*args):
        Debug.Start("create_layouts")
        self.create_recycle_view()
        Debug.End()
# ------------------------------------------------------------------------
    def create_recycle_view(self):
        Debug.Start("create_recycle_view")
        self.RecyleBoxLayout = RecycleGridLayout(default_size=(None,72),
                                                default_size_hint=(1, None),
                                                size_hint=(1, None),
                                                orientation='lr-tb')
        self.RecyleBoxLayout.padding = 25
        self.RecyleBoxLayout.spacing = 5
        self.RecyleBoxLayout.cols = 1
        # self.RecyleBoxLayout.orientation
        self.RecyleBoxLayout.bind(minimum_height=self.RecyleBoxLayout.setter("height"))

        self.recycleView = RecycleView()
        self.recycleView.pos_hint = {"center_x" : 0.5, "center_y" : 0.45}
        self.recycleView.size_hint = (1,0.90)
        self.recycleView.add_widget(self.RecyleBoxLayout)
        self.recycleView.viewclass = CustomThreeLineIconListItem
        self.Layout.add_widget(self.recycleView)

        buttonIntroducer = _("Button") + ": "
        axisIntroducer = _("Axis") + ": "

        for name,dictionary in batiscanAxesActions.items():
            description = _(dictionary["description"])
            if(Controls._axes[name]["binded"]):
                bindInformation = Controls._axes[name]["bindedTo"] + ": " + Controls._axes[name]["bindedAs"]
            else:
                bindInformation = _("Not binded")

            self.recycleView.data.insert(0,
                                         {
                                             "text" : axisIntroducer + name,
                                             "secondary_text" : description,
                                             "tertiary_text" : bindInformation,
                                             "halign" : "left"
                                         })
            
        for name,dictionary in batiscanButtonsActions.items():
            description = _(dictionary["description"])
            if(Controls._buttons[name]["binded"]):
                bindInformation = Controls._buttons[name]["bindedTo"] + ": " + Controls._buttons[name]["bindedAs"]
            else:
                bindInformation = _("Not binded")

            self.recycleView.data.append({
                                             "text" : buttonIntroducer + name,
                                             "secondary_text" : description,
                                             "tertiary_text" : bindInformation,
                                             "halign" : "left"
                                         })
        Debug.End()
# ------------------------------------------------------------------------
    def ButtonPressed(self, *args):
        """
            ButtonPressed:
            ==============
            Summary:
            --------
            Callback function executed when a button is
            pressed.
        """
        Debug.Start("ButtonPressed")
        Debug.Log(args)

        from kivymd.uix.button import MDFillRoundFlatButton

        dialog = MDDialog(
            title=_("Arguments:"),
            text=str(args),
            buttons=[
                MDFillRoundFlatButton(text=_("I guess yeah"), font_style="H6")
            ]
        )
        dialog.open()

        Debug.End()
# ------------------------------------------------------------------------
LoadingLog.End("AboutMenu.py")