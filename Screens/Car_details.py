from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.slider import Slider
import requests
from Car_details_class import Car_details_class
from kivy.uix.image import Image
from kivy.uix.image import AsyncImage
import sys


sys.path.append('customclasses')
from Custom_button import CustomButton
from Custom_label import CustomLabel
from Custom_input import CustomTextInput


class CarDetails(Screen):
    def __init__(self, **kwargs):
        super(CarDetails, self).__init__(**kwargs)
        self.car_id = None
        self.user_id = None
        self.car = Car_details_class()
        self.details_dict = {}
        self.price = 0
        self.days = 0
        self.staff_access = False

        self.layout = BoxLayout(orientation='vertical', size_hint=(1, 1), pos_hint={'center_x': 1.1, 'center_y': 0.72})
        self.add_widget(self.layout)

    def on_pre_enter(self):

        if self.car_id:
            url = f'http://127.0.0.1:5000/car-details/{self.car_id}'
            response = requests.get(url)
            car_data = response.json()
            if 'error' not in car_data:
                self.car = Car_details_class(
                    car_data['id'], car_data['brand'], car_data['status'], car_data['price_per_day'],
                    car_data['year_of_production'], car_data['horsepower'], car_data['engine_type'],
                    car_data['body'], car_data['color'], car_data['max_velocity'], car_data['gearbox'],
                    car_data['seats_no'], car_data['deposit'], car_data['last_rental_end'], car_data['model'],
                    car_data['photo']
                )
                self.details_dict = {
                    "Body ": self.car.body,
                    "Gearbox ": self.car.gearbox,
                    "Number of seats ": self.car.seats_no,
                    "Year of production ": self.car.year_of_production,
                    "Horsepower ": self.car.horsepower}

                self.update_layout()

            else:
                self.layout.add_widget(Label(text=car_data['error']))
        else:
            self.layout.add_widget(Label(text="Car ID is not defined"))

    def set_car_id(self, car_id):
        self.car_id = car_id

    def set_user_id(self, user_id):
        self.user_id = user_id

    def update_layout(self):
        self.clear_widgets()
        self.layout.clear_widgets()
        self.add_widget(self.layout)
        self.layout.add_widget(Label())

        upper_left_layout = BoxLayout(orientation='vertical', pos_hint={'center_x': 0.4895, 'center_y': 0.9})
        self.img = AsyncImage(source=self.car.photo)
        self.img.size = (500, 400)
        self.img.size_hint = (None, None)
        upper_left_layout.add_widget(self.img)
        self.add_widget(upper_left_layout)

        upper_right_layout = BoxLayout(orientation='vertical', pos_hint={'right': 1, 'top': 1})
        main_info_label = CustomLabel(
            text=f"{self.car.color} {self.car.brand} {self.car.model}",
            font_size=30,
            size_hint_y=None,
            height=150,
            valign='bottom'
        )
        status_label = CustomLabel(text=self.status_text())
        price_deposit_label = CustomLabel(
            text=f"Price per Day: ${self.car.price_per_day} Deposit: ${self.car.deposit}",
            height=100
        )
        details_label_1 = CustomLabel(text='Details:', font_size=20, size_hint_y=None, height=50)

        for detail_key, detail_value in self.details_dict.items():
            upper_right_layout.add_widget(
                CustomLabel(text=f"{detail_key}: {detail_value}", size_hint_y=None, height=30, halign='center'))

        x_center = 0
        if not self.staff_access:
            self.buy_button = CustomButton(text='Buy')
            self.buy_button.bind(
                on_press=lambda btn: self.reservation(self.car_id, self.price, self.days))
            x_center = 0.75
        else:
            x_center = 0.85

        buttons_layout = GridLayout(cols=2, size_hint_y=None, spacing=10, height=50,
                                    pos_hint={'center_x': x_center, 'center_y': 0.05})
        buttons_layout.add_widget(CustomButton(text='Back', on_press=self.go_back))




        bottom_left_layout = BoxLayout(orientation='vertical', spacing=10, size_hint=(.5, .3),
                                       pos_hint={'center_y': 0.3})
        self.s = Slider(orientation='horizontal', min=1, max=30, value=7, step=1, value_track=True)
        self.s.bind(value=self.update_price_label)
        self.days = self.s.value
        self.price = self.s.value * self.car.price_per_day
        self.days_label = CustomLabel(text=f"Choose the amount of days: {self.days}", font_size=15,
                                      pos_hint={'center_x': 0.5})
        self.price_label = CustomLabel(text=f"Price: {self.price}", font_size=15, pos_hint={'center_x': 0.5})

        upper_right_layout.add_widget(main_info_label)
        upper_right_layout.add_widget(status_label)
        upper_right_layout.add_widget(price_deposit_label)
        upper_right_layout.add_widget(details_label_1)
        self.layout.add_widget(upper_right_layout)
        if not self.staff_access:
            buttons_layout.add_widget(self.buy_button)
        self.add_widget(buttons_layout)

        bottom_left_layout.clear_widgets()
        bottom_left_layout.add_widget(self.days_label)
        bottom_left_layout.add_widget(self.s)
        bottom_left_layout.add_widget(self.price_label)

        self.add_widget(bottom_left_layout)



    def update_price_label(self, instance, value):
        self.days = self.s.value
        self.price = self.s.value * self.car.price_per_day
        self.days_label.text = f"Choose the amount of days: {self.days}"
        self.price_label.text = f"Price: {self.price}"

    def set_staff_access(self, access):
        self.staff_access = access


    def go_back(self, instance):
        self.manager.current = 'user'

    def reservation(self, car_id, price, days):
        self.update_price_label(None, self.s.value)
        self.manager.get_screen('reservation').set_car_id(car_id)
        self.manager.get_screen('reservation').set_price(price)
        self.manager.get_screen('reservation').set_days(days)
        self.manager.get_screen('reservation').set_user_id(self.user_id)
        self.manager.current = 'reservation'

    def status_text(self):
        if self.car.status == 'free':
            return "The car is currently available"
        if self.car.status == 'booked':
            return f"The car is currently taken, it will be available on: {self.car.last_rental_end}"
