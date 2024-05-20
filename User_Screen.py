import requests
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from Manager import ManagerScreen
from kivy.core.window import Window


import hashlib

class UserScreen(Screen):
    def __init__(self, **kwargs):
        super(UserScreen, self).__init__(**kwargs)
        self.size_hint = (None, None)


    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()

    def on_pre_enter(self):
        Window.size = (1280, 720)
        Window.position = 'custom'
        Window.left = 320
        Window.top = 180


    def on_leave(self):
        Window.size = (800, 600)