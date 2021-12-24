from Main import MainApp as ma
from Main import stdframe as std
from Subframes import PasswordManager as pwd

if __name__ == "__main__":
    app = ma.MainApp()
    app.addFrame(pwd.PasswordManagerFrame)
    app.mainloop()