from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label


class RenewalScreen(BoxLayout):
        def resubscribe(self):
            print("clicke")


class MyApp(App):

    def build(self):
        return RenewalScreen()

if __name__ == "__main__":
    app = MyApp()
    app.run()
