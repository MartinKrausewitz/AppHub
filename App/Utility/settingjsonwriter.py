import os
import json

isrunning = True
setting = dict()
sub = None

# get app path
pwdir = ""
pwddir = os.getcwd()

while isrunning:
    a = input()
    if a == "exit":
        isrunning = False
    if a == "print":
        print(setting)
    if a == "printpath":
        print(pwdir)
    if a == "goback":
        pwdir = os.path.dirname(pwdir)
    ar = a.split(" ")
    if ar[0] == "addsub":
        s = dict()
        setting[ar[1]] = s
    if ar[0] == "setsub":
        sub = ar[1]
    if ar[0] == "addset":
        if sub is None:
            continue
        setting[sub][ar[1]] = ar[2]
    if ar[0] == "join":
        pwdir = os.path.join(pwdir, ar[1])
    if ar[0] == "save":
        savedir = os.path.join(pwdir, ar[1])
        print(savedir)
        with open(savedir, "w") as f:
            f.write(json.dumps(setting))
    if ar[0] == "setpath":
        pwdir = ar[1]
    if ar[0] == "load":
        loaddir = os.path.join(pwdir, ar[1])
        with open(loaddir, "r") as f:
            setting = json.loads(f.read())




