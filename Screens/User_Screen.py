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
from Car_for_list import Car_for_list
from kivy.uix.gridlayout import GridLayout
from kivy.uix.spinner import Spinner
from kivy.uix.image import Image
import hashlib
import sys

# Tutaj dawaj importy z tej ścieżki
sys.path.append('customclasses')
from Custom_button import CustomButton
from Custom_label import CustomLabel
from Custom_input import CustomTextInput


class UserScreen(Screen):

    def __init__(self, **kwargs):

        self.filter_price_input = None
        self.filter_seats_input = None
        self.filter_body_input = None
        self.filter_brand_input = None
        self.cars = []
        self.org = []
        self.user_id = None
        self.sort_value = 90
        self.component_height = 50

        super(UserScreen, self).__init__(**kwargs)

    def create_layout(self):
        self.img = Image(source="images/logo.png")
        self.img.size = (300, 300)
        self.img.size_hint = (None, None)
        self.img.pos_hint = {'center_x': 0.09, 'center_y': 0.9}
        self.clear_widgets()

        scrollview = ScrollView(size_hint=(None, None), size=(1000, 800),do_scroll_x=False, do_scroll_y=True, pos_hint={'center_x': 0.68, 'center_y': 0.4})


        car_list_layout = GridLayout(cols=1, size_hint_x=0.8, size_hint_y=1.3, padding=10, spacing=10)
        car_list_layout.bind(minimum_height=car_list_layout.setter('height'))

        for car in self.cars:
            car_info = (
                f"{car.color} {car.brand} {car.model} \n"
                f"Body: {car.body}, Gearbox: {car.gearbox}, Places: {car.places}\n"
                f"Price per Day: ${car.price_per_day}"
            )
            car_button = Button(
                text=car_info,
                size_hint_y=None,
                size_hint_x=0.5,
                height=120,
                background_normal='',
                background_color=(8 / 255, 32 / 255, 50 / 255, 1),
                color=(1, 1, 1, 1),
                halign='center',
                valign='middle',
                border=(0, 0, 0, 1),
                padding=[0, 10, 0, 10]
            )
            car_button.bind(size=lambda btn, *args: setattr(btn, 'text_size', (btn.width, None)))
            car_button.bind(on_press=lambda btn, car_id=car.id: self.car_details(car_id))
            car_list_layout.add_widget(car_button)

        scrollview.add_widget(car_list_layout)

        back_button = CustomButton(text='Back')
        sort_button = CustomButton(text='Sort')

        sort_layout = BoxLayout(orientation='vertical', size_hint=(None, None), height=self.component_height,
                                spacing=10,
                                pos_hint={'center_x': 0.05, 'center_y': 0.2})
        spinner = Spinner(
            text='Pick sorting option',
            values=('Price per day descending', 'Price per day ascending', 'Brand alphabetically',
                    'Brand analphabetically'),
            size_hint=(None, None),
            size=(200, 44),
            background_color=(1, 76 / 255, 41 / 256, 1),

        )

        spinner.bind(text=self.on_spinner_text_changed)
        sort_layout.add_widget(spinner)
        sort_layout.add_widget(sort_button)

        self.filter_brand_input = CustomTextInput(hint_text='Enter brand')
        self.filter_body_input = CustomTextInput(hint_text='Enter body type')
        self.filter_seats_input = CustomTextInput(hint_text='Enter number of seats')
        self.filter_price_input = CustomTextInput(hint_text='Enter maximum price')

        filter_button = CustomButton(text='Filter')
        default_button = CustomButton(text='Default list')
        filter_button.bind(on_press=self.filter_cars)
        default_button.bind(on_press=self.default)

        sort_layout.add_widget(self.filter_brand_input)
        sort_layout.add_widget(self.filter_body_input)
        sort_layout.add_widget(self.filter_seats_input)
        sort_layout.add_widget(self.filter_price_input)
        sort_layout.add_widget(filter_button)
        sort_layout.add_widget(default_button)

        sort_layout.add_widget(back_button)

        self.add_widget(self.img)
        self.add_widget(sort_layout)
        self.add_widget(scrollview)

        back_button.bind(on_press=self.go_back)
        sort_button.bind(on_press=self.sorting)

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()

    def on_pre_enter(self):
        Window.size = (1280, 720)
        Window.position = 'custom'
        Window.left = 320
        Window.top = 180
        url = 'http://127.0.0.1:5000/user-screen'
        response = requests.get(url)
        response_json = response.json()
        self.cars = []
        for elem in response_json:
            self.cars.append(
                Car_for_list(elem['id'], elem['brand'], elem['color'], elem['model'], elem['price_per_day'],
                             elem['body'], elem['gearbox'], elem['places']))
        self.org = self.cars
        self.create_layout()

    def go_back(self, instance):
        self.manager.current = 'login'

    def set_user_id(self, user_id):
        self.user_id = user_id

    def on_leave(self):
        Window.size = (800, 600)

    def car_details(self, car_id):
        self.manager.get_screen('car').set_car_id(car_id)
        self.manager.get_screen('car').set_user_id(self.user_id)
        self.manager.current = 'car'

    def on_spinner_text_changed(self, spinner, text):
        if text == 'Price per day descending':
            self.sort_value = 0
        elif text == 'Price per day ascending':
            self.sort_value = 1
        elif text == 'Brand alphabetically':
            self.sort_value = 2
        elif text == 'Brand analphabetically':
            self.sort_value = 3

    def sorting(self, instance):
        if self.sort_value == 0:
            self.cars.sort(key=lambda car: car.price_per_day, reverse=True)
        elif self.sort_value == 1:
            self.cars.sort(key=lambda car: car.price_per_day)
        elif self.sort_value == 2:
            self.cars.sort(key=lambda car: car.brand[0])
        elif self.sort_value == 3:
            self.cars.sort(key=lambda car: car.brand[0], reverse=True)
        self.create_layout()

    def filter_cars(self, instance):
        filter_body = self.filter_body_input.text.strip()
        filter_brand = self.filter_brand_input.text.strip()
        filter_seats = self.filter_seats_input.text.strip()
        filter_price = self.filter_price_input.text.strip()

        filtered = self.cars

        if filter_body:
            filtered = list(filter(lambda car: contains_substring(car.body, filter_body), filtered))

        if filter_brand:
            filtered = list(filter(lambda car: contains_substring(car.brand, filter_brand), filtered))

        if filter_seats:
            try:
                seats = int(filter_seats)
                filtered = list(filter(lambda car: car.places == seats, filtered))
            except ValueError:
                pass

        if filter_price:
            try:
                price = float(filter_price)
                filtered = list(filter(lambda car: car.price_per_day <= price, filtered))
            except ValueError:
                pass

        self.cars = filtered

        self.create_layout()

    def default(self, instance):
        self.cars = self.org
        self.create_layout()


def contains_substring(main_string, substring):
    return substring.lower() in main_string.lower()
