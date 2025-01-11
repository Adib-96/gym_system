from kivy.app import App
from kivy.uix.screenmanager import ScreenManager,SlideTransition
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from subcription_view.subscForm import HomeScreen
from scan_view.scan_view import QRCodeScannerScreen
from gym_member_list.gymMembers import MembersDisplay
from kivy.lang.builder import Builder
from membership_Renewal.membership_renewal import Renewal

Builder.load_file("subcription_view/homescreen.kv")
Builder.load_file("gym_member_list/gymmembers.kv")
Builder.load_file("membership_Renewal/myapp.kv")

class PowerPlanner(App):
    def build(self):

        self.sm = ScreenManager(transition=SlideTransition())
        self.sm.add_widget(HomeScreen(name="Membership Registration"))
        self.sm.add_widget(QRCodeScannerScreen(name="QR_code Screen"))
        self.sm.add_widget(MembersDisplay(name="MembersDisplay"))
        self.sm.add_widget(Renewal(name="Membership Renewal"))


        self.dropdown = DropDown()
        screens = [("Membership Registration", "Membership Registration"), ("QR_code Screen", "QR_code Screen"), ("MembersDisplay", "MembersDisplay"),("Membership Renewal","Membership Renewal")]

        self.selected_button = None

        for screen_text, screen_name in screens:
            btn = Button(text=screen_text, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn, name=screen_name: self.on_button_click(btn, name))
            self.dropdown.add_widget(btn)

        # Main button to trigger the dropdown
        main_button = Button(text="Select Screen", size_hint=(None, None), size=(180, 44))
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
