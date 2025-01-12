from kivy.uix.actionbar import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label 
from kivy.uix.button import Button  # Import the correct Label class
# Import the correct Label class

class RenewalWidget(BoxLayout):
    def print_selected_subscription(self):
        layout = BoxLayout(orientation='vertical')
        layout.padding = 25
        layout.spacing = 200
        
        lbl = Label(text="Success! Your renewal was completed successfully.",font_size="25pt",color=(0.184, 0.654, 0.831, 1.0))
        close_button = Button(text="Close",size_hint=(None,0.3),pos_hint={"center_x":0.5},width=250)
        close_button.bind(on_press=self.close_popup)  # Bind close button to dismiss the popup
        layout.add_widget(lbl)
        layout.add_widget(close_button)
        member_id = self.ids.Id.text
        print(member_id)
        if self.ids.monthly.active:
            print("Monthly")
        elif self.ids.s_20.active:
            print("20 Sessions")
        elif self.ids.s_30.active:
            print("30 Sessions")
        else:
            print("No subscription selected.")
        self.popup = Popup(
            title='Subscribe Form',
            content=layout,
            auto_dismiss=False,
            size_hint=(0.8, 0.8),
            size=(200, 200)
        )
        self.popup.open()

    def close_popup(self, instance):
        self.popup.dismiss()

class Renewal(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(RenewalWidget())
