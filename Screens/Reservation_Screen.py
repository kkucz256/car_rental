import requests
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from Car_for_list import Car_for_list
from kivy.uix.gridlayout import GridLayout
from kivy.uix.spinner import Spinner
from kivy.uix.image import Image
import hashlib
import sys

sys.path.append('customclasses')
from Custom_button import CustomButton
from Custom_label import CustomLabel
from Custom_input import CustomTextInput

class ReservationScreen(Screen):
    def __init__(self, **kwargs):
        super(ReservationScreen, self).__init__(**kwargs)
        self.car_id = None
        self.user_id = None
        self.price = 0
        self.days = 0

        self.layout = BoxLayout(orientation='vertical')
        self.layout.size_hint = (None, None)
        self.layout.size = Window.size
        self.layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        self.add_widget(self.layout)

    def update_layout(self):
        label = CustomLabel(
            text=f"car_id: {self.car_id}\nprice: {self.price}\ndays: {self.days}\nuser_id: {self.user_id}",
            valign='middle',
            halign='center'
        )
        label.bind(size=label.setter('text_size'))
        label.size_hint = (None, None)
        label.size = Window.size
        label.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        self.layout.add_widget(label)

    def on_pre_enter(self):
        self.layout.clear_widgets()
        self.update_layout()

    def set_car_id(self, car_id):
        self.car_id = car_id

    def set_user_id(self, user_id):
        self.user_id = user_id

    def set_price(self, price):
        self.price = price

    def set_days(self, days):
        self.days = days
