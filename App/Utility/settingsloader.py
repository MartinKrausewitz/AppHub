import json
import os


class SettingsLoader:
    def __init__(self, file, landir, lankey):
        with open(file, "r") as f:
            self.settings = json.loads(f.read())
        with open(os.path.join(landir, self.settings[lankey]["lan"] + ".lan")) as f:
            self.landir = json.loads(f.read())

    def getbykey(self, sub, key):
        return self.settings[sub][key]

    def lanbykey(self, key):
        return self.landir[key]
