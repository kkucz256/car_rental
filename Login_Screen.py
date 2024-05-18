import requests
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from Manager import ManagerScreen
import hashlib


def sha256_hash(data):
    hasher = hashlib.sha256()
    hasher.update(data.encode() if isinstance(data, str) else data)
    return hasher.hexdigest()


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        label = Label(text='Welcome', size_hint=(None, None), size=(200, 50))
        login_button = Button(text='Log-in as user', size_hint=(None, None), size=(200, 50))
        login_staff_button = Button(text='Log-in as staff', size_hint=(None, None), size=(200, 50))
        register_button = Button(text='Register', size_hint=(None, None), size=(200, 50))

        layout = BoxLayout(orientation='vertical', spacing=10, size_hint=(None, None), size=(200, 200),
                           pos_hint={'center_x': 0.5, 'center_y': 0.5})
        layout.add_widget(label)
        layout.add_widget(login_button)
        layout.add_widget(login_staff_button)
        layout.add_widget(register_button)

        self.add_widget(layout)

        login_button.bind(on_press=self.switch_to_login_screen)
        login_staff_button.bind(on_press=self.switch_to_login_screen_staff)
        register_button.bind(on_press=self.switch_to_register_screen)

    def switch_to_login_screen(self, instance):
        self.manager.current = 'login'

    def switch_to_login_screen_staff(self, instance):
        self.manager.current = 'staff'

    def switch_to_register_screen(self, instance):
        self.manager.current = 'register'


class LoginScreen(Screen):
    def __init__(self, info, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.orientation = 'vertical'

        info_label = Label(text='', size_hint=(None, None), size=(200, 50))

        if info == 'staff':
            info2_label = Label(text='You are trying to login as staff', size_hint=(None, None), size=(200, 50))
        else:
            info2_label = Label(text='You are trying to login as user', size_hint=(None, None), size=(200, 50))

        username = Label(text='E-mail:', size_hint=(None, None), size=(200, 50))

        self.username_text = TextInput(multiline=False, size_hint=(None, None), width=200, height=30)
        password = Label(text='Password:', size_hint=(None, None), size=(200, 50))
        self.password_text = TextInput(multiline=False, size_hint=(None, None), width=200, height=30, password=True)

        back_button = Button(text='Back', size_hint=(None, None), size=(200, 50))
        login_button = Button(text='Login', size_hint=(None, None), size=(200, 50))
        layout = BoxLayout(orientation='vertical', spacing=10, size_hint=(None, None), size=(200, 200),
                           pos_hint={'center_x': 0.5, 'center_y': 0.4})

        layout.add_widget(info_label)
        layout.add_widget(info2_label)
        layout.add_widget(username)
        layout.add_widget(self.username_text)
        layout.add_widget(password)
        layout.add_widget(self.password_text)
        layout.add_widget(login_button)
        layout.add_widget(back_button)

        self.add_widget(layout)

        back_button.bind(on_press=self.switch_to_main_screen)

        if info == 'staff':
            login_button.bind(on_press=self.manager_access)
        else:
            login_button.bind(on_press=self.user_access)

    def manager_access(self, instance):
        login_credentials = {
            'email': self.username_text.text,
            'password': sha256_hash(self.password_text.text)
        }
        url = 'http://127.0.0.1:5000/log-in_staff'
        response = requests.get(url, json=login_credentials)
        message = list(response_json.keys())[0]
        if response.status_code == 200:
            self.manager.current = 'manager'
        elif response.status_code == 400:
            self.show_popup("Error", message)
        elif response.status_code == 300:
            self.show_popup("Error", message)

    def user_access(self, instance):
        login_credentials = {
            'email': self.username_text.text,
            'password': sha256_hash(self.password_text.text)
        }
        url = 'http://127.0.0.1:5000/log-in'
        response = requests.get(url, json=login_credentials)
        response_json = response.json()
        message = list(response_json.keys())[0]
        if response.status_code == 200:
            self.manager.current = 'manager'
        elif response.status_code == 400:
            self.show_popup("Error", message)
        elif response.status_code == 300:
            self.show_popup("Error", message)

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()

    def switch_to_main_screen(self, instance):
        self.manager.current = 'main'


class RegisterScreen(Screen):
    def __init__(self, **kwargs):
        super(RegisterScreen, self).__init__(**kwargs)
        component_width = 200
        component_height = 50
        input_height = 30

        self.labels = ['E-mail:', 'Phone number:', 'Date of birth (YYYY/MM/DD):', 'First name:', 'Last name:', 'City:',
                       'Country:',
                       'Postal code:', 'Addr1:', 'Addr2:', 'Password:', 'Repeat Password:']
        self.text_inputs = {}
        layout = GridLayout(cols=2, spacing=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        for label_text in self.labels:
            layout.add_widget(Label(text=label_text, size_hint_y=None, height=component_height))
            if label_text == 'Password:' or label_text == 'Repeat Password:':
                text_input = TextInput(multiline=False, size_hint_y=None, height=input_height, password=True)
            else:
                text_input = TextInput(multiline=False, size_hint_y=None, height=input_height)
            layout.add_widget(text_input)
            self.text_inputs[label_text] = text_input

        scroll_view = ScrollView(size_hint=(0.8, None), size=(600, 500), pos_hint={'center_x': 0.47})
        scroll_view.add_widget(layout)

        screen_layout = BoxLayout(orientation='vertical', spacing=10)
        screen_layout.add_widget(scroll_view)

        button_layout = BoxLayout(size_hint=(None, None), height=component_height, spacing=10,
                                  pos_hint={'center_x': 0.3})
        back_button = Button(text='Back', size_hint=(None, None), size=(component_width, component_height))
        register_button = Button(text='Register', size_hint=(None, None), size=(component_width, component_height))
        button_layout.add_widget(back_button)
        button_layout.add_widget(register_button)

        screen_layout.add_widget(button_layout)
        self.add_widget(screen_layout)

        back_button.bind(on_press=self.switch_to_main_screen)
        register_button.bind(on_press=self.user_register)

    def user_register(self, instance):

        address = {
            'address_1': self.text_inputs['Addr1:'].text,
            'address_2': self.text_inputs['Addr2:'].text,
            'city': self.text_inputs['City:'].text,
            'country': self.text_inputs['Country:'].text,
            'post_code': self.text_inputs['Postal code:'].text
        }

        login_credentials = {
            'email': self.text_inputs['E-mail:'].text,
            'password': sha256_hash(self.text_inputs['Password:'].text),
            'date_of_birth': self.text_inputs['Date of birth (YYYY/MM/DD):'].text,
            'phone_number': self.text_inputs['Phone number:'].text,
            'first_name': self.text_inputs['First name:'].text,
            'last_name': self.text_inputs['Last name:'].text,
            'address': address
        }

        if all(text_input.text for text_input in self.text_inputs.values()):
            if self.text_inputs['Password:'].text == self.text_inputs['Repeat Password:'].text:
                url = 'http://127.0.0.1:5000/register'
                response = requests.post(url, json=login_credentials)
                if response.status_code == 200:
                    response_json = response.json()
                    success_message = list(response_json.keys())[0]
                    self.show_popup('Success', success_message)
                elif response.status_code == 400:
                    self.show_popup("Error", f"Something went wrong Mr./Mrs. {self.text_inputs['Last name:'].text}")
            else:
                self.show_popup("Error", "Passwords do not match")
        else:
            self.show_popup("Error", "Please fill in all the fields")

    def switch_to_main_screen(self, instance):
        self.manager.current = 'main'

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()
