from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.core.window import Window

Window.clearcolor = (1,1,1,1)




class NavMenu(App):
    def print_if_clicked(self,instance,touch):
        if instance.collide_point(touch.x , touch.y):
            dropdown = DropDown()
            home = Button(text="Home",size_hint=(1,None),height=40,on_press=lambda btn:dropdown.select(btn.text))
            subsc = Button(text="Subscription",size_hint=(1,None),height=40,on_press=lambda btn:dropdown.select(btn.text))
            resub =Button(text="ReSubscription",size_hint=(1,None),height=40,on_press=lambda btn:dropdown.select(btn.text))
            members_list = Button(text="Members list",size_hint=(1,None),height=40,on_press=lambda btn:dropdown.select(btn.text))
            QR_reader = Button(text="QR code Reader",size_hint=(1,None),height=40,on_press=lambda btn:dropdown.select(btn.text))
            dropdown.add_widget(home)
            dropdown.add_widget(subsc)
            dropdown.add_widget(resub)
            dropdown.add_widget(members_list)
            dropdown.add_widget(QR_reader)
            dropdown.open(self.my_image)
    def build(self):
        self.container = BoxLayout()
        self.container.orientation = "horizontal"
        self.my_image = Image(source='menu.png',size_hint=(None,None),pos_hint={"x":0,"y":0.89},size=(120,80))
        self.my_image.bind(on_touch_down=self.print_if_clicked)
        self.container.add_widget(self.my_image)
        return self.container

if __name__ == '__main__':
    NavMenu().run()
