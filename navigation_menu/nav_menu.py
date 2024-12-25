from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.core.window import Window

Window.clearcolor = (1, 1, 1, 1)
"""
The NavMenu Kivy application is a gym management system's graphical user interface component. 
It includes a navigation menu triggered by clicking on an image,
presenting various gym-related options in a dropdown menu.
"""
class NavMenu(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"

        self.my_image = Image(
            source='menu.png',
            size_hint=(None, None),
            pos_hint={"x": 0, "y": 0.89},
            size=(120, 80)
        )
        self.my_image.bind(on_touch_down=self.print_if_clicked)

        # Add the image widget to the layout

        self.add_widget(self.my_image)

    def print_if_clicked(self, instance, touch):
        if instance.collide_point(touch.x, touch.y):
            dropdown = DropDown()
            options = ["Home", "Subscription", "ReSubscription", "Members list", "QR code Reader"]
            for option in options:
                btn = Button(
                    text=option,
                    size_hint=(1, None),
                    height=40,
                    on_press=lambda btn: dropdown.select(btn.text)
                )
                dropdown.add_widget(btn)
            dropdown.open(self.my_image)
