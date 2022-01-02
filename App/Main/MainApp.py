import tkinter as tk
from tkinter import ttk
from App.Main import stdframe as st
from App.Main import SettingWindow as sett

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        # title
        self.title("Main")
        # frame array
        self.frame = []
        # height and width
        width = self.winfo_screenwidth()
        heigth = self.winfo_screenheight()
        sizex = 300
        sizey = 300
        self.newgeometry = str(sizex) + "x" + str(sizey) + "+" + str(int(width/2) - int(sizex/2)) + "+" + str(int(heigth/2) - int(sizey/2))
        self.geometry(self.newgeometry)
        # menubar
        self.menubar = tk.Menu(self)
        self.config(menu=self.menubar)
        # file menu
        self.filemenu = tk.Menu(self.menubar, tearoff=False)
        # add command
        self.filemenu.add_command(label="Quit", command=self.destroy)
        # add file menu to menubar
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        # frame menu
        self.framemenu = tk.Menu(self.menubar, tearoff=False)
        # add command
        self.filemenu.add_command(label="Settings", command=self.changesett)
        # add frame menu to menubar
        self.menubar.add_cascade(label="Frame", menu=self.framemenu)
        # mainframe
        self.mainframe = None
        self.showframe(st.stdFrame)

    def addFrame(self, addingframe):
        if not issubclass(addingframe, ttk.Frame):
            return
        self.frame.append(addingframe)
        self.framemenu.add_command(label="Show " + addingframe.returntitle(), command=lambda: self.showframe(addingframe))
        self.framemenu.update()

    def showframe(self, targetframe):
        if self.mainframe is not None:
            self.mainframe.destroy()
        self.mainframe = targetframe(self)
        self.mainframe.requestInfo()
        self.mainframe.initdisplay()
        self.geometry(self.mainframe.newgeometry)

    def changesett(self):
        if self.mainframe is None:
            return
        d = self.mainframe.getsettingdic()
        print(d)
        settingwindow = sett.SettingWindow(self, d)
