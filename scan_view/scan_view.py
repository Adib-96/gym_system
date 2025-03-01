from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from datetime import datetime
import cv2
from pyzbar.pyzbar import decode
from utils.encod_decod_QR import decode_and_verify_qr_data

class QRCodeScannerScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.img = Image(size_hint=(1, 0.8))
        self.layout.add_widget(self.img)
        self.message = Button(text="No QR Code Detected", font_size='24sp', size_hint=(1, 0.2))
        self.layout.add_widget(self.message)
        self.add_widget(self.layout)
        self.capture = None

    def on_enter(self, *args):
        # Open the camera when this screen is entered
        self.capture = cv2.VideoCapture(0)  # Use the appropriate camera index for your device
        Clock.schedule_interval(self.update, 1.0 / 30.0)

    def on_leave(self, *args):
        # Release the camera when leaving the screen
        Clock.unschedule(self.update)
        self.capture.release()

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            # Convert the frame to texture for display
            buffer = cv2.flip(frame, 0).tobytes()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
            self.img.texture = texture

            # Decode QR codes in the frame
            for code in decode(frame):
                qr_data = code.data.decode('utf-8')

                # Process the QR code every time it is scanned
                member_info = decode_and_verify_qr_data(qr_data)

                # Update the UI based on the status message
                if member_info[0] is None:
                    self.message.text = "Session updated successfully {}".format(*member_info[1])
                    self.message.color = "green"
                else:
                    self.message.text = "{} {}".format(member_info[0], *member_info[1])
                    self.message.color = "red"