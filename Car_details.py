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

class CarDetails(Screen):
    def __init__(self, **kwargs):
        super(CarDetails, self).__init__(**kwargs)
        self.car_id = None
        self.layout = BoxLayout(orientation='vertical')
        self.label = Label(text="Loading car details...")
        self.layout.add_widget(self.label)
        self.add_widget(self.layout)

    def on_pre_enter(self):
        if self.car_id:
            url = f'http://127.0.0.1:5000/car-details/{self.car_id}'
            response = requests.get(url)
            car_data = response.json()
            if 'error' not in car_data:
                self.label.text = (
                    f"Car Details:\n"
                    f"ID: {car_data['id']}\n"
                    f"Brand: {car_data['brand']}\n"
                    f"Model: {car_data['model']}\n"
                    f"Color: {car_data['color']}\n"
                    f"Price per Day: {car_data['price_per_day']}\n"
                    f"Body: {car_data['body']}\n"
                    f"Gearbox: {car_data['gearbox']}\n"
                    f"Seats: {car_data['places']}\n"
                    f"Year of Production: {car_data['year_of_production']}\n"
                    f"Horsepower: {car_data['horsepower']}\n"
                    f"Engine Type: {car_data['engine_type']}\n"
                    f"Max Velocity: {car_data['max_velocity']}\n"
                    f"Deposit: {car_data['deposit']}\n"
                    f"Last Rental End: {car_data['last_rental_end']}"
                )
            else:
                self.label.text = car_data['error']

    def set_car_id(self, car_id):
        self.car_id = car_id