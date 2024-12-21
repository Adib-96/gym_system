from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.togglebutton import ToggleButton
from datetime import datetime


#set configuration
Window.clearcolor = (1, 1, 1, 1)  # RGBA: White

Config.set('graphics', 'width', '1280')
Config.set('graphics', 'height', '900')
Config.set('graphics', 'resizable', '1')


class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def submit_form(self):
        name = self.ids.name_input.text
        age = self.ids.age_input.text
        email = self.ids.email_input.text
        activity = None
        sub_methode = None
        ##iterate over Activities
        for activ_button in [self.ids.bodybuilding, self.ids.karate,self.ids.aerobic]:
            if activ_button.state == 'down':
                activity = activ_button.text
                break

        ##iterate over sub methode

        for sub_button in [self.ids.monthly,self.ids.s_20,self.ids.s_30]:
            if sub_button.state == 'down':
                sub_methode = sub_button.text.split()[0]
                break
        print({'name':name, 'age':age, 'email':email,'date':datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 'activity':activity, 'sub_methode':sub_methode})
    pass
"""
    def on_button_press(self, instance):

        ## activity logic to found the activity pressed
        selected_activity = None
        for button in [self.bodybuilding, self.karate, self.aerobic]:
            if button.state == "down":
                selected_activity = button.text
                #to minimize algorithm loop :)
                break


        ## subscription methodes to found the one pressed
        selected_sub_methode = None
        for btn in [self.normal_sub, self.session_20, self.session_30, self.normal_sub]:
            if btn.state == "down":
                selected_sub_methode = btn.text
                break


        # Print input data on button press
        print({
            "username": self.username.text,
            "age": self.age.text,
            "gym_activity": selected_activity,
            "email": self.email.text,
            "entry_time": MainLayout.get_current_time(),
            "subscription_methode":selected_sub_methode
        })
        ## reset form fields
        self.username.text = ""
        self.age.text = ""
        self.email.text = ""
        button.state ="normal"
        btn.state = "normal"

        print(f"{instance.text} Button pressed!")
    """



class SubForm(App):
    def build(self):
        return MainLayout()



if __name__ == '__main__':
    SubForm().run()
