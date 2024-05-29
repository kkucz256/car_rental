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

import hashlib


class UserScreen(Screen):

    def __init__(self, **kwargs):

        self.filter_price_input = None
        self.filter_seats_input = None
        self.filter_body_input = None
        self.filter_brand_input = None
        self.cars = []
        self.org=[]
        self.sort_value = 90

        super(UserScreen, self).__init__(**kwargs)

        self.button_color = (34 / 255, 40 / 255, 49 / 255, 1)

        self.component_width = 200
        self.component_height = 50

    def create_layout(self):
        self.clear_widgets()

        scrollview = ScrollView(do_scroll_x=False, do_scroll_y=True)

        car_list_layout = GridLayout(cols=1, size_hint_y=None, padding=10, spacing=10)
        car_list_layout.bind(minimum_height=car_list_layout.setter('height'))

        for car in self.cars:
            car_info = (
                f"{car.color} {car.brand} {car.model} \n"
                f"Body: {car.body}, Gearbox: {car.gearbox}, Places: {car.places}\n"
                f"Price per Day: PLN{car.price_per_day}"
            )
            car_button = Button(
                text=car_info,
                size_hint_y=None,
                size_hint_x=0.6,
                height=120,
                background_normal='',
                background_color=(0.5, 0.5, 0.5, 1),
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

        back_button = Button(text='Back', size_hint=(None, None), background_color=self.button_color,
                             size=(self.component_width, self.component_height))
        sort_button = Button(text='Sort', size_hint=(None, None), background_color=self.button_color,
                             size=(self.component_width, self.component_height))

        button_layout = BoxLayout(size_hint=(None, None), height=self.component_height, spacing=10,
                                  pos_hint={'center_x': 0.48})
        sort_layout = BoxLayout(size_hint=(None, None), height=self.component_height, spacing=10,
                                pos_hint={'center_x': 0.39})
        spinner = Spinner(
            text='Pick sorting option',
            values=('Sort by price per day descending', 'Sort by price per day ascending', 'Sort by brand alphabetic',
                    'Sort by brand analphabetic'),
            size_hint=(None, None),
            size=(300, 44)
        )
        spinner.bind(text=self.on_spinner_text_changed)
        sort_layout.add_widget(spinner)
        sort_layout.add_widget(sort_button)

        button_layout.add_widget(back_button)

        self.filter_brand_input = TextInput(hint_text='Enter brand', multiline=False, size_hint=(None, None), width=200,
                                            height=self.component_height)
        self.filter_body_input = TextInput(hint_text='Enter body type', multiline=False, size_hint=(None, None),
                                           width=200, height=self.component_height)
        self.filter_seats_input = TextInput(hint_text='Enter number of seats', multiline=False, size_hint=(None, None),
                                            width=200, height=self.component_height)
        self.filter_price_input = TextInput(hint_text='Enter maximum price', multiline=False, size_hint=(None, None),
                                            width=200, height=self.component_height)

        # Przycisk filtru
        filter_button = Button(text='Filter', size_hint=(None, None), background_color=self.button_color,
                               size=(self.component_width, self.component_height))
        default_button = Button(text='Default list', size_hint=(None, None), background_color=self.button_color,
                               size=(self.component_width, self.component_height))
        filter_button.bind(on_press=self.filter_cars)
        default_button.bind(on_press=self.default)

        # Układ pól tekstowych
        filter_layout = BoxLayout(size_hint=(None, None), height=self.component_height, spacing=10,
                                  pos_hint={'center_x': 0.1})
        filter_layout.add_widget(self.filter_brand_input)
        filter_layout.add_widget(self.filter_body_input)
        filter_layout.add_widget(self.filter_seats_input)
        filter_layout.add_widget(self.filter_price_input)
        filter_layout.add_widget(filter_button)
        filter_layout.add_widget(default_button)

        main_layout = BoxLayout(orientation='vertical',
                                padding=[100, 30, 100, 30], spacing=10)

        main_layout.add_widget(filter_layout)

        main_layout.add_widget(scrollview)

        main_layout.add_widget(sort_layout)
        main_layout.add_widget(button_layout)

        self.add_widget(main_layout)

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
        self.org=self.cars
        self.create_layout()

    def go_back(self, instance):
        self.manager.current = 'login'

    def on_leave(self):
        Window.size = (800, 600)

    def car_details(self, car_id):
        self.manager.get_screen('car').set_car_id(car_id)
        self.manager.current = 'car'

    def on_spinner_text_changed(self, spinner, text):
        if text == 'Sort by price per day descending':
            self.sort_value = 0
        elif text == 'Sort by price per day ascending':
            self.sort_value = 1
        elif text == 'Sort by brand alphabetic':
            self.sort_value = 2
        elif text == 'Sort by brand analphabetic':
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
        # Pobieramy wartości wprowadzone przez użytkownika z pól tekstowych
        filter_body = self.filter_body_input.text.strip()
        filter_brand = self.filter_brand_input.text.strip()
        filter_seats = self.filter_seats_input.text.strip()
        filter_price = self.filter_price_input.text.strip()

        # Kopiujemy listę samochodów do przefiltrowania
        filtered = self.cars

        # Filtrujemy po rodzaju nadwozia
        if filter_body:
            filtered = list(filter(lambda car: contains_substring(car.body, filter_body), filtered))

        # Filtrujemy po marce
        if filter_brand:
            filtered = list(filter(lambda car: contains_substring(car.brand, filter_brand), filtered))

        # Filtrujemy po liczbie miejsc
        if filter_seats:
            try:
                seats = int(filter_seats)
                filtered = list(filter(lambda car: car.places == seats, filtered))
            except ValueError:
                pass  # Ignorujemy błędną wartość wprowadzoną przez użytkownika

        # Filtrujemy po maksymalnej cenie
        if filter_price:
            try:
                price = float(filter_price)
                filtered = list(filter(lambda car: car.price_per_day <= price, filtered))
            except ValueError:
                pass  # Ignorujemy błędną wartość wprowadzoną przez użytkownika

        # Ustawiamy przefiltrowaną listę samochodów
        self.cars = filtered

        # Odświeżamy widok
        self.create_layout()

    def default(self, instance):
        self.cars = self.org
        self.create_layout()


def contains_substring(main_string, substring):
    return substring.lower() in main_string.lower()

