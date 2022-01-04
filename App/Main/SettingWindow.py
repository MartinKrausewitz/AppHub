import tkinter as tk
from tkinter import ttk
import json


class SettingWindow(tk.Toplevel):
    def __init__(self, parent, settings, stdsettings, path):
        super().__init__(parent)
        if type(settings) is not dict:
            self.destroy()
        # todo left frame
        self.leftframe = leftframe(self, settings.keys())
        self.leftframe.grid(row=0, column=0)
        # todo right frame
        self.rigthframe = rigthframe(self, settings, stdsettings, path)
        self.rigthframe.grid(row=0, column=1)
        self.leftframe.setlink(self.rigthframe)


class leftframe(ttk.Frame):
    def __init__(self, master, ar):
        super().__init__(master)
        self.buttonlist = []
        self.link = None
        i = 0
        for x in ar:
            self.buttonlist.append(ttk.Button(self, text=x, command=lambda c=x: self.changewidow(c)))
            self.buttonlist[i].grid(row=i, column=0)
            i += 1

    def setlink(self, l):
        self.link = l

    def changewidow(self, c):
        if self.link is None:
            return
        self.link.setkey(c)

class rigthframe(ttk.Frame):
    def __init__(self, master, dict, std, path):
        super().__init__(master)
        self.data = dict
        self.stdsettings = std
        self.path = path

        self.llist = []
        self.elist = []
        self.stringvars = []

        self.savebutton = ""

    def setkey(self, key):
        self.remall()
        for x in self.data[key].keys():
            self.llist.append(ttk.Label(self, text=x))
            print(x)
            value = self.data[key][x]
            print(self.stdsettings[key][x])
            if value[0] == "[" and value[len(value) - 1] == "]":
                ar = eval(value)
                print(ar)
                self.stringvars.append(tk.StringVar(self))
                index = len(self.stringvars) - 1
                self.elist.append(ttk.OptionMenu(self, self.stringvars[index], self.stdsettings[key][x], *ar))
            else:
                self.elist.append(ttk.Entry(self))
                self.elist[len(self.elist) - 1].insert("1", self.stdsettings[key][x])
        z = 0
        for i in range(0, len(self.elist)):
            self.llist[i].grid(row=i, column=0)
            self.elist[i].grid(row=i, column=1)
            z += 1
        self.savebutton = ttk.Button(self, text="save", command=lambda : self.save(key))
        self.savebutton.grid(row=z, column=0)

    def remall(self):
        for i in range(0, len(self.elist)):
            self.llist[i].destroy()
            self.elist[i].destroy()
        self.llist = []
        self.elist = []

    def save(self, key):
        newdic = self.stdsettings.copy()
        i = 0
        countop = 0
        for x in newdic[key].keys():
            if type(self.elist[i]) == ttk.OptionMenu:
                value = self.stringvars[countop].get()
                countop += 1
            else:
                value = self.elist[i].get()
            newdic[key][x] = value
            i += 1
        print(newdic)
        with open(self.path, "w") as f:
            f.write(json.dumps(newdic))


