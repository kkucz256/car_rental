from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
import requests
from Car_details_class import Car_details_class


class CarDetails(Screen):
    def __init__(self, **kwargs):
        super(CarDetails, self).__init__(**kwargs)
        self.car_id = None
        self.car = Car_details_class()
        self.details_dict = {}

        self.button_color = (34 / 255, 40 / 255, 49 / 255, 1)
        self.component_width = 200
        self.component_height = 50

        self.layout = GridLayout(cols=2)
        self.add_widget(self.layout)

    def on_pre_enter(self):
        self.layout.clear_widgets()
        if self.car_id:
            url = f'http://127.0.0.1:5000/car-details/{self.car_id}'
            response = requests.get(url)
            car_data = response.json()
            if 'error' not in car_data:
                self.car = Car_details_class(
                    car_data['id'], car_data['brand'], car_data['status'], car_data['price_per_day'],
                    car_data['year_of_production'], car_data['horsepower'], car_data['engine_type'],
                    car_data['body'], car_data['color'], car_data['max_velocity'], car_data['gearbox'],
                    car_data['seats_no'], car_data['deposit'], car_data['last_rental_end'], car_data['model']
                )
                self.details_dict = {
                    "Body ": self.car.body,
                    "Gearbox ": self.car.gearbox,
                    "Number of seats ": self.car.seats_no,
                    "Year of profuction ": self.car.year_of_production,
                    "Horsepower ": self.car.horsepower}
                self.update_layout()
            else:
                self.layout.add_widget(Label(text=car_data['error']))

    def set_car_id(self, car_id):
        self.car_id = car_id

    def update_layout(self):
        # Tutaj wstawić zdj jak będzie działać
        self.layout.add_widget(Label())

        upper_right_layout = GridLayout(cols=1)
        main_info_label = Label(
            text=f"{self.car.color} {self.car.brand} {self.car.model}",
            font_size=30,
            size_hint_y=None,
            height=150,
            valign='bottom'
        )
        status_label = Label(text=self.status_text(), size_hint_y=None, height=50)
        price_deposit_label = Label(
            text=f"Price per Day: ${self.car.price_per_day} Deposit: ${self.car.deposit}",
            size_hint_y=None,
            height=100
        )
        upper_right_layout.add_widget(main_info_label)
        upper_right_layout.add_widget(status_label)
        upper_right_layout.add_widget(price_deposit_label)
        self.layout.add_widget(upper_right_layout)

        details_layout = GridLayout(cols=2)
        details_label_1 = Label(text='Details:', font_size=20, size_hint_y=None, height=50)
        details_labels_scrollview = ScrollView(size_hint_y=None, height=250)
        details_labels_layout = GridLayout(cols=1, size_hint_y=None)
        details_labels_layout.bind(minimum_height=details_labels_layout.setter('height'))
        details_labels_layout.add_widget(details_label_1)
        for detail_key, detail_value in self.details_dict.items():
            details_labels_layout.add_widget(Label(text=f"{detail_key}: {detail_value}", size_hint_y=None, height=30))
        details_labels_scrollview.add_widget(details_labels_layout)
        details_layout.add_widget(details_labels_scrollview)
        self.layout.add_widget(details_layout)

        buttons_layout = GridLayout(cols=2, size_hint_y=None, height=50)
        buttons_layout.add_widget(Button(text='Back', on_press=self.go_back))
        buttons_layout.add_widget(Button(text='Buy'))
        self.add_widget(buttons_layout)

    def go_back(self, instance):
        self.manager.current = 'user'

    def status_text(self):
        if self.car.status == 'free':
            return "The car is currently available"
        if self.car.status == 'booked':
            return f"The car is currently taken, it will be available on: {self.car.last_rental_end}"
