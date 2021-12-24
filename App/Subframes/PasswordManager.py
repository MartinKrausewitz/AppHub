import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog

from App.Main import stdframe as st
from App.Utility import EncryptDecrypt as ED
from App.Utility import tkinterDisplayKeys as dk
import os
import json

class PasswordManagerFrame(st.stdFrame):
    def __init__(self, container):
        super().__init__(container)

        pwddir = os.path.abspath(os.path.join(os.path.dirname("AppHub"), ".."))
        pwddir = os.path.join(pwddir, "data")
        self.initialized = True
        if not os.path.exists(os.path.join(pwddir, "maintable")):
            self.initialized = False
        self.enc = ED.EncryptDecrypt(pwddir)
        self.data = ""
        self.labellist = []
        self.buttonlistdisplay = []
        self.buttonlistremove = []
        self.topbutton = []

    @staticmethod
    def returntitle():
        return "PasswortManager"

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

    def initprocess(self):
        p1 = simpledialog.askstring("Passwort", "Bitte geben Sie ein Passwort ein", show="*")
        p2 = simpledialog.askstring("Passwort", "Bitte geben Sie daselbe Passwort erneut ein", show="*")
        if not p1 == p2:
            self.initprocess()
            return
        self.enc.setNewKey(p1)
        begintable = dict()
        begintable["counter"] = "1"
        retval = self.enc.encryptDict(begintable)
        print(begintable)
        print(retval)
        self.enc.writeFile("maintable", retval[0], retval[1], retval[2])
        self.initialized = True

    def initdisplay(self):
        if type(self.data) is not dict:
            return
        self.topbutton.append(ttk.Button(self,text="Passwort hinzufügen", command=self.add))
        for i in range(0, len(self.topbutton)):
            self.topbutton[i].grid(row=0, column=i)
        self.displaypwd()

    def displaypwd(self):
        firstfree = int(self.data["counter"])
        for i in range(1,firstfree):
            self.labellist.append(ttk.Label(self, text=self.data[str(i)]["name"]))
            self.labellist[i - 1].grid(row=i, column=0)
            self.buttonlistdisplay.append(ttk.Button(self, text="Display", command=lambda c=i:self.displayitem(c)))
            self.buttonlistdisplay[i - 1].grid(row=i, column=1)
            self.buttonlistremove.append(ttk.Button(self, text="Remove", command=lambda c=i:self.removeentry(c)))
            self.buttonlistremove[i - 1].grid(row=i, column=2)

    def displayitem(self, id):
        window = dk.keyDisplay(self, self.data[str(id)])
        window.grab_set()

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

    def encdicandsave(self):
        d = self.enc.encryptDict(self.data)
        self.enc.writeFile("maintable", d[0], d[1], d[2])

    def removeentry(self, id):
        self.data.pop(str(id))
        for i in range(id, int(self.data["counter"]) - 1):
            self.data[str(i)] = self.data[str(i + 1)]
            self.data.pop(str(id + 1))

        self.data["counter"] = str(int(self.data["counter"]) - 1)
        self.encdicandsave()
        self.update()

    def update(self):
        for i in range(0, len(self.buttonlistdisplay)):
            self.buttonlistdisplay[i].destroy()
            self.buttonlistremove[i].destroy()
            self.labellist[i].destroy()
        self.displaypwd()

