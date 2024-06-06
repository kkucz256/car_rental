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
import requests

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

        self.layout = BoxLayout(spacing=10, orientation='vertical')

        self.layout.size_hint = (1, 1)
        self.layout.size = (800, 600)
        self.layout.pos_hint = {'center_x': 0.87, 'center_y': 0.77}

        self.add_widget(self.layout)

    def update_layout(self):
        self.img = Image(source="images/logo.png")
        self.img.size = (300, 300)
        self.img.size_hint = (None, None)
        self.img.pos_hint = {'center_x': 0.5, 'center_y': 0.8}
        user_response = requests.get(f'http://127.0.0.1:5000/user-details/{self.user_id}')
        if user_response.status_code == 200:
            user_data = user_response.json()
            user_name = f"{user_data['first_name']} {user_data['last_name']}"
        else:
            user_name = "User not found"

        car_response = requests.get(f'http://127.0.0.1:5000/car-details/{self.car_id}')
        if car_response.status_code == 200:
            car_data = car_response.json()
            car_info = f"{car_data['color']} {car_data['brand']} {car_data['model']}"
        else:
            car_info = "Car not found"

        self.layout.clear_widgets()

        label = CustomLabel(
            text=f"{user_name} is trying to book:\n{car_info}\nFor {self.price} PLN\nFor {self.days} days",
            size_hint=(None, None),
            height=200,
            width=300,
            halign='center'
        )
        label.bind(size=label.setter('text_size'))

        info_label = CustomLabel(text="Type starting date of your rental:")
        self.date_input = CustomTextInput(_hint_text="YYYY-MM-DD")

        back_button = CustomButton(text="Back")
        back_button.bind(on_press=self.go_back)
        self.layout.add_widget(label)
        self.layout.add_widget(info_label)
        self.layout.add_widget(self.date_input)
        self.layout.add_widget(back_button)
        self.add_widget(self.img)

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

    def go_back(self, instance):
        self.manager.current = 'car'
