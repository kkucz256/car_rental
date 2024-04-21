import requests
import json
from datetime import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

last_rental_beginning = datetime(2024, 4, 19)
last_rental_end = datetime(2024, 4, 21)
formatted_last_rental_end = last_rental_end.strftime('%Y-%m-%d %H:%M:%S')
formatted_last_rental_beginning = last_rental_beginning.strftime('%Y-%m-%d %H:%M:%S')


class CarReservationApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10, size_hint=(None, None), width=400,
                           height=400)

        titles = ['Price per day:', 'Year:', 'Horsepower:', 'Max velocity:', 'Seats no:']

        self.text_inputs = []
        for title in titles:
            title_label = Label(text=title, size_hint_x=None, width=100, halign='right', pos_hint={'center_x': 0.5})
            layout.add_widget(title_label)

            text_input = TextInput(multiline=False, size_hint=(None, None), width=200, height=30,
                                   pos_hint={'center_x': 0.5})
            layout.add_widget(text_input)
            self.text_inputs.append(text_input)

        add_button = Button(text='Add', size_hint=(None, None), width=200, height=30, pos_hint={'center_x': 0.5})
        layout.add_widget(add_button)

        add_button.bind(on_press=self.extract_data)

        layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        return layout

    def extract_data(self, instance):
        price = self.text_inputs[0].text
        year = self.text_inputs[1].text
        hpw = self.text_inputs[2].text
        velocity = self.text_inputs[3].text
        seats = self.text_inputs[4].text

        car_data = {
            'brand_id': 1,
            'status': 'free',
            'price_per_day': price,
            'year_of_production': year,
            'horsepower': hpw,
            'engine_type': 'diesel',
            'body': 'wagon',
            'color_id': 1,
            'max_velocity': velocity,
            'gearbox': 'manual',
            'seats_no': seats,
            'deposit': 1000,
            'last_rental_beginning': formatted_last_rental_beginning,
            'last_rental_end': formatted_last_rental_end,
            'place_id': 1,
            'photo': "https://i.imgur.com"
        }

        url = 'http://127.0.0.1:5000/cars'
        response = requests.post(url, json=car_data)
        if response.status_code == 200:
            print(response.content.decode('utf-8'))
        elif response.status_code == 400:
            print("Bad request! Car data is invalid.")
        else:
            print(f"An error occurred! Status code: {response.status_code}")


if __name__ == '__main__':
    CarReservationApp().run()
