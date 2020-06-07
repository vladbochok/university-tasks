from tkinter import Tk

import Mediator
from Controller.BoardController import BoardController


class GameComponent:
    """
    Сlass that creates game settings
    turns on and off the display of game events
    created for flexible distribution of tasks between other classes
    """
    _BOARD_ROW = 8
    _BOARD_COLUMN = 8

    def __init__(self, root:Tk, mediator:Mediator):
        self._root = root
        self._mediator = mediator
        self._boardController = BoardController(root, self._BOARD_ROW, self._BOARD_COLUMN, mediator)

    def start_new_game(self):
        """destroys previous game settings, creates a new script"""
        self._boardController.destroy()
        self._boardController = BoardController(self._root, self._BOARD_ROW, self._BOARD_COLUMN, self._mediator)

    def show(self):
        self._boardController.draw()

    def hide(self):
        self._boardController.hide()
