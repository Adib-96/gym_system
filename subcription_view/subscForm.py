from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label  # Import the correct Label class
from kivy.config import Config
from kivy.core.window import Window
from datetime import datetime
from kivy.uix.screenmanager import Screen
import uuid
from utils.encod_decod_QR import generate_qrcode
from warehouse.database import create_member
from warehouse.database import create_new_subscription
from datetime import datetime,timedelta



# Set configuration
Window.clearcolor = (1, 1, 1, 1)  # RGBA: White

Config.set('graphics', 'width', '1280')
Config.set('graphics', 'height', '900')
Config.set('graphics', 'resizable', '1')


class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.popup = None
        self.user_info = {}


    def submit_form(self):
        name = self.ids.name_input.text
        age = self.ids.age_input.text
        email = self.ids.email_input.text
        activity = None
        sub_methode = None

        # Iterate over Activities
        for activ_button in [self.ids.bodybuilding, self.ids.crossfit, self.ids.Mixed_Arts]:
            if activ_button.state == 'down':
                activity = activ_button.text
                break

        # Iterate over subscription methods
        for sub_button in [self.ids.monthly, self.ids.s_20, self.ids.s_30]:
            if sub_button.state == 'down':
                sub_methode = sub_button.text.split()[0]
                break
            
        
        ## populate user info with data
        self.user_info['name'] = None if len(name) == 0 else str.lower(name)
        self.user_info['age'] = age
        self.user_info['email'] = email
        self.user_info['activity'] = None if activity is None else str.lower(activity) 
        self.user_info['sub_methode'] = None if sub_methode is None else str.lower(sub_methode)
        self.user_info['date'] = datetime.now().strftime("%Y/%m/%d")
        
        
        ## widgt(label) for displaying error message
        error_submit_form = self.ids.error_text
        ##! Handle empty Form
        if self.user_info['name'] is not None and self.user_info['activity'] is not None and self.user_info['sub_methode'] is not None:
            self.show_popup()
            error_submit_form.text = ''
        else:
            error_submit_form.bold = True
            error_submit_form.text = "Please fill all required fields."
            print('You must fill the name,activity and subscription method to pass dear friend')

        # Reset form fields
        activ_button.state = 'normal'
        sub_button.state = 'normal'
        self.ids.name_input.text = ""
        self.ids.age_input.text = ""
        self.ids.email_input.text = ""

    def show_popup(self):
        
        
        user_id = str(uuid.uuid4())
        self.user_info['id'] = user_id
        
        
        #!-------------------- add user_info to DB------------------------------------------------------------------------------------
        create_member(member_id=self.user_info['id'],name=self.user_info['name'],age=self.user_info['age'],email=self.user_info['email'])
        #* Monthly Subscription
        if self.user_info["sub_methode"] == "monthly":
            end_date = datetime.strptime(self.user_info["date"], '%Y/%m/%d') + timedelta(days=30)
            formatted_end_data = end_date.strftime('%Y/%m/%d')
            create_new_subscription(
                                    member_id=self.user_info['id'],
                                    subscription_method=self.user_info['sub_methode'],
                                    subscription_start_dt=self.user_info['date'],
                                    subscription_end_dt=formatted_end_data,
                                    remaining_sessions=None,
                                    activity=self.user_info["activity"]
                                    )
        else:
            sessions = None
            subscription_methode = self.user_info['sub_methode']
            if subscription_methode == "20_session":
                sessions = 20
            else:
                sessions = 30
            create_new_subscription(
                                    member_id=self.user_info['id'],
                                    subscription_method=subscription_methode,
                                    subscription_start_dt=self.user_info['date'],
                                    subscription_end_dt=None,
                                    remaining_sessions=sessions,
                                    activity=self.user_info["activity"]
                                    )
        #!-------------------- add user_info to DB------------------------------------------------------------------------------------
        
        ###############################***********************###################################
        ###############################***********************###################################

        layout = BoxLayout(orientation='vertical')
        layout.padding = 25
        lbl = Label(text="Member created successfully",font_size="25pt",color=(0.184, 0.654, 0.831, 1.0),size_hint=(None, None),height=20,pos_hint = {'x':0.45,'y':0.9})
        lb_scan_your_code = Label(text="Scan your Code",font_size="25pt",color=(0.184, 0.654, 0.831, 1.0),size_hint=(None, None),pos_hint = {'x':0.45,'y':0.1})

        ### GENERATING QR CODE
        generate_qrcode(user_id)

        qrCode = Image(source="./qr_images/{}.png".format(user_id))
        qrCode.size_hint= (.4,.3)
        qrCode.pos_hint= {'x':.3, 'y':.1}
        close_button = Button(text="Close",size_hint=(.5,0.07),pos_hint={'x':.25,'y':.1})
        close_button.bind(on_press=self.close_popup)  # Bind close button to dismiss the popup
        ## add widgets to container
        layout.add_widget(lbl)
        layout.add_widget(lb_scan_your_code)
        layout.add_widget(qrCode)
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


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(MainLayout())


