import requests
from datetime import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.image import Image
import sys

sys.path.append('customclasses')
from Custom_button import CustomButton
from Custom_label import CustomLabel
from Custom_input import CustomTextInput

last_rental_beginning = datetime(2024, 4, 19)
last_rental_end = datetime(2024, 4, 21)
formatted_last_rental_end = last_rental_end.strftime('%Y-%m-%d %H:%M:%S')
formatted_last_rental_beginning = last_rental_beginning.strftime('%Y-%m-%d %H:%M:%S')


class ManagerScreen(Screen):
    def __init__(self, **kwargs):
        super(ManagerScreen, self).__init__(**kwargs)

        layout = GridLayout(cols=2, spacing=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        component_height = 50

        self.titles = ['Brand name:', 'Model:', 'Price per day:', 'Year of production:', 'Horsepower:', 'Engine type:',
                       'Body:',
                       'Color:', 'Max velocity:', 'Gearbox:', 'Seats no:', 'Deposit:', 'Photo URL:']
        self.text_inputs = {}

        for title in self.titles:
            layout.add_widget(CustomLabel(text=title))
            text_input = CustomTextInput()
            layout.add_widget(text_input)
            self.text_inputs[title] = text_input

        scroll_view = ScrollView(size_hint=(None, None), size=(500, 500), pos_hint={'center_x': 0.58})
        scroll_view.add_widget(layout)

        screen_layout = BoxLayout(orientation='vertical', spacing=10, pos_hint={'center_x': 0.51, 'center_y': 0.52})
        screen_layout.add_widget(scroll_view)

        button_layout = BoxLayout(size_hint=(None, None), height=component_height, spacing=10,
                                  pos_hint={'center_x': 0.33})

        back_button = CustomButton(text='Back')
        add_button = CustomButton(text='Add')

        button_layout.add_widget(back_button)
        button_layout.add_widget(add_button)

        screen_layout.add_widget(button_layout)

        self.add_widget(screen_layout)
        back_button.bind(on_press=self.go_back)
        add_button.bind(on_press=self.add_data)

    def add_data(self, instance):

        car_data = {
            'brand_name': self.text_inputs['Brand name:'].text,
            'status': 'free',
            'price_per_day': self.text_inputs['Price per day:'].text,
            'year_of_production': self.text_inputs['Year of production:'].text,
            'horsepower': self.text_inputs['Horsepower:'].text,
            'engine_type': self.text_inputs['Engine type:'].text,
            'body': self.text_inputs['Body:'].text,
            'color_name': self.text_inputs['Color:'].text,
            'max_velocity': self.text_inputs['Max velocity:'].text,
            'gearbox': self.text_inputs['Gearbox:'].text,
            'seats_no': self.text_inputs['Seats no:'].text,
            'deposit': self.text_inputs['Deposit:'].text,
            'last_rental_beginning': formatted_last_rental_beginning,
            'last_rental_end': formatted_last_rental_end,
            'place_id': 1,
            'photo': self.text_inputs['Photo URL:'].text,
            'model': self.text_inputs['Model:'].text
        }
        if all(text_input.text for text_input in self.text_inputs.values()):
            url = 'http://127.0.0.1:5000/cars'
            response = requests.post(url, json=car_data)
            response_json = response.json()
            message = list(response_json.keys())[0]
            if response.status_code == 200:
                self.show_popup('Success', message)
                self.clear_text_inputs()
            elif response.status_code == 400:
                self.show_popup('Error', 'Car data is invalid')
            else:
                self.show_popup('Error', 'Unknown error')
        else:
            self.show_popup('Error', 'Fill all the fields')

    def go_back(self, instance):
        self.manager.get_screen('user').set_staff_access(True)
        self.manager.current = 'user'

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()

    def clear_text_inputs(self):
        for text_input in self.text_inputs.values():
            text_input.text = ''