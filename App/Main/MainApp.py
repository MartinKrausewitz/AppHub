import tkinter as tk
from tkinter import ttk
from App.Main import stdframe as st

class MainApp(tk.Tk):
    frame = []

    def __init__(self):
        super().__init__()
        self.title("Main")
        width = self.winfo_screenwidth()
        heigth = self.winfo_screenheight()
        sizex = 300
        sizey = 300
        self.newgeometry = str(sizex) + "x" + str(sizey) + "+" + str(int(width/2) - int(sizex/2)) + "+" + str(int(heigth/2) - int(sizey/2))
        self.geometry(self.newgeometry)
        self.menubar = tk.Menu(self)
        self.config(menu=self.menubar)
        self.filemenu = tk.Menu(self.menubar, tearoff=False)
        self.filemenu.add_command(label="Quit", command=self.destroy)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.mainframe = None
        self.showframe(st.stdFrame)

    def addFrame(self, addingframe):
        if not issubclass(addingframe, ttk.Frame):
            return
        self.frame.append(addingframe)
        self.filemenu.add_command(label="Show " + addingframe.returntitle(),
                                  command=lambda: self.showframe(addingframe))
        self.filemenu.update()

    def showframe(self, targetframe):
        if self.mainframe != None:
            self.mainframe.destroy()
        self.mainframe = targetframe(self)
        self.mainframe.requestInfo()
        self.mainframe.initdisplay()
        self.geometry(self.mainframe.newgeometry)
