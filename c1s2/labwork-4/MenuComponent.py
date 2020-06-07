from tkinter import *

import Mediator


class MenuComponent:
    """
    Create simple Menu GUI.
    delegates the work of the logic buttons of the class to the Mediator.
    """
    _BUTTON_SIZE = 30
    _BACKGROUND_COLOR = '#DADEEB'
    _FRONT_IMAGE = "images/icon.png"

    def __init__(self, root: Tk, mediator: Mediator):
        self._root = root
        self._mediator = mediator
        self._img = PhotoImage(file=self._FRONT_IMAGE)
        self._create_button()

    def show(self):
        """Configures and displays the main menu."""
        self._root.configure(background=self._BACKGROUND_COLOR)
        self._show_button()

    def hide(self):
        """Hides all menu items, leaves the specified background."""
        self._hide_button()

    def _create_button(self):
        self._title = Label(self._root, text="Bejeweled", bg="#DADEEB", font='Helvetica 20 bold')
        self._imgLabel = Label(self._root, bg=self._BACKGROUND_COLOR, image=self._img)
        self._startButton = Button(self._root, text="Play",
                                   font='Helvetica 12 bold', width=self._BUTTON_SIZE, command=self._command_start)
        self._quitButton = Button(self._root, text="Quit", font='Helvetica 10 bold',
                                  fg="black", width=self._BUTTON_SIZE, command=self._command_quit)

    def _show_button(self):
        width, height = self._get_size()
        pad_x = width / 2 - self._BUTTON_SIZE * 5  # get central x coordinates

        self._title.grid(row=0, column=0, sticky=E + W, pady=10, padx=pad_x)
        self._imgLabel.grid(row=1, column=0, rowspan=3, sticky=E + W, pady=10, padx=pad_x)
        self._startButton.grid(row=5, column=0, sticky=E + W, pady=10, padx=pad_x)
        self._quitButton.grid(row=6, column=0, sticky=E + W, pady=10, padx=pad_x)

    def _hide_button(self):
        self._title.grid_forget()
        self._imgLabel.grid_forget()
        self._startButton.grid_forget()
        self._quitButton.grid_forget()

    def _get_size(self):
        self._root.update() # updates the window data
        return self._root.winfo_width(), self._root.winfo_height()

    def _command_start(self):
        self._mediator.show_game()

    def _command_quit(self):
        self._mediator.quit()
