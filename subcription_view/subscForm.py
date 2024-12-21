from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label  # Import the correct Label class
from kivy.config import Config
from kivy.core.window import Window
from datetime import datetime

# Set configuration
Window.clearcolor = (1, 1, 1, 1)  # RGBA: White

Config.set('graphics', 'width', '1280')
Config.set('graphics', 'height', '900')
Config.set('graphics', 'resizable', '1')


class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.popup = None

    def submit_form(self):
        name = self.ids.name_input.text
        age = self.ids.age_input.text
        email = self.ids.email_input.text
        activity = None
        sub_methode = None

        # Iterate over Activities
        for activ_button in [self.ids.bodybuilding, self.ids.karate, self.ids.aerobic]:
            if activ_button.state == 'down':
                activity = activ_button.text
                break

        # Iterate over subscription methods
        for sub_button in [self.ids.monthly, self.ids.s_20, self.ids.s_30]:
            if sub_button.state == 'down':
                sub_methode = sub_button.text.split()[0]
                break

        print({
            'name': name,
            'age': age,
            'email': email,
            'date': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            'activity': activity,
            'sub_methode': sub_methode
        })

        self.show_popup()

        # Reset form fields
        activ_button.state = 'normal'
        sub_button.state = 'normal'
        self.ids.name_input.text = ""
        self.ids.age_input.text = ""
        self.ids.email_input.text = ""

    def show_popup(self):
        layout = BoxLayout(orientation='vertical')
        lbl = Label(text="Member created successfully",font_size="30pt",color=(0.4,0.5,0.6,1))  # Use Kivy's Label
        close_button = Button(text="Close",size_hint=(0.4,0.1),pos_hint={'x':0.3})
        close_button.bind(on_press=self.close_popup)  # Bind close button to dismiss the popup
        layout.add_widget(lbl)
        layout.add_widget(close_button)
        self.popup = Popup(
            title='Subscribe Form',
            content=layout,
            auto_dismiss=False,
            size_hint=(0.8, 0.8),
            size=(400, 400)
        )
        self.popup.open()

    def close_popup(self, instance):
        self.popup.dismiss()


class HomeScreen(App):
    def build(self):
        return MainLayout()


if __name__ == '__main__':
    HomeScreen().run()
