from tkinter import *

from Controller import GemController


class BoardView:
    """
    The class responsible for the graphical representation of the playing field.
    Visualizes the menu in the game.
    """
    _BACKGROUND_MENU_COLOR = "#DADEEB"
    _MENU_BUTTON_SIZE = 12

    def __init__(self, root, width, height, canvas, mediator):
        self._root = root
        self._width = width
        self._height = height
        self._canvas = canvas
        self._mediator = mediator
        self._score_point = 0
        self._create_board()
        self._create_menu()
        self._draw_menu()

    def draw_board(self):
        self._canvas.grid(row=0, column=0, rowspan=self._height)

    def hide_board(self):
        self._canvas.grid_forget()

    def set_gem(self, row: int, column: int, gem_controller: GemController):
        self.gems[row][column] = gem_controller

    def update_score(self, score_point: int):
        """updates and displays game points"""
        self._score_point = score_point
        self._update_score()  # change the visual display of points for the player

    def _create_board(self):
        self.gems = [[0] * self._height for _ in range(self._width)]  # initializes a two-dimensional array

    def _create_menu(self):
        # creates elements for display on the canvas
        self._score_label = Label(self._root, text=f"Score: {self._score_point}", bg=self._BACKGROUND_MENU_COLOR,
                                  font='Helvetica 10 bold')
        self._main_menu = Button(self._root, text=f"Menu", bg=self._BACKGROUND_MENU_COLOR, font='Helvetica 10 bold',
                                 width=self._MENU_BUTTON_SIZE,
                                 command=self._mediator.show_menu)
        self._new_game = Button(self._root, text=f"New game", bg=self._BACKGROUND_MENU_COLOR, font='Helvetica 10 bold',
                                width=self._MENU_BUTTON_SIZE,
                                command=self._mediator.start_new_game)
        self._quit = Button(self._root, text=f"Quit", bg=self._BACKGROUND_MENU_COLOR, font='Helvetica 10 bold',
                            width=self._MENU_BUTTON_SIZE,
                            command=self._mediator.quit)

    def _draw_menu(self):
        self._score_label.grid(row=0, column=2)
        self._main_menu.grid(row=1, column=2)
        self._new_game.grid(row=2, column=2)
        self._quit.grid(row=7, column=2)

    def _update_score(self):
        self._score_label["text"] = f"Score: {self._score_point}"
