from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from subcription_view.subscForm import HomeScreen
from kivy.lang.builder import Builder


Builder.load_file("subcription_view/homescreen.kv")

class ScreenTwo(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text="Welcome to Screen 2"))


class ScreenThree(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text="Welcome to Screen 3"))


class MainApp(App):
    def build(self):
        # Create ScreenManager and add Screens
        self.sm = ScreenManager()
        self.sm.add_widget(HomeScreen(name="HomeScreen"))
        self.sm.add_widget(ScreenTwo(name="screen2"))
        self.sm.add_widget(ScreenThree(name="screen3"))

        # Create Dropdown Menu
        self.dropdown = DropDown()
        screens = [("Subscription Form", "HomeScreen"), ("Screen 2", "screen2"), ("Screen 3", "screen3")]

        for screen_text, screen_name in screens:
            btn = Button(text=screen_text, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn, name=screen_name: self.switch_screen(name))
            self.dropdown.add_widget(btn)

        # Main button to trigger the dropdown
        main_button = Button(text="Select Screen", size_hint=(None, None), size=(150, 44))
        main_button.bind(on_release=self.dropdown.open)

        # Layout
        layout = BoxLayout(orientation="vertical")
        layout.add_widget(main_button)
        layout.add_widget(self.sm)

        return layout

    def switch_screen(self, screen_name):
        if self.sm.current == screen_name:
            self.dropdown.dismiss()
        self.sm.current = screen_name
        self.dropdown.dismiss()


if __name__ == "__main__":
    MainApp().run()
