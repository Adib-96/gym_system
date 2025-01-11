from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen

class RenewalWidget(BoxLayout):
    def print_selected_subscription(self):
        if self.ids.monthly.active:
            print("Monthly")
        elif self.ids.s_20.active:
            print("20 Sessions")
        elif self.ids.s_30.active:
            print("30 Sessions")
        else:
            print("No subscription selected.")

class Renewal(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(RenewalWidget())
