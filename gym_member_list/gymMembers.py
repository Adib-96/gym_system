from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.properties import ListProperty
from warehouse.database import fetch_all, membership_renewal
from datetime import datetime
from functools import partial

class GymMembers(BoxLayout):
    members = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(members=self.display_data)

    def collect_filters(self):
        
        # Fetch data and update members list
        self.members = fetch_all()

    def display_data(self, instance, value):
        self.ids.user_display.clear_widgets()
        for user in self.members:
            statut = "inactive.png"
            #*case when membership is active
            if user[3] == "monthly" and user[4] is not None and datetime.now() <= datetime.strptime(user[4], '%Y/%m/%d'):
                statut = "active.png"
            elif user[3] in ('20_session', '30_session') and user[5] > 0:
                statut = "active.png"

            username_label = Label(text=user[1], size_hint=(1, None), height=64, font_size=16, bold=True)
            activity_label = Label(text=user[2], size_hint=(1, None), height=64, font_size=16)
            sub_methode = Label(text=user[3], size_hint=(1, None), height=64, font_size=16)
            img_active_inactive = Image(source=statut, size_hint=(1, None), height=64)

            renewal_label = Button(text="Renewal", size_hint=(1, None), height=65, font_size="16sp")
            renewal_label.on_press = partial(self.renew_membership, user[0], user[3], img_active_inactive)

            self.ids.user_display.add_widget(username_label)
            self.ids.user_display.add_widget(activity_label)
            self.ids.user_display.add_widget(sub_methode)
            self.ids.user_display.add_widget(img_active_inactive)
            self.ids.user_display.add_widget(renewal_label)

    def renew_membership(self, member_id, sub_method, img_widget):
        # Perform renewal logic
        membership_renewal(member_id, sub_method)
        
        # Update the image to show active status
        img_widget.source = "active.png"
        img_widget.reload()  # Refresh the image to apply the new source #!Here Where to autoReload

class MembersDisplay(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.gym_members = GymMembers()
        self.add_widget(self.gym_members)

