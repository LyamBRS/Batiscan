#====================================================================#
# File Information
#====================================================================#
"""
    Navigation.py
    =============
    This file contains BRS Kontrol's Batiscan application top
    navigation bar and navigation drawer. It contains classes and
    functions allowing you to quickly get an uniformed tool bar to
    use for your drivers.
"""
#====================================================================#
# Loading Logs
#====================================================================#
from Libraries.BRS_Python_Libraries.BRS.Debug.LoadingLog import LoadingLog
LoadingLog.Start("AppLoading.py")
#====================================================================#
# Imports
#====================================================================#
#region ------------------------------------------------------ Python
LoadingLog.Import("Python")
#endregion
#region --------------------------------------------------------- BRS
LoadingLog.Import("Libraries")
from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog import Debug
from Libraries.BRS_Python_Libraries.BRS.GUI.Utilities.references import Shadow, Rounding
from Libraries.BRS_Python_Libraries.BRS.Utilities.LanguageHandler import _
from Libraries.BRS_Python_Libraries.BRS.GUI.Utilities.colors import GetAccentColor
#endregion
#region -------------------------------------------------------- Kivy
LoadingLog.Import("Kivy")
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle
#endregion
#region ------------------------------------------------------ KivyMD
LoadingLog.Import('KivyMD')
from kivymd.uix.button import BaseButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.recyclegridlayout import RecycleGridLayout
from kivymd.uix.recycleview import RecycleView
from kivymd.uix.list import ThreeLineListItem
from kivymd.uix.label import MDLabel
#endregion

LoadingLog.Import("Local")
#====================================================================#
# Functions
#====================================================================#

#====================================================================#
# Classes
#====================================================================#
LoadingLog.Class("ListCard")
class ListCard(BaseButton, Widget):
    #region   --------------------------- DOCSTRING
    ''' 
        ListCard:
        ===========
        Summary:
        --------
        This class is used to create a card that displays a dictionary
        with a title associated with it.
    '''
    #endregion
    #region   --------------------------- MEMBERS
    banner_rect = None
    savedData = None
    #endregion
    #region   --------------------------- METHODS
    #region   -- Public
    def PressedEnd(self, *args):
        """
            Function called by the card once the ripple effect
            comes to an end.
        """
        pass
    #endregion
    #region   -- Private
    # ------------------------------------------------------
    def _RippleHandling(self, object, finished):
        if(finished):
            self.PressedEnd(self)
    # ------------------------------------------------------
    def UpdateBanner(self, *args):
        banner_width = self.TitleLayout.width
        banner_height = self.TitleLayout.height + 5

        if self.banner_rect:
            self.banner_rect.pos = (self.TitleLayout.x, self.TitleLayout.y - 6)
            self.banner_rect.size = (banner_width, banner_height)
        else:
            corner:str = Rounding.Cards.default.replace("dp","")
            corner = int(corner)
            with self.TitleLayout.canvas.before:
                Color(*self.banner_color)
                self.banner_rect = RoundedRectangle(pos=self.TitleLayout.pos, size=(banner_width, banner_height), radius=[corner, corner, corner, corner])
    # ------------------------------------------------------
    def CreateRecycleLayout(self):
        Debug.Start("CreateRecycleLayout")
        self.RecycleBoxLayout = RecycleGridLayout(default_size=(None,72),
                                                        default_size_hint=(1, None),
                                                        size_hint=(1, None),
                                                        orientation='lr-tb')
        self.RecycleBoxLayout.padding = 25
        self.RecycleBoxLayout.spacing = 5
        self.RecycleBoxLayout.cols = 1

        self.RecycleBoxLayout.bind(minimum_height=self.RecycleBoxLayout.setter("height"))

        self.RecycleView = RecycleView()
        self.RecycleView.add_widget(self.RecycleBoxLayout)
        self.RecycleView.viewclass = ThreeLineListItem
        self.RecycleViewLayout.add_widget(self.RecycleView)
        self.RecycleViewLayout.add_widget(MDLabel(text="AAAH"))

        for data in self.savedData:
            Debug.Log(data)
            firstLine = data["text"]
            secondLine = data["secondary_text"]
            thirdLine = data["tertiary_text"]

            self.RecycleView.data.insert(0,
                                         {
                                             "text" : firstLine,
                                             "secondary_text" : secondLine,
                                             "tertiary_text" : thirdLine,
                                             "halign" : "left",
                                         })
        Debug.End()
    #endregion
    #endregion
    #region   --------------------------- CONSTRUCTOR
    def __init__(self,
                 initialDataList:list,
                 title:str="",
                 **kwargs):
        """
            list: [{text : text, secondary_text: secondary_text, tertiary_text: tertiary_text}]
        """
        super(ListCard, self).__init__(**kwargs)
        Debug.Start("ListCard")
        #region --------------------------- Initial check ups
        self.padding = 0
        self.spacing = 0

        self.savedData = initialDataList

        self.bind(_finishing_ripple = self._RippleHandling)

        self.Card = MDCard()
        self.Card.orientation = "vertical"
        self.Card.elevation = Shadow.Elevation.default
        self.Card.shadow_softness = Shadow.Smoothness.default
        self.Card.radius = Rounding.Cards.default
        self.size = (400,425)
        self.disabled = True
        #endregion

        #region --------------------------- Widgets
        self.Layout = MDFloatLayout()
        self.Layout.size_hint = (1,1)

        self.TitleLayout = MDBoxLayout()
        self.TitleLayout.orientation = "horizontal"
        # self.RequirementsLayout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.TitleLayout.size_hint = (1, 0.15)

        self.ListLayout = MDBoxLayout()
        self.ListLayout.orientation = "horizontal"
        # self.RequirementsLayout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.ListLayout.size_hint = (1, 0.5)
        self.ListLayout.pos_hint = { 'center_x': 0.5, 'center_y': 0.5 }

        self.Name = MDLabel(text=title, font_style = "H4", halign = "center")
        self.Name.pos_hint = { 'center_x': 0.5, 'center_y': 0.5 }

        self.RecycleViewLayout = MDBoxLayout(orientation="vertical", padding=20, pos_hint = { 'center_x': 0.5, 'center_y': 0.5 })
        #endregion

        #region --------------------------- Array handling
        Debug.Log("Putting keys and values in card")
        #endregion

        self.TitleLayout.add_widget(self.Name)
        self.Layout.add_widget(self.ListLayout)
        self.Card.add_widget(self.TitleLayout)
        self.Card.add_widget(self.Layout)
        self.add_widget(self.Card)
        #region --------------------------- Canvas
        # Adding a banner to the top of the card for requirement
        # icons to be layed on.
        self.banner_color = GetAccentColor()
        self.TitleLayout.bind(pos=self.UpdateBanner, size=self.UpdateBanner)

        #endregion

        Debug.End()
    #endregion
    pass
#====================================================================#
LoadingLog.End("Navigation.py")