from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen,SlideTransition
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from subcription_view.subscForm import HomeScreen
from scan_view.scan_view import QRCodeScannerScreen
from kivy.lang.builder import Builder


Builder.load_file("subcription_view/homescreen.kv")




class ScreenThree(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text="Welcome to Screen 3"))


class PowerPlanner(App):
    def build(self):

        self.sm = ScreenManager(transition=SlideTransition())
        self.sm.add_widget(HomeScreen(name="HomeScreen"))
        self.sm.add_widget(QRCodeScannerScreen(name="QR_code Screen"))
        self.sm.add_widget(ScreenThree(name="screen3"))


        self.dropdown = DropDown()
        screens = [("Subscription Form", "HomeScreen"), ("QR_code Screen", "QR_code Screen"), ("Screen 3", "screen3")]

        self.selected_button = None

        for screen_text, screen_name in screens:
            btn = Button(text=screen_text, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn, name=screen_name: self.on_button_click(btn, name))
            self.dropdown.add_widget(btn)

        # Main button to trigger the dropdown
        main_button = Button(text="Select Screen", size_hint=(None, None), size=(150, 44))
        main_button.bind(on_release=self.dropdown.open)


        layout = BoxLayout(orientation="vertical")
        layout.add_widget(main_button)
        layout.add_widget(self.sm)

        return layout

    def on_button_click(self, button, screen_name):
        # Reset background of the previously selected button
        if self.selected_button:
            self.selected_button.background_color = (1, 1, 1, 1)

        # Update the current button's background
        button.background_color = (0.5, 1, 0.5, 1)
        self.selected_button = button


        self.switch_screen(screen_name)

    def switch_screen(self, screen_name):
        self.sm.current = screen_name
        self.dropdown.dismiss()


if __name__ == "__main__":
    PowerPlanner().run()
