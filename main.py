import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Rectangle
from kivy.config import Config
from datetime import datetime
import pyrebase

Config.set('kivy', 'keyboard_mode', 'systemandmulti')

# Firebase configuration
firebase_config = {
    "apiKey": "AIzaSyA74r4K7nAxWTckZQC2m7yUuKRC1hhvaeM",
    "authDomain": "simylr-ff5f6.firebaseapp.com",
    "databaseURL": "https://simylr-ff5f6-default-rtdb.firebaseio.com",
    "projectId": "simylr-ff5f6",
    "storageBucket": "simylr-ff5f6.appspot.com",
    "messagingSenderId": "1085868492181",
    "appId": "1:1085868492181:web:766648122aaeca29d4e29c",
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
database = firebase.database()


class SignupScreen(Screen):
    def __init__(self, **kwargs):
        super(SignupScreen, self).__init__(**kwargs)
        self.layout = FloatLayout()
        self.add_widget(self.layout)

        # Set background color
        self.layout.canvas.before.clear()
        with self.layout.canvas.before:
            Color(0, 0.71, 0.92, 1)  # #00b7eb in RGBA
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        # Add signup screen UI elements here
        # e.g., email input, password input, confirm password input, signup button, back button

        title_label = Label(text="Sign Up", font_size=24, bold=True, pos_hint={'center_x': 0.5, 'center_y': 0.8},
                            size_hint=(0.8, 0.1), halign='center')
        self.layout.add_widget(title_label)

        self.email_input = TextInput(pos_hint={'center_x': 0.5, 'center_y': 0.6}, size_hint=(0.6, 0.08),
                                     hint_text="Email", hint_text_color=(0.5, 0.5, 0.5, 1), foreground_color=(0, 0, 0, 1),
                                     cursor_color=(0, 0, 0, 1), write_tab=False, multiline=False)
        self.email_input.bind(focus=self.clear_placeholder)
        self.layout.add_widget(self.email_input)

        self.password_input = TextInput(pos_hint={'center_x': 0.5, 'center_y': 0.5}, size_hint=(0.6, 0.08),
                                        hint_text="Password", hint_text_color=(0.5, 0.5, 0.5, 1),
                                        foreground_color=(0, 0, 0, 1), cursor_color=(0, 0, 0, 1), password=True,
                                        write_tab=False, multiline=False)
        self.password_input.bind(focus=self.clear_placeholder)
        self.layout.add_widget(self.password_input)

        self.confirm_password_input = TextInput(pos_hint={'center_x': 0.5, 'center_y': 0.4}, size_hint=(0.6, 0.08),
                                                hint_text="Confirm Password", hint_text_color=(0.5, 0.5, 0.5, 1),
                                                foreground_color=(0, 0, 0, 1), cursor_color=(0, 0, 0, 1), password=True,
                                                write_tab=False, multiline=False)
        self.confirm_password_input.bind(focus=self.clear_placeholder)
        self.layout.add_widget(self.confirm_password_input)

        signup_button = Button(text="Sign Up", pos_hint={'center_x': 0.5, 'center_y': 0.3}, size_hint=(0.3, 0.1))
        signup_button.bind(on_release=self.signup)
        self.layout.add_widget(signup_button)

        back_button = Button(text="Back", pos_hint={'center_x': 0.5, 'center_y': 0.2}, size_hint=(0.3, 0.1))
        back_button.bind(on_release=self.back)
        self.layout.add_widget(back_button)

    def clear_placeholder(self, instance, value):
        if value:
            instance.text = ""

    def signup(self, instance):
        email = self.email_input.text
        password = self.password_input.text
        confirm_password = self.confirm_password_input.text

        if password == confirm_password:
            try:
                user = auth.create_user_with_email_and_password(email, password)
                # Account creation successful, switch to the login screen
                self.manager.current = 'login'
            except:
                # Show error message
                error_popup = Popup(title='Error', content=Label(text='Failed to create an account.'),
                                    size_hint=(None, None), size=(200, 200))
                error_popup.open()
        else:
            # Show error message for password confirmation
            error_popup = Popup(title='Error', content=Label(text='Passwords do not match.'),
                                size_hint=(None, None), size=(200, 200))
            error_popup.open()

    def back(self, instance):
        self.manager.current = 'login'

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.layout = FloatLayout()
        self.add_widget(self.layout)

        # Set background color
        self.layout.canvas.before.clear()
        with self.layout.canvas.before:
            Color(0, 0.71, 0.92, 1)  # #00b7eb in RGBA
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        # Add login screen UI elements here
        # e.g., email input, password input, login button, signup button, error label

        title_label = Label(text="Sign In", font_size=24, bold=True, pos_hint={'center_x': 0.5, 'center_y': 0.8},
                            size_hint=(0.8, 0.1), halign='center')
        self.layout.add_widget(title_label)

        self.email_input = TextInput(pos_hint={'center_x': 0.5, 'center_y': 0.6}, size_hint=(0.6, 0.08),
                                     hint_text="Email", hint_text_color=(0.5, 0.5, 0.5, 1), foreground_color=(0, 0, 0, 1),
                                     cursor_color=(0, 0, 0, 1), write_tab=False, multiline=False)
        self.email_input.bind(focus=self.clear_placeholder)
        self.layout.add_widget(self.email_input)

        self.password_input = TextInput(pos_hint={'center_x': 0.5, 'center_y': 0.5}, size_hint=(0.6, 0.08),
                                        hint_text="Password", hint_text_color=(0.5, 0.5, 0.5, 1),
                                        foreground_color=(0, 0, 0, 1), cursor_color=(0, 0, 0, 1), password=True,
                                        write_tab=False, multiline=False)
        self.password_input.bind(focus=self.clear_placeholder)
        self.layout.add_widget(self.password_input)

        login_button = Button(text="Login", pos_hint={'center_x': 0.5, 'center_y': 0.4}, size_hint=(0.3, 0.1))
        login_button.bind(on_release=self.login)
        self.layout.add_widget(login_button)

        signup_button = Button(text="Sign Up", pos_hint={'center_x': 0.5, 'center_y': 0.3}, size_hint=(0.3, 0.1))
        signup_button.bind(on_release=self.signup)
        self.layout.add_widget(signup_button)

    def clear_placeholder(self, instance, value):
        if value:
            instance.text = ""

    def login(self, instance):
        email = self.email_input.text
        password = self.password_input.text

        try:
            user = auth.sign_in_with_email_and_password(email, password)
            # If login successful, switch to the home screen
            self.manager.current = 'home'
        except:
            # Show error message
            error_popup = Popup(title='Error', content=Label(text='Invalid email or password.'), size_hint=(None, None),
                                size=(200, 200))
            error_popup.open()

    def signup(self, instance):
        self.manager.current = 'signup'

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.add_widget(self.layout)

        # Set background color
        self.layout.canvas.before.clear()
        with self.layout.canvas.before:
            Color(0, 0.71, 0.92, 1)  # #00b7eb in RGBA
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        # Add home screen UI elements here
        # e.g., take picture button, prompt label

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class PhotoshopScreen(Screen):
    def __init__(self, **kwargs):
        super(PhotoshopScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.add_widget(self.layout)

        # Set background color
        self.layout.canvas.before.clear()
        with self.layout.canvas.before:
            Color(0, 0.71, 0.92, 1)  # #00b7eb in RGBA
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        # Add Photoshop screen UI elements here
        # e.g., display prompt, image editing tools

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class RatingScreen(Screen):
    def __init__(self, **kwargs):
        super(RatingScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.add_widget(self.layout)

        # Set background color
        self.layout.canvas.before.clear()
        with self.layout.canvas.before:
            Color(0, 0.71, 0.92, 1)  # #00b7eb in RGBA
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        # Add rating screen UI elements here
        # e.g., display image, rating buttons, submit button

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class ProfileScreen(Screen):
    def __init__(self, **kwargs):
        super(ProfileScreen, self).__init__(**kwargs)
        self.layout = FloatLayout()
        self.add_widget(self.layout)

        # Set background color
        self.layout.canvas.before.clear()
        with self.layout.canvas.before:
            Color(0, 0.71, 0.92, 1)  # #00b7eb in RGBA
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        # Add profile screen UI elements here
        # e.g., profile picture, badges display

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        self.layout = FloatLayout()
        self.add_widget(self.layout)

        # Set background color
        self.layout.canvas.before.clear()
        with self.layout.canvas.before:
            Color(0, 0.71, 0.92, 1)  # #00b7eb in RGBA
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        # Add settings screen UI elements here
        # e.g., settings options, logout button

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class FriendsScreen(Screen):
    def __init__(self, **kwargs):
        super(FriendsScreen, self).__init__(**kwargs)
        self.layout = FloatLayout()
        self.add_widget(self.layout)

        # Set background color
        self.layout.canvas.before.clear()
        with self.layout.canvas.before:
            Color(0, 0.71, 0.92, 1)  # #00b7eb in RGBA
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        # Add friends screen UI elements here
        # e.g., friend list, ratings, etc.

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class MainApp(App):
    def build(self):
        sm = ScreenManager()

        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(SignupScreen(name='signup'))
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(PhotoshopScreen(name='photoshop'))
        sm.add_widget(RatingScreen(name='rating'))
        sm.add_widget(ProfileScreen(name='profile'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(FriendsScreen(name='friends'))

        return sm


if __name__ == '__main__':
    MainApp().run()