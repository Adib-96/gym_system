from kivy.app import App
from kivy.uix.boxlayout import BoxLayout




class GymMembers(BoxLayout):
    def display_text(self):
        user_input = self.ids.search_input.text
        print(f"user_input: {user_input}")


class GymMembersApp(App):
    def build(self):
        return GymMembers()


if __name__ == '__main__':
    app = GymMembersApp()
    app.run()