from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget

from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition

import time

from kivy.config import Config
Config.set('graphics', 'fullscreen', '1')

Builder.load_string('''
<MenuScreen>:
    BoxLayout:
        orientation: 'vertical'
        Button:
            text: 'Change background'
            on_release: root.manager.current = 'backgrounds'
        Button:
            text: 'Capture new clip'
            on_release: root.manager.current = 'capture'
        Button:
            text: 'Settings'
            on_release: root.manager.current = 'settings'

<BackgroundsScreen>:
    BoxLayout:
        orientation: 'vertical'

        Button:
            text: 'placeholder'
            size_hint_y: None
            height: '48dp'
        Button:
            text: 'Back to menu'
            size_hint_y: None
            height: '48dp'
            on_release: root.manager.current = 'menu'

<CaptureScreen>:
    FloatLayout:
        orientation: 'horizontal'
        CameraWidget:

<CameraWidget>:
    FloatLayout:
        size_hint_x: None
        size_hint_y: None
        size: root.size
        post: root.pos
        orientation: 'vertical'
        Camera:
            id: camera
            index: 0
            resolution: (1280, 1080)
            play: False
        BoxLayout:
            Button:
                text: 'Start camera'
                size_hint_y: None
                height: '48dp'
                on_press: camera.play = not camera.play
            Button:
                text: 'Capture'
                size_hint_y: None
                height: '48dp'
                on_press: root.capture(); overlay.source = root.filename
            Button:
                text: 'Finish animation'
                size_hint_y: None
                height: '48dp'
                width: 0.5
                on_press: camera.play = False; pass
                on_release: app.sm.current = 'menu'
        BoxLayout:
            size: root.size
            post: root.pos
            orientation: 'vertical'
            opacity: 0.33
            Image:
                id: overlay
                source: 'image.jpg'

<SettingsScreen>:
    BoxLayout:
        size: root.size
        post: root.pos
        orientation: 'vertical'
        Button:
            text: 'placeholder button for now'
        Button:
            text: 'Back to menu'
            on_release: root.manager.current = 'menu'

''')

class CameraWidget(Widget):
    filename = 'image.jpg'
    def __init__ (self,**kwargs):
        super ().__init__(**kwargs)

    def capture(self):
        '''Function to capture images and name them
        according to their time and date.
        '''
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        self.filename = "IMG_{}.png".format(timestr)
        camera.export_to_png(self.filename)
        print("Captured")

class BackgroundsScreen(Screen):
    """
    Screen containing the backgrounds on which the animations are overlain
    """
    def __init__ (self,**kwargs):
        super ().__init__(**kwargs)

class CaptureScreen(Screen):
    """
    Screen containing the camera control for capturing stop motion animations
    """
    def __init__ (self,**kwargs):
        super ().__init__(**kwargs)

class SettingsScreen(Screen):
    """
    Screen containing the settings for greenscreening the animations
    """
    def __init__ (self,**kwargs):
        super ().__init__(**kwargs)

class MenuScreen(Screen):
    """
    Screen containing the menu buttons for the different modes of the app
    """
    def __init__ (self,**kwargs):
        super ().__init__(**kwargs)

class StopMotionApp(App):
    sm = None # The root screen manager
    def build(self):
        self.sm = ScreenManager(transition=FadeTransition())
        self.sm.add_widget(MenuScreen(name='menu'))
        self.sm.add_widget(BackgroundsScreen(name='backgrounds'))
        self.sm.add_widget(CaptureScreen(name='capture'))
        self.sm.add_widget(SettingsScreen(name='settings'))
        self.sm.current = 'menu'
        return self.sm

if __name__ == '__main__':
    StopMotionApp().run()
