import kivy
kivy.require('1.9.1')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout

from kivy.uix.videoplayer import VideoPlayer


class VideoPlayerApp(App):

    def build(self):

        self.player = VideoPlayer()

        return (self.player)


if __name__ == '__main__':
    VideoPlayerApp().run()
