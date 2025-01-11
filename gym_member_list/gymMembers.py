from kivy.uix.effectwidget import Rectangle
from kivy.uix.behaviors.touchripple import Color
from kivy.uix.actionbar import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.core.clipboard import Clipboard


class GymMembers(BoxLayout):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        #Todo fetch data from DB
        self.users = []
        
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
        
        #!!!!!!!!!!!!!!!!!!!!!!!!
        
        self.display_data(username=username,activity=selected_activities,subscription_method = selected_methods)
        #!!!!!!!!!!!!!!!!!!!!!!!!
        
        
    def display_data(self,**kwargs):
        # object destructring 
        username,activity,subscription_method = kwargs
        
        ## clear old dataaaaa
        self.ids.user_display.clear_widgets()
        
        ##? here we gonna pull data from sqlite and push it down
        for user in self.users:
            lb0 = Label(text=str(user['id']), size_hint_y=None, height=50,font_size=16)
            lb0.bind(on_touch_down=self.copy_to_clipboard)
            with lb0.canvas.before:
                Color(0.776, 0.675, 0.561, 1)
                Rectangle(size=lb0.size, pos=lb0.pos)
            lb0.bind(size=self.update_rect, pos=self.update_rect)
            
            
            lb1 = Label(text=user['username'], size_hint_y=None, height=50,font_size=16)
            with lb1.canvas.before:
                Color(0.776, 0.675, 0.561, 1)
                Rectangle(size=lb1.size, pos=lb1.pos)
            lb1.bind(size=self.update_rect, pos=self.update_rect)

            lb2 = Label(text=user['activity'], size_hint_y=None, height=50,font_size=16)
            with lb2.canvas.before:
                Color(0.851, 0.851, 0.851, 1)
                Rectangle(size=lb1.size, pos=lb1.pos)
            lb2.bind(size=self.update_rect, pos=self.update_rect)

            lb3 = Label(text=user['subscription'], size_hint_y=None, height=50,font_size=16)
            with lb3.canvas.before:
                Color(0.851, 0.851, 0.851, 1)
                Rectangle(size=lb1.size, pos=lb1.pos)
            lb3.bind(size=self.update_rect, pos=self.update_rect)

            lb4 = Label(text="ExpDate/RemainingSessions", size_hint_y=None, height=50,font_size=16)
            with lb4.canvas.before:
                Color(0.851, 0.851, 0.851, 1)
                Rectangle(size=lb1.size, pos=lb1.pos)
            lb4.bind(size=self.update_rect, pos=self.update_rect)
            
            self.ids.user_display.add_widget(lb0)
            self.ids.user_display.add_widget(lb1)
            self.ids.user_display.add_widget(lb2)
            self.ids.user_display.add_widget(lb3)
            self.ids.user_display.add_widget(lb4)
    
    def update_rect(self, instance, value):
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(0.918, 0.878, 0.835, 0.2)
            Rectangle(size=instance.size, pos=instance.pos)
            
    ## instance = the label copied
    def copy_to_clipboard(self, instance, touch):
        print(instance)
        if instance.collide_point(*touch.pos):
            # Copy the text from the label to the clipboard
            Clipboard.copy(instance.text)
            print("Text copied to clipboard:", instance.text)


class MembersDisplay(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(GymMembers())