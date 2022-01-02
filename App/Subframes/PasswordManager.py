import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog

from App.Main import stdframe as st
from App.Utility import EncryptDecrypt as ED
from App.Utility import tkinterDisplayKeys as dk
import os
import json

# todo implement language
# todo add backup
# todo setting window

class PasswordManagerFrame(st.stdFrame):
    def __init__(self, container):
        super().__init__(container)
        # get app path
        pwddir = os.path.abspath(os.path.join(os.path.dirname("AppHub"), ".."))
        print(pwddir)
        pwddir = os.path.join(pwddir, "data")
        pwddir = os.path.join(pwddir, "pwmanager")
        self.datadir = pwddir
        # look if maintable file exists
        self.initialized = True
        if not os.path.exists(os.path.join(pwddir, "maintable")):
            self.initialized = False
        # init encryptor/decryptor
        self.enc = ED.EncryptDecrypt(pwddir)
        # variables: data stores dict |  topbutton stores topbutton | framearray stores frames
        self.data = ""
        self.topbutton = []
        self.framearray = []

        # init style and adding styles
        self.style = ttk.Style()
        self.defstyle()

        # geometry init
        width = self.winfo_screenwidth()
        heigth = self.winfo_screenheight()
        sizex = 1000
        sizey = 500
        self.newgeometry = str(sizex) + "x" + str(sizey) + "+" + str(int(width/2) - int(sizex/2)) + "+" + str(int(heigth/2) - int(sizey/2))

    # returns the name of the frame and subapp
    @staticmethod
    def returntitle():
        return "PasswortManager"

    # adding the style
    def defstyle(self):
        self.style.configure("1.TFrame", background="#99A4AA")
        self.style.configure("1.TLabel", background="#99A4AA")
        self.style.configure("1.TButton", background="#99A4AA", foreground="#99A4AA")
        self.style.configure("0.TFrame", background="#99CCCC")
        self.style.configure("0.TLabel", background="#99CCCC")
        self.style.configure("0.TButton", background="#99CCCC", foreground="#99CCCC")

    # initial interaction needed for starting here requests password or setting a new one
    def requestInfo(self):
        if (self.initialized == False):
            self.initprocess()
            return
        print("start")
        pfalse = True
        while (pfalse):
            p = simpledialog.askstring("Passwort", "Bitte geben sie ein Passwort ein", show="*")
            try:
                self.enc.setNewKey(p)
            except AttributeError:
                return
            try:
                self.data = json.loads(str(self.enc.decryptFile("maintable"), "utf-8"))
                print(self.data)
                pfalse = False
            except TypeError:
                print("Wrong Password")
                continue
            except UnicodeDecodeError:
                print("Wrong Password, could not Decode")
                continue
            except Exception as e:
                print("Error" + e)
                continue

    # process for the first setup
    def initprocess(self):
        p1 = simpledialog.askstring("Passwort", "Bitte geben Sie ein Passwort ein", show="*")
        p2 = simpledialog.askstring("Passwort", "Bitte geben Sie daselbe Passwort erneut ein", show="*")
        if not p1 == p2:
            self.initprocess()
            return
        self.enc.setNewKey(p1)
        self.data = dict()
        self.data["counter"] = "1"
        self.encdicandsave()
        self.initialized = True

    # setting up the top buttons
    def initdisplay(self):
        # looks if data is a dictionary
        if type(self.data) is not dict:
            return
        # topbuttons actually only the add button
        self.topbutton.append(ttk.Button(self,text="Passwort hinzufügen", command=self.add))
        for i in range(0, len(self.topbutton)):
            self.topbutton[i].grid(row=0, column=i)
        self.displaypwd()

    # displays the passwords
    def displaypwd(self):
        firstfree = int(self.data["counter"])
        for i in range(1,firstfree):
            self.framearray.append(subframe(self.data, i, self, 1000))
            self.framearray[i - 1].grid(row=i, column=0)

    # displays an item
    def displayitem(self, id):
        window = dk.keyDisplay(self, self.data[str(id)])
        window.grab_set()

    # adds an entry to the dictionary
    def add(self):
        firstfree = self.data["counter"]
        entry = dict()
        key = ""
        keyvalue = simpledialog.askstring("Eintragsname", "Geben sie diesem Eintrag einen Namen:")
        if keyvalue is None:
            return
        entry["name"] = keyvalue
        while True:
            key = simpledialog.askstring("Schlüsselwort", "Geben sie ein Schlüsselwort ein:")
            if key is None:
                break
            keyvalue = simpledialog.askstring("Schlüsselwortwert", "Geben sie ein Wert ein, der ihrem Schlüsselwort zugeordent wird:")
            if key is None:
                continue
            entry[key] = keyvalue
        self.data[firstfree] = entry
        self.data['counter'] = str(int(firstfree)+1)
        self.encdicandsave()
        self.update()
        print(self.data)

    # encrypts the dictionary and saves it
    def encdicandsave(self):
        d = self.enc.encryptDict(self.data)
        self.enc.writeFile("maintable", d[0], d[1], d[2])

    # removes and entry from the dictionary then encrypts it and saves it
    def removeentry(self, id):
        self.data.pop(str(id))
        for i in range(id, int(self.data["counter"]) - 1):
            self.data[str(i)] = self.data[str(i + 1)]
            self.data.pop(str(id + 1))

        self.data["counter"] = str(int(self.data["counter"]) - 1)
        self.encdicandsave()
        self.update()

    # updates the interfaces removes existing frames and setts up new ones
    def update(self):
        for i in range(0, len(self.framearray)):
            self.framearray[i].destroy()
        self.framearray = []
        self.displaypwd()

    # returns the setiingsdict saved as blueprint
    def getsettingdic(self):
        with open(os.path.join(self.datadir, "settingsblueprint"), "r") as f:
            return json.loads(f.read())

    # returns the setiingsdict saved as blueprint
    def getstdsettingdic(self):
        with open(os.path.join(self.datadir, "stdsettings"), "r") as f:
           return json.loads(f.read())


class subframe(ttk.Frame):
    def __init__(self, data, i, sup, width):
        super().__init__(sup, style=str(i%2)+".TFrame")
        t1 = (int(0.1*width),int(0.3*width))      # padding of Label (right, left)
        t2 = (int(0.05*width),int(0.05*width))    # padding of Button (right, left)
        stylelable = str(i%2)+".TLabel"     # 0.TLabel|1.TLabel
        stylebutton = str(i%2)+".TButton"   # 0.TButton|1.TButton
        noc = 10 #number of characters
        ttk.Label(self, text=data[str(i)]["name"], style=stylelable, width=noc).grid(row=0, column=0, padx=t1)
        ttk.Button(self, text="Display", command=lambda c=i: sup.displayitem(c), style=stylebutton, width=noc).grid(row=0, column=1, padx=t2)
        ttk.Button(self, text="Remove", command=lambda c=i: sup.removeentry(c), style=stylebutton, width=noc).grid(row=0, column=2, padx=t2)

