"""
Python game using the tkinter - Bejeweled

@author Vladyslav Bochok
"""

from tkinter import *
from Mediator import Mediator


def config_root():
    master = Tk()
    master.title("Bejeweled")
    master.geometry('404x295')
    master.resizable(False, False)
    return master


if __name__ == '__main__':
    root = config_root()
    mediator = Mediator(root)
    mediator.show_menu()
    root.mainloop()
