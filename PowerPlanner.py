from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder
from kivy.graphics import Color, Rectangle
from kivy.uix.image import Image
# Import your screens
from subcription_view.subscForm import HomeScreen
from scan_view.scan_view import QRCodeScannerScreen
from gym_member_list.gymMembers import MembersDisplay

# Load KV files
Builder.load_file("subcription_view/homescreen.kv")
Builder.load_file("gym_member_list/gymmembers.kv")

class PowerPlanner(App):
    def build(self):
        # ScreenManager setup
        self.sm = ScreenManager(transition=SlideTransition())
        self.sm.add_widget(HomeScreen(name="Membership Registration"))
        self.sm.add_widget(QRCodeScannerScreen(name="QR_code Screen"))
        self.sm.add_widget(MembersDisplay(name="MembersDisplay"))

        # Dropdown setup
        self.dropdown = DropDown()
        screens = [("Membership Registration", "Membership Registration"), 
                   ("QR_code Screen", "QR_code Screen"), 
                   ("MembersDisplay", "MembersDisplay"),
                   ]
        
        self.selected_button = None
        main_button = Button( text = "SELECT SCREEN",size_hint=(None, None), size=(180, 50))
        main_button.bind(on_release=self.dropdown.open)
        
        for screen_text, screen_name in screens:
            btn = Button(text=screen_text, size_hint=(None,None), height=44,width=180)
            btn.bind(on_release=lambda btn, name=screen_name: self.on_button_click(btn, name))
            self.dropdown.add_widget(btn)

        # Main button to trigger the dropdown


        # BoxLayout setup with background color
        layout = BoxLayout(orientation="vertical")
        with layout.canvas.before:
            Color(0,0,0,0.7)  # Light grey background
            self.rect = Rectangle(size=layout.size, pos=layout.pos)
        layout.bind(size=self._update_rect, pos=self._update_rect)
        layout.padding = 20
        layout.add_widget(main_button)
        layout.add_widget(self.sm)

        return layout

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def on_button_click(self, button, screen_name):
        if self.selected_button:
            self.selected_button.background_color = (1, 1, 1, 1)
        button.background_color = (0.5, 1, 0.5, 1)
        self.selected_button = button
        self.switch_screen(screen_name)

    def switch_screen(self, screen_name):
        self.sm.current = screen_name
        self.dropdown.dismiss()

if __name__ == "__main__":
    PowerPlanner().run()
