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
from datetime import datetime, timedelta
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
        self.layout.pos_hint = {'center_x': 0.87, 'center_y': 0.65}

        self.add_widget(self.layout)

    def update_layout(self):
        self.img = Image(source="images/logo.png")
        self.img.size = (300, 300)
        self.img.size_hint = (None, None)
        self.img.pos_hint = {'center_x': 0.5, 'center_y': 0.83}

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

        enum_response = requests.get('http://127.0.0.1:5000/get-enum-values/payment_type')
        if enum_response.status_code == 200:
            payment_types = enum_response.json()['values']
        else:
            payment_types = ['Card', 'BLIK', 'Cash']

        self.payment_spinner = Spinner(
            text='Select Payment Method',
            values=payment_types,
            size_hint=(None, None),
            size=(200, 44)
        )

        buy_button = CustomButton(text="Buy")
        buy_button.bind(on_press=self.create_booking)

        back_button = CustomButton(text="Back")
        back_button.bind(on_press=self.go_back)

        self.layout.add_widget(label)
        self.layout.add_widget(info_label)
        self.layout.add_widget(self.date_input)
        self.layout.add_widget(self.payment_spinner)
        self.layout.add_widget(buy_button)
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

    def create_booking(self, instance):
        rental_beginning = self.date_input.text
        try:
            rental_beginning_date = datetime.strptime(rental_beginning, '%Y-%m-%d')
        except ValueError:
            popup = Popup(title='Error', content=Label(text='Invalid date format. Please use YYYY-MM-DD.'),
                          size_hint=(None, None), size=(400, 200))
            popup.open()
            return

        if rental_beginning_date < datetime.today():
            popup = Popup(title='Error', content=Label(text='You cannot book a car for a past date.'),
                          size_hint=(None, None), size=(400, 200))
            popup.open()
            return

        if self.payment_spinner.text == "Select Payment Method":
            popup = Popup(title='Error', content=Label(text='You must select payment method.'),
                          size_hint=(None, None), size=(400, 200))
            popup.open()
            return

        rental_beginning_formatted = self.format_rental_beginning(rental_beginning)
        rental_end = self.calculate_rental_end(rental_beginning, self.days)
        payment_type = self.payment_spinner.text
        payment_amount = self.price

        booking_data = {
            'customer_id': self.user_id,
            'car_id': self.car_id,
            'rental_days': self.days,
            'rental_beginning': rental_beginning_formatted,
            'rental_end': rental_end,
            'payment_type': payment_type,
            'payment_amount': payment_amount
        }

        try:
            response = requests.post('http://127.0.0.1:5000/create-booking', json=booking_data)
            response.raise_for_status()
            if response.status_code == 200:
                booking_id = response.json().get('booking_id')
                popup = Popup(title='Success',
                              content=Label(text=f'Booking created successfully!\nBooking ID: {booking_id}'),
                              size_hint=(None, None), size=(400, 200))
                popup.open()
            elif response.status_code == 201:
                try:
                    response_json = response.json()
                    message = f'Car is already booked from:\n {response_json["start_date"]}to: \n{response_json["end_date"]}'
                except json.JSONDecodeError:
                    message = 'Car is already booked for the specified dates.'

                popup = Popup(title='Error', content=Label(text=message),
                              size_hint=(None, None), size=(400, 200))
                popup.open()
        except requests.exceptions.RequestException as e:
            popup = Popup(title='Error', content=Label(text=f'Failed to create booking. Error: {str(e)}'),
                          size_hint=(None, None), size=(400, 200))
            popup.open()

    def format_rental_beginning(self, rental_beginning):
        return f"{rental_beginning} 00:00:00.000000"

    def calculate_rental_end(self, start_date, rental_days):
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
        rental_end_obj = start_date_obj + timedelta(days=rental_days)
        rental_end = rental_end_obj.strftime("%Y-%m-%d 00:00:00.000000")
        return rental_end