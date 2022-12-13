import os
import sys
import certifi
from kivy.lang.builder import Builder
from kivy.metrics import dp
from kivy.uix.image import AsyncImage
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy import platform
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.button import MDRectangleFlatIconButton, RectangularElevationBehavior
from kivymd.uix.snackbar import Snackbar
from kivyauth.google_auth import initialize_google, login_google, logout_google
from kivyauth.utils import stop_login
from kivyauth.utils import login_providers, auto_login

GOOGLE_CLIENT_ID = (
    "161589307268-3mk3igf1d0qh4rk03ldfm0u68g038h6t.apps.googleusercontent.com"
)
GOOGLE_CLIENT_SECRET = "secret"


class SimylrApp(App):
    current_provider = ""

    def build(self):
        initialize_google(
            self.after_login,
            self.error_listener,
            GOOGLE_CLIENT_ID,
            GOOGLE_CLIENT_SECRET,
        )
        if platform == "android":
            NewRelic.withApplicationToken(
                "eu01xx3a293465cda73cd2f5b1154ed969b9af4b27-NRMA"
            ).start(context.getApplication())

        # set_statusbar_color()
        tmp = Builder.load_string(kv)
        if platform != "android":
            from kivymd.uix.dialog import MDDialog
            from kivymd.uix.button import MDFlatButton

            btn = MDFlatButton(text="CANCEL", text_color=self.theme_cls.primary_color)
            btn.bind(on_release=lambda *args: (stop_login(), self.dialog.dismiss()))
            self.dialog = MDDialog(
                title="",
                size_hint_x=None,
                size_hint_y=None,
                width="250dp",
                type="custom",
                auto_dismiss=False,
                content_cls=Content(),
                buttons=[btn],
            )
        return tmp

    def on_start(self):
        if platform == "android":
            if auto_login(login_providers.google):
                self.current_provider = login_providers.google
            elif auto_login(login_providers.facebook):
                self.current_provider = login_providers.facebook
            elif auto_login(login_providers.github):
                self.current_provider = login_providers.github
            elif auto_login(login_providers.twitter):
                self.current_provider = login_providers.twitter
        primary_clr= [ 108/255, 52/255, 131/255 ]
        hex_color= '#%02x%02x%02x' % (int(primary_clr[0]*200), int(primary_clr[1]*200), int(primary_clr[2]*200))
        set_statusbar_color()

    
    def show_login_progress(self):
        if platform != "android":
            self.dialog.open()

    def hide_login_progress(self):
        if platform != "android":
            self.dialog.dismiss()

    def gl_login(self, *args):
        login_google()
        self.current_provider = login_providers.google

    def logout_(self):
        if self.current_provider == login_providers.google:
            logout_google(self.after_logout)

    def after_login(self, name, email, photo_uri):
        self.hide_login_progress()

        if platform == "android":
            show_toast("Logged in using {}".format(self.current_provider))
        else:
            Snackbar(text="Logged in using {}".format(self.current_provider)).show()

        self.root.current = "homescreen"
        self.update_ui(name, email, photo_uri)

    def after_logout(self):
        self.update_ui("", "", "")
        self.root.current = "loginscreen"
        if platform == "android":
            show_toast(text="Logged out from {} login".format(self.current_provider))
        else:
            Snackbar(
                text="Logged out from {} login".format(self.current_provider)
            ).show()

    def update_ui(self, name, email, photo_uri):
        self.root.ids.home_screen.ids.user_photo.add_widget(
            AsyncImage(
                source=photo_uri, size_hint=(None, None), height=dp(60), width=dp(60)
            )
        )
        self.root.ids.home_screen.ids.user_name.title = "Welcome, {}".format(name)
        self.root.ids.home_screen.ids.user_email.text = (
            "Your Email: {}".format(email)
            if email
            else "Your Email: Could not fetch email"
        )

    def error_listener(self):
        if platform == "android":
            show_toast("Error logging in.")
        else:
            Snackbar(text="Error logging in. Check connection or try again.").show()
        Clock.schedule_once(lambda *args: self.hide_login_progress())

if __name__ == "__main__":
    SimylrApp().run()