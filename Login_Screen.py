import requests
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
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
    def __init__(self,info, **kwargs):
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
        self.password_text = TextInput(multiline=False, size_hint=(None, None), width=200, height=30,password=True)

        back_button = Button(text='Back', size_hint=(None, None), size=(200, 50))
        login_button = Button(text='Login', size_hint=(None, None), size=(200, 50))
        layout = BoxLayout(orientation='vertical', spacing=10, size_hint=(None, None), size=(200, 200),
                           pos_hint={'center_x': 0.5, 'center_y': 0.5})

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
        login_button.bind(on_press=self.manager_access)

    def switch_to_main_screen(self, instance):
        self.manager.current = 'main'

    def manager_access(self, instance):
        login_credentials = {
            'email': self.username_text.text,
            'password': sha256_hash(self.password_text.text)
        }
        url = 'http://127.0.0.1:5000/log-in'
        response = requests.get(url, json=login_credentials)
        if response.status_code == 200:
            self.manager.current = 'manager'
        elif response.status_code == 400:
            print(f"No such user {self.username_text.text}")
        elif response.status_code ==300:
            print("Wrong password")






class RegisterScreen(Screen):
    def __init__(self, **kwargs):
        super(RegisterScreen, self).__init__(**kwargs)
        self.orientation = 'vertical'
        info_label = Label(text='', size_hint=(None, None), size=(200, 50))
        username = Label(text='E-mail:', size_hint=(None, None), size=(200, 50))
        self.username_text = TextInput(multiline=False, size_hint=(None, None), width=200, height=30)
        password = Label(text='Password:', size_hint=(None, None), size=(200, 50))
        self.password_text = TextInput(multiline=False, size_hint=(None, None), width=200, height=30)
        password2 = Label(text='Repeat Password:', size_hint=(None, None), size=(200, 50))
        self.password_text2 = TextInput(multiline=False, size_hint=(None, None), width=200, height=30)
        back_button = Button(text='Back', size_hint=(None, None), size=(200, 50))
        register_button = Button(text='Register', size_hint=(None, None), size=(200, 50))
        layout = BoxLayout(orientation='vertical', spacing=10, size_hint=(None, None), size=(200, 200),
                           pos_hint={'center_x': 0.5, 'center_y': 0.5})

        layout.add_widget(info_label)
        layout.add_widget(username)
        layout.add_widget(self.username_text)
        layout.add_widget(password)
        layout.add_widget(self.password_text)
        layout.add_widget(password2)
        layout.add_widget(self.password_text2)
        layout.add_widget(register_button)
        layout.add_widget(back_button)

        self.add_widget(layout)
        back_button.bind(on_press=self.switch_to_main_screen)
        register_button.bind(on_press=self.register)

    def register(self, instance):
        pass

    def switch_to_main_screen(self, instance):
        self.manager.current = 'main'
