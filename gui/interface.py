from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.listview import ListItemButton
from kivy.core.window import Window
from kivy.properties import StringProperty

import kivy
import easygui
import copy
kivy.require("1.9.0")


# Face object list
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
    info = StringProperty()

    # method called by "Train" button
    def train(self):
        print("training!")

    # adding names to list
    def submit_face(self):
        self.info = ""
        face_name = self.name_text_input.text
        if face_name:
            check_name = False
            if face_name in self.face_list.adapter.data:
                check_name = True
                self.info = "name already exists"

            if not check_name:
                self.face_list.adapter.data.extend([face_name])
                self.face_list._trigger_reset_populate()
        else:
            self.info = "name cannot be empty"

    # deleting items from list
    def delete_face(self):
        self.info = ""
        if self.face_list.adapter.selection:
            selection = self.face_list.adapter.selection[0].text
            self.face_list.adapter.data.remove(selection)
            if faces:
                faces.pop(Faces.get_face_index(selection))
            self.face_list._trigger_reset_populate()
            #self.face_list.adapter.selection = None
        else:
            self.info = "select item to delete"

    # loading pictures from file explorer
    def add_pictures(self):
        self.info = ""
        if self.face_list.adapter.selection:
            self.picture_list = easygui.fileopenbox(multiple=True)
            selection = self.face_list.adapter.selection[0].text

            # check file extensions
            if self.picture_list:
                self.picture_list = [x for x in self.picture_list if x.endswith('jpg') or x.endswith('png')]
                # create new objects
                if self.picture_list:
                    for i in range(len(faces)):
                        if faces[i].name == selection:
                            faces.pop(Faces.get_face_index(selection))
                            self.info = "item has been overwritten"

                    selected_face = Face(selection, self.picture_list)
                    faces.append(copy.copy(selected_face))
                else:
                    self.info = "no useful files found"
            else:
                self.info = "no pictures have been selected"
        else:
            self.info = "select item to upload pictures"
            try:
                selected_face = Face(selection, self.picture_list)
                faces.append(copy.copy(selected_face))
            except UnboundLocalError:
                pass
        else:
            self.info = "no useful files found"


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
        Window.clearcolor = (0.2, 0.2, 0.2, 1)
        return Faces()


if __name__ == '__main__':
    InterfaceApp().run()
