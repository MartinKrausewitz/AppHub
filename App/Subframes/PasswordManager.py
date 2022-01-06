import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from tkinter import filedialog as fd
from tkinter import messagebox as mb

from App.Main import stdframe as st
from App.Utility import EncryptDecrypt as ED
from App.Utility import tkinterDisplayKeys as dk
from App.Utility import settingsloader as sett

import shutil
import os
import json

# todo add backup

class PasswordManagerFrame(st.stdFrame):
    def __init__(self, container):
        super().__init__(container)
        # get app path
        pwddir = os.path.abspath(os.path.join(os.path.dirname("AppHub"), ".."))
        pwddir = os.path.join(pwddir, "data")
        pwddir = os.path.join(pwddir, "pwmanager")
        self.datadir = pwddir
        # settingsloader
        settingsfile = os.path.join(pwddir, "settings.set")
        self.sl = sett.SettingsLoader(settingsfile, pwddir, "general")
        # look if maintable file exists
        self.initialized = True
        if not os.path.exists(os.path.join(pwddir, "maintable")):
            self.initialized = False
        # init encryptor/decryptor
        self.enc = ED.EncryptDecrypt(pwddir)
        # variables: data stores dict |  topbutton stores topbutton | framearray stores frames
        self.data = ""
        self.topbutton = ""
        self.framearray = []
        self.allowchange = True

        # init style and adding styles
        self.style = ttk.Style()
        self.defstyle()

        self.mainfile = "maintable"

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
        col1 = self.sl.getbykey("appearance", "col1")
        col2 = self.sl.getbykey("appearance", "col2")
        self.style.configure("1.TFrame", background=col1)
        self.style.configure("1.TLabel", background=col1)
        self.style.configure("1.TButton", background=col1, foreground=col1)
        self.style.configure("0.TFrame", background=col2)
        self.style.configure("0.TLabel", background=col2)
        self.style.configure("0.TButton", background=col2, foreground=col2)

    # initial interaction needed for starting here requests password or setting a new one
    def requestInfo(self):
        if (self.initialized == False):
            self.initprocess()
            return
        print("start")
        pfalse = True
        while (pfalse):
            p = simpledialog.askstring(self.sl.lanbykey("pw"), self.sl.lanbykey("enterpw"), show="*")
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
        p1 = simpledialog.askstring(self.sl.lanbykey("pw"), self.sl.lanbykey("newpw"), show="*")
        p2 = simpledialog.askstring(self.sl.lanbykey("pw"), self.sl.lanbykey("againpw"), show="*")
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
        self.topbutton = TopButtons(self)
        self.topbutton.grid(row=0, column=0, sticky="w")
        self.displaypwd()

    # displays the passwords
    def displaypwd(self):
        firstfree = int(self.data["counter"])
        for i in range(1,firstfree):
            self.framearray.append(subframe(self.data, i, self, 1000, self.sl))
            self.framearray[i - 1].grid(row=i, column=0)

    # displays an item
    def displayitem(self, id):
        window = dk.keyDisplay(self, self.data[str(id)])
        window.grab_set()

    # make backup
    def makebac(self):
        file = fd.asksaveasfilename(defaultextension=".bac")
        if file is None:
            return

        p1 = simpledialog.askstring(self.sl.lanbykey("pw"), self.sl.lanbykey("newpw"), show="*")
        p2 = simpledialog.askstring(self.sl.lanbykey("pw"), self.sl.lanbykey("againpw"), show="*")

        if p1 is None or p2 is None:
            return

        if not p1 == p2:
            self.makebac()
            return
        kzw = self.enc.getrawkey()
        self.enc.setNewKey(p1)
        d = self.enc.encryptDict(self.data)
        self.enc.writeFileByPath(file, d[0], d[1], d[2])
        self.enc.setrawkey(kzw)
        pass

    # load backup
    def loadbac(self):
        file = fd.askopenfilename(defaultextension=".bac")
        if file is None:
            return
        p = simpledialog.askstring(self.sl.lanbykey("pw"), self.sl.lanbykey("enterpw"), show="*")
        if p is None:
            return
        self.enc.setNewKey(p)
        self.data = json.loads(str(self.enc.decrytFileByPath(file),"utf-8"))
        s = mb.askquestion(self.sl.lanbykey("conf"), self.sl.lanbykey("overorshow"))
        if s == "yes":
            self.allowchange = False
        elif s == "no":
            self.secbac()
            self.encdicandsave()
        else:
            return
        self.update()

    # automatic security backup
    def secbac(self):
        # find filename
        src = os.path.join(self.datadir, self.mainfile)
        basename = "securitybackup"
        filenamefound = False
        i = 0
        while not filenamefound:
            name = basename + str(i) + ".bac"
            tmppath = os.path.join(self.datadir, name)
            if not os.path.exists(tmppath):
                filenamefound = True
                shutil.copy(src, tmppath)
            i = i + 1

    # export to arduino password manager
    def exptoapm(self):
        # todo: password
        # todo: file dialog
        pass

    def chpw(self):
        if not self.allowchange:
            return

        p1 = simpledialog.askstring(self.sl.lanbykey("pw"), self.sl.lanbykey("newpw"), show="*")
        p2 = simpledialog.askstring(self.sl.lanbykey("pw"), self.sl.lanbykey("againpw"), show="*")

        if p1 is None or p2 is None:
            return

        if not p1 == p2:
            self.chpw()
            return
        self.enc.setNewKey(p1)
        self.encdicandsave()

    # adds an entry to the dictionary
    def add(self):
        if not self.allowchange:
            return

        firstfree = self.data["counter"]
        entry = dict()
        key = ""
        keyvalue = simpledialog.askstring(self.sl.lanbykey("ename"), self.sl.lanbykey("entryname"))
        if keyvalue is None:
            return
        entry["name"] = keyvalue
        while True:
            key = simpledialog.askstring(self.sl.lanbykey("kword"), self.sl.lanbykey("keyword"))
            if key is None:
                break
            keyvalue = simpledialog.askstring(self.sl.lanbykey("kwvalue"), self.sl.lanbykey("keywordvalue"))
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
        if not self.allowchange:
            return

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
        with open(os.path.join(self.datadir, "settingsblueprint.set"), "r") as f:
            return json.loads(f.read())

    # returns the setiingsdict saved as blueprint
    def getcurrentsettingdic(self):
        if os.path.exists(os.path.join(self.datadir, "settings.set")):
            with open(os.path.join(self.datadir, "settings.set"), "r") as f:
                return json.loads(f.read())
        with open(os.path.join(self.datadir, "stdsettings.set"), "r") as f:
            return json.loads(f.read())

    def getsettingspath(self):
        return os.path.join(self.datadir, "settings.set")


class subframe(ttk.Frame):
    def __init__(self, data, i, master, width, lan):
        super().__init__(master, style=str(i % 2) + ".TFrame")
        t1 = (int(0.1*width),int(0.3*width))      # padding of Label (right, left)
        t2 = (int(0.05*width),int(0.05*width))    # padding of Button (right, left)
        t3 = (int(0.05*width),int(1.5*width))    # padding of Button (right, left)
        stylelable = str(i%2)+".TLabel"     # 0.TLabel|1.TLabel
        stylebutton = str(i%2)+".TButton"   # 0.TButton|1.TButton
        noc = 10 #number of characters
        ttk.Label(self, text=data[str(i)]["name"], style=stylelable, width=noc).grid(row=0, column=0, padx=t1)
        ttk.Button(self, text=lan.lanbykey("dis"), command=lambda c=i: master.displayitem(c), style=stylebutton, width=noc).grid(row=0, column=1, padx=t2)
        ttk.Button(self, text=lan.lanbykey("rem"), command=lambda c=i: master.removeentry(c), style=stylebutton, width=noc).grid(row=0, column=2, padx=t3)

class TopButtons(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.topbutton = []
        # add an entry
        self.topbutton.append(ttk.Button(self,text=master.sl.lanbykey("addentry"), command=master.add))
        # make backup
        self.topbutton.append(ttk.Button(self,text=master.sl.lanbykey("makebac"), command=master.makebac))
        # load backup
        self.topbutton.append(ttk.Button(self,text=master.sl.lanbykey("loadbac"), command=master.loadbac))
        # change password
        self.topbutton.append(ttk.Button(self,text=master.sl.lanbykey("changepw"), command=master.chpw))
        # export to arduino password manager
        self.topbutton.append(ttk.Button(self,text=master.sl.lanbykey("exportapm"), command=master.exptoapm))
        for i in range(0, len(self.topbutton)):
            self.topbutton[i].grid(row=0, column=i)


