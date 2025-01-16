from kivy.uix.effectwidget import Rectangle
from kivy.uix.behaviors.touchripple import Color
from kivy.uix.actionbar import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.core.clipboard import Clipboard
from kivy.uix.image import Image
from warehouse.database import fetch_all

class GymMembers(BoxLayout):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        #Todo fetch data from DB
        self.members = []
        
    def collect_filters(self):
        
        
        
        username = self.ids.username_filter.text.strip()
        selected_activities = []
        if self.ids.bodybuilding.active:
            selected_activities.append("bodybuilding")
        if self.ids.crossfit.active:
            selected_activities.append("crossfit")
        if self.ids.martial_arts.active:
            selected_activities.append("mixed_arts")
        
        # Collect subscription method filter data
        selected_methods = []
        if self.ids.monthly.active:
            selected_methods.append("monthly")
        if self.ids.session_20.active:
            selected_methods.append("20_session")
        if self.ids.session_30.active:
            selected_methods.append("30_session")
        
        
        
        #Todo===========================================================================================================
        #Todo        FETCH DATA FROM WAREHOUSE THEN PASS THE RESULT  and passe it to SELF.USERS                         |
        #Todo===========================================================================================================
        
        
        #!!!!!!!!!!!!!!!!!!!!!!!!
        #TodoDISPLAY_DATA(id,username,activity,subscription_methode,end_date,remaining_session)|
        members = fetch_all()
        self.members = members
        self.display_data()

        #!!!!!!!!!!!!!!!!!!!!!!!!
        
        
    def display_data(self):
        
        
        ## clear old dataaaaa
        self.ids.user_display.clear_widgets()
        
        ##? here we gonna pull data from sqlite and push it down
        for user in self.members:
            
            lb0 = Label(text=user[0], size_hint=(None,None),width=350,height=50,font_size=16)
            lb0.bind(on_touch_down=self.copy_to_clipboard)
            with lb0.canvas.before:
                Color(0.776, 0.675, 0.561, 1)
                Rectangle(size=lb0.size, pos=lb0.pos)
            lb0.bind(size=self.update_rect, pos=self.update_rect)
            
            
            lb1 = Label(text=user[1],size_hint=(1,None), height=50,font_size=16)
            with lb1.canvas.before:
                Color(0.776, 0.675, 0.561, 1)
                Rectangle(size=lb1.size, pos=lb1.pos)
            lb1.bind(size=self.update_rect, pos=self.update_rect)

            lb2 = Label(text=user[2],size_hint=(None,None), width=250,height=50,font_size=16)
            with lb2.canvas.before:
                Color(0.851, 0.851, 0.851, 1)
                Rectangle(size=lb1.size, pos=lb1.pos)
            lb2.bind(size=self.update_rect, pos=self.update_rect)

            lb3 = Label(text=user[3] ,size_hint=(1,None), height=50,font_size=16,padding=[0.4,0.9,0.4,0.4])
            with lb3.canvas.before:
                Color(0.851, 0.851, 0.851, 1)
                Rectangle(size=lb1.size, pos=lb1.pos)
            lb3.bind(size=self.update_rect, pos=self.update_rect)

            img = Image(source="button.png" ,fit_mode="scale-down",size_hint= (None, None),size=(280,50))
            with img.canvas.before:
                Color(0.851, 0.851, 0.851, 1)
                Rectangle(size=lb1.size, pos=lb1.pos)
            img.bind(size=self.update_rect, pos=self.update_rect)
            
            self.ids.user_display.add_widget(lb0)
            self.ids.user_display.add_widget(lb1)
            self.ids.user_display.add_widget(lb2)
            self.ids.user_display.add_widget(lb3)
            self.ids.user_display.add_widget(img)
    
    def update_rect(self, instance, value):
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(0.918, 0.878, 0.835, 0.2)
            Rectangle(size=instance.size, pos=instance.pos)
            
    ## instance = the label copied
    def copy_to_clipboard(self, instance, touch):
        if instance.collide_point(*touch.pos):
            # Copy the text from the label to the clipboard
            Clipboard.copy(instance.text)
            print("Text copied to clipboard:", instance.text)


class MembersDisplay(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(GymMembers())