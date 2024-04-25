from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from Manager import ManagerScreen


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        label = Label(text='Welcome', size_hint=(None, None), size=(200, 50))
        login_button = Button(text='Log-in', size_hint=(None, None), size=(200, 50))
        register_button = Button(text='Register', size_hint=(None, None), size=(200, 50))

        layout = BoxLayout(orientation='vertical', spacing=10, size_hint=(None, None), size=(200, 200),
                           pos_hint={'center_x': 0.5, 'center_y': 0.5})
        layout.add_widget(label)
        layout.add_widget(login_button)
        layout.add_widget(register_button)

        self.add_widget(layout)

        login_button.bind(on_press=self.switch_to_login_screen)
        register_button.bind(on_press=self.switch_to_register_screen)

    def switch_to_login_screen(self, instance):
        self.manager.current = 'login'

    def switch_to_register_screen(self, instance):
        self.manager.current = 'register'


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.orientation = 'vertical'
        info_label = Label(text='', size_hint=(None, None), size=(200, 50))
        username = Label(text='E-mail:', size_hint=(None, None), size=(200, 50))
        username_text = TextInput(multiline=False, size_hint=(None, None), width=200, height=30)
        password = Label(text='Password:', size_hint=(None, None), size=(200, 50))
        password_text = TextInput(multiline=False, size_hint=(None, None), width=200, height=30)

        back_button = Button(text='Back', size_hint=(None, None), size=(200, 50))
        login_button = Button(text='Login', size_hint=(None, None), size=(200, 50))
        layout = BoxLayout(orientation='vertical', spacing=10, size_hint=(None, None), size=(200, 200),
                           pos_hint={'center_x': 0.5, 'center_y': 0.5})

        layout.add_widget(info_label)
        layout.add_widget(username)
        layout.add_widget(username_text)
        layout.add_widget(password)
        layout.add_widget(password_text)
        layout.add_widget(login_button)
        layout.add_widget(back_button)

        self.add_widget(layout)
        back_button.bind(on_press=self.switch_to_main_screen)
        login_button.bind(on_press=self.manager_access)

    def switch_to_main_screen(self, instance):
        self.manager.current = 'main'

    def manager_access(self, instance):
        self.manager.current = 'manager'


class RegisterScreen(Screen):
    def __init__(self, **kwargs):
        super(RegisterScreen, self).__init__(**kwargs)
        self.orientation = 'vertical'
        info_label = Label(text='', size_hint=(None, None), size=(200, 50))
        username = Label(text='E-mail:', size_hint=(None, None), size=(200, 50))
        username_text = TextInput(multiline=False, size_hint=(None, None), width=200, height=30)
        password = Label(text='Password:', size_hint=(None, None), size=(200, 50))
        password_text = TextInput(multiline=False, size_hint=(None, None), width=200, height=30)
        password2 = Label(text='Repeat Password:', size_hint=(None, None), size=(200, 50))
        password_text2 = TextInput(multiline=False, size_hint=(None, None), width=200, height=30)

        back_button = Button(text='Back', size_hint=(None, None), size=(200, 50))
        register_button = Button(text='Register', size_hint=(None, None), size=(200, 50))
        layout = BoxLayout(orientation='vertical', spacing=10, size_hint=(None, None), size=(200, 200),
                           pos_hint={'center_x': 0.5, 'center_y': 0.5})

        layout.add_widget(info_label)
        layout.add_widget(username)
        layout.add_widget(username_text)
        layout.add_widget(password)
        layout.add_widget(password_text)
        layout.add_widget(password2)
        layout.add_widget(password_text2)
        layout.add_widget(register_button)
        layout.add_widget(back_button)

        self.add_widget(layout)
        back_button.bind(on_press=self.switch_to_main_screen)
        register_button.bind(on_press=self.register)

    def register(self, instance):
        pass

    def switch_to_main_screen(self, instance):
        self.manager.current = 'main'






