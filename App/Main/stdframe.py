import tkinter as tk
from tkinter import ttk


class stdFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.grid(row=0, column=0)

        width = self.winfo_screenwidth()
        heigth = self.winfo_screenheight()
        sizex = 300
        sizey = 300
        self.newgeometry = str(sizex) + "x" + str(sizey) + "+" + str(int(width/2) - int(sizex/2)) + "+" + str(int(heigth/2) - int(sizey/2))

    @staticmethod
    def returntitle():
        return "stdframe"

    def requestInfo(self):
        pass

    def initdisplay(self):
        self.label = ttk.Label(self, text="This is the standard Frame")
        self.label.pack()

    def getsettingdic(self):
        return dict()
    def getcurrentsettingdic(self):
        return dict()
    def getsettingspath(self):
        return None