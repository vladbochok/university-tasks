from tkinter import *

import Mediator
from Model.BoardModel import BoardModel
from View.BoardView import BoardView
from Controller.GemController import GemController
from random import randint
from Handler import Handler


class BoardController:
    """
    The main class that is responsible for the board.
    The functions of the class work both on the graphical interface and on the logical part.

    Creates classes BoardModel, BoardView and controls them from the outside.
    """
    _BOARD_HEIGHT = 288
    _BOARD_WIDTH = 288
    _BACKGROUND_COLOR = "blue"
    _GEM_TYPE_MIN_VALUE = 1
    _GEM_TYPE_MAX_VALUE = 7

    def __init__(self, root: Tk, width: int, height: int, mediator: Mediator):
        """
        initializes the canvas for further work with it.
        creates instances of Board classes.
        Generates the correct random playing field
        """
        self._root = root
        self._width = width
        self._height = height

        self._create_canvas()
        self._score_points = 0

        self.board_model = BoardModel(width, height)
        self._board_view = BoardView(root, width, height, self._canvas, mediator)

        self._control = Handler(self)
        self._set_random_board()

    def draw(self):
        """shows graphic elements"""
        self._board_view.draw_board()

    def hide(self):
        """hides graphic elements"""
        self._board_view.hide_board()

    def swap_gems(self, gem1, gem2):
        """"Replaces gems, removes steaks and updates statistics"""
        self.board_model.swap_gems(gem2, gem1)
        self._update_points()

    def _update_points(self):
        self._score_points = self.board_model.get_points()  # receives data processing
        self._board_view.update_score(self._score_points)

    def _create_canvas(self):
        self._canvas = Canvas(self._root, background=self._BACKGROUND_COLOR, width=self._BOARD_WIDTH,
                              height=self._BOARD_HEIGHT, relief=SOLID, borderwidth=2)

    def _set_gem(self, row, column, gem_controller):
        self.board_model.set_gem(row, column, gem_controller)
        self._board_view.set_gem(row, column, gem_controller)

    def _set_random_board(self):
        for i in range(self._width):
            for j in range(self._height):
                rand_type = self._get_random_gem_type()
                gem_controller = GemController(self._root, rand_type, i, j, self._control, self._canvas)
                self._set_gem(i, j, gem_controller)  # uses a random stone to initialize the field

        self.board_model.fix_board()  # removes groups of gems more than 3

    def _get_random_gem_type(self):
        return randint(self._GEM_TYPE_MIN_VALUE, self._GEM_TYPE_MAX_VALUE)

    def destroy(self):
        """cleans and destroys the game board"""
        self._canvas.destroy()
