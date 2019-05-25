import kivy
import easygui
import copy
kivy.require("1.9.0")

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.listview import ListItemButton
from kivy.uix.gridlayout import GridLayout

faces = []

class Face:
    def __init__(self, name, pictures):
        self.name = name
        self.pictures = pictures


class ListButton(ListItemButton):
    pass


class Faces(BoxLayout):
    name_text_input = ObjectProperty()
    picture_list = []
    face_list = ObjectProperty()

    def train(self):
        print("training!")

    def submit_face(self):
        face_name = self.name_text_input.text
        if face_name:
            check_name = False
            if face_name in self.face_list.adapter.data:
                check_name = True
                print("name already exists")

            if not check_name:
                self.face_list.adapter.data.extend([face_name])
                self.face_list._trigger_reset_populate()


    def delete_face(self):
        if self.face_list.adapter.selection:
            selection = self.face_list.adapter.selection[0].text
            self.face_list.adapter.data.remove(selection)
            if faces:
                faces.pop(Faces.get_face_index(selection))
            self.face_list._trigger_reset_populate()

    def add_pictures(self):
        self.picture_list = easygui.fileopenbox(multiple=True)

        if self.face_list.adapter.selection:
            selection = self.face_list.adapter.selection[0].text
            # add selection to list
            selected_face = Face(selection, self.picture_list)
            faces.append(copy.copy(selected_face))

        print("list: ")
        for i in range(len(faces)):
            print(faces[i].name)
            for j in range(len(faces[i].pictures)):
                print(faces[i].pictures[j])

    def get_face_index(name):
        for i, f in enumerate(faces):
            if f.name == name:
                return i
        return -1

class InterfaceApp(App):
    def build(self):
        return Faces()


if __name__ == '__main__':
    InterfaceApp().run()
