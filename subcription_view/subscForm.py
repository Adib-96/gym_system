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
Config.set('graphics', 'width', '720')
Config.set('graphics', 'height', '300')
Config.set('graphics', 'resizable', '1')




class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 10
        self.padding = 30
        # Username label and input field
        username_label = Label(markup=True,text="[b]Username[/b]",font_size='20sp',color="black",pos_hint= {'center_x':.07, 'center_y':.8})
        self.username = TextInput(hint_text="Let us know your name",multiline=False,font_size="20sp",height=55,pos_hint= {'center_x':.5, 'center_y':.8})

        # age label and input field
        age_label = Label(markup=True,text="[b]Age[/b]" ,font_size='20sp',color="black",height=30,pos_hint= {'center_x':.03, 'center_y':.8})
        self.age = TextInput(hint_text="Let us know your age",multiline=False, font_size="20sp",height=55,pos_hint= {'center_x':.5, 'center_y':.8})

        #email label and input field
        email_label = Label(markup=True,text='[b]Email[/b]',font_size='20sp',color="black",height=30,pos_hint= {'center_x':.04, 'center_y':.8})
        self.email = TextInput(hint_text="Let us know your email",multiline=False, font_size="20sp",height=55,pos_hint= {'center_x':.5, 'center_y':.8})


        #Gym activity
        """-----------------------------------------------------------"""
        box_for_activity = BoxLayout()
        box_for_activity.spacing = 10
        box_for_activity.orientation = 'horizontal'

        gym_activity = Label(markup=True,text="[b]Activity[/b]",font_size='20sp',color='black',pos_hint= {'center_x':.05, 'center_y':.8})


        self.bodybuilding = ToggleButton(text="bodybuilding",group="activity")
        self.karate = ToggleButton(text="karate",group="activity")
        self.aerobic =ToggleButton(text="aerobic",group="activity")

        box_for_activity.add_widget( self.bodybuilding)
        box_for_activity.add_widget( self.karate)
        box_for_activity.add_widget(self.aerobic)
        """-----------------------------------------------------------"""

        """-----------------------------------------------------------"""

        ##subscription methode

        subscription_container = BoxLayout()
        subscription_container.orientation = 'horizontal'
        subscription_container.spacing = 20
        subscription_methode = Label(text="[b]Subsc Methode[/b]",color=(0,0,0,1),font_size='20sp',markup=True,halign="left",pos_hint= {'center_x':.09, 'center_y':.8})

        self.normal_sub = ToggleButton(text="monthly",group="subscription_methode")
        self.session_20 = ToggleButton(text="20_session",group="subscription_methode")
        self.session_30 = ToggleButton(text="30_session",group="subscription_methode")


        subscription_container.add_widget(self.normal_sub)
        subscription_container.add_widget(self.session_20)
        subscription_container.add_widget(self.session_30)


        """-----------------------------------------------------------"""


        # Submit button
        submit_methode = Button(text="Submit" ,font_size=25, color=(.2,1,.5,1),on_press=self.on_button_press,size_hint= (.5, None),
                      pos_hint= {'center_x':.5, 'center_y':.8},height='50')

        # Add widgets to layout
        self.add_widget(username_label)
        self.add_widget(self.username)
        self.add_widget(age_label)
        self.add_widget(self.age)
        self.add_widget(email_label)
        self.add_widget(self.email)

        self.add_widget(gym_activity)
        self.add_widget(box_for_activity)
        self.add_widget(subscription_methode)
        self.add_widget(subscription_container)

        self.add_widget(submit_methode)


    # display date
    @staticmethod
    def get_current_time():
        return datetime.now().strftime("%d/%m/%Y %H:%M:%S")




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





class SubForm(App):
    def build(self):
        return MainLayout()


if __name__ == '__main__':
    SubForm().run()
