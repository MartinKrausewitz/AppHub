import tkinter as tk
from tkinter import ttk
from tkinter import Tk
import copy

class keyDisplay(tk.Toplevel):
    def __init__(self, parent, keydict):
        super().__init__(parent)
        self.title(keydict["name"])
        key = keydict.keys()
        i = 0
        for x in key:
            if x == "name":
                continue
            ttk.Label(self, text=x).grid(row=i, column=0)
            ttk.Label(self, text=keydict[x]).grid(row=i, column=1)
            ttk.Button(self, text="In Zwischenablage kopieren", command=lambda v=x:self.copytoclipboard(keydict[v])).grid(row=i, column=2)
            i += 1

    def copytoclipboard(self, s):
        r = Tk()
        r.withdraw()
        r.clipboard_clear()
        r.clipboard_append(s)
        r.update()
        r.destroy()
