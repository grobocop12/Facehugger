import kivy
kivy.require('1.9.1')

import sys
import os
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout

from kivy.uix.videoplayer import VideoPlayer


class VideoPlayerApp(App):

    def build(self):

        self.player = VideoPlayer()
        self.player.source = sys.argv[1]
        return (self.player)


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print('You have to pass the path to source file')
        sys.exit()
    if not os.path.isfile(sys.argv[1]):
        print('Error: file not found')
        sys.exit()
    VideoPlayerApp().run()
