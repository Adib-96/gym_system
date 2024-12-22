from kivy.app import App
from kivy.properties import StringProperty
from arabic_reshaper import reshape
from bidi.algorithm import get_display

class QrSuccessCode(App):
   arabic_text = StringProperty("")

   """userName from DB"""
   #username_text = StringProperty("")


   def build(self):
      raw_text = "مرحباً"
      resahped_text = reshape(raw_text)
      self.arabic_text = get_display(resahped_text)
      return  super().build()


app = QrSuccessCode()
app.run()