from tkinter import *
from MenuComponent import MenuComponent
from GameComponent import GameComponent


class Mediator:
    """
    Additional class that changes the state of the home screen,
    and delegates work to the following classes:

    GameComponent, MenuComponent
    """
    def __init__(self, root: Tk):
        self._root = root
        self._game = GameComponent(root, self)
        self._menu = MenuComponent(root, self)

    def start_new_game(self):
        """Clears the screen and creates a new playing field."""
        self._game.start_new_game()
        self.show_game()

    def show_game(self):
        """Shows the current playing field."""
        self._menu.hide()
        self._game.show()

    def show_menu(self):
        """Changes the game scene."""
        self._game.hide()
        self._menu.show()

    def quit(self):
        """Closes the main process."""
        self._root.destroy()
