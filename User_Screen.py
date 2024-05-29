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

import hashlib

class UserScreen(Screen):


    def __init__(self, **kwargs):

        self.cars=[]

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
        button_layout = BoxLayout(size_hint=(None, None), height=self.component_height, spacing=10,
                                  pos_hint={'center_x': 0.5})
        button_layout.add_widget(back_button)

        main_layout = BoxLayout(orientation='vertical',
                                padding=[100, 30, 100, 30])
        main_layout.add_widget(scrollview)

        self.add_widget(main_layout)
        self.add_widget(button_layout)

        back_button.bind(on_press=self.go_back)



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
        self.create_layout()



    def go_back(self, instance):
        self.manager.current = 'login'


    def on_leave(self):
        Window.size = (800, 600)

    def car_details(self, car_id):
        self.manager.get_screen('car').set_car_id(car_id)
        self.manager.current = 'car'