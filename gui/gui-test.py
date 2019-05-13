import kivy
import easygui
kivy.require('1.9.1')

import sys
import os
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.videoplayer import VideoPlayer
from kivy.properties import StringProperty


class Grid(GridLayout):
    def __init__(self, **kwargs):
        super(Grid, self).__init__(**kwargs)


        self.inside_grid = GridLayout()
        self.inside_grid.rows = 2
        #self.inside_grid.cols = 3

        self.rows = 3
        self.player = VideoPlayer()
        self.add_widget(self.player)

        self.open_explorer = Button(text="Select file", font_size=40)
        self.open_explorer.bind(on_press=self.openexp)
        self.inside_grid.add_widget(self.open_explorer)

        self.play_video = Button(text="Play", font_size=40)
        self.play_video.bind(on_press=self.playvid)
        self.inside_grid.add_widget(self.play_video)


        self.add_widget(self.inside_grid)

    def openexp(self, instance):
        self.file = easygui.fileopenbox()
        print(self.file)

    def playvid(self, instance):
        self.player.source = str(self.file)
        if self.player.source.lower().endswith(('.mp4', '.avi', '.mkv', '.flv', '.wmv')):
            print(self.player.source)
            self.player.state = 'play'
        else:
            print('this should be an error i guess')

class VideoPlayerApp(App):
    def build(self):
        return Grid()


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print('You have to pass the path to source file')
        sys.exit()
    if not os.path.isfile(sys.argv[1]):
        print('Error: file not found')
        sys.exit()
    VideoPlayerApp().run()


