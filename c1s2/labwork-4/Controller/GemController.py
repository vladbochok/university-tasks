from tkinter import *

import Handler
from View.GemView import GemView
from Model.GemModel import GemModel
from random import randint


class GemController:
    """"
    Basic class that describes gems.
    Includes graphical representation classes and models to which it delegates operations
    Included in the classes of the Board as a structural unit
    """
    _TYPE_EMPTY_VALUE = 0
    _TYPE_MIN_VALUE = 1
    _TYPE_MAX_VALUE = 7

    def __init__(self, root: Tk, type: int, row: int, column: int, handler: Handler, canvas: Canvas):
        self.root = root
        self.type = type
        self.row = row
        self.column = column

        self.gem_model = GemModel(type, row, column)
        self.gem_view = GemView(root, type, row, column, handler, canvas)

    def set_type(self, type):
        self.type = type
        self.gem_model.set_type(type)
        self.gem_view.set_type(type)

    def set_empty_type(self):
        """changes the type of heme to zero, which describes the absence of gem"""
        self.set_type(self._TYPE_EMPTY_VALUE)

    def set_random_type(self):
        random_type = randint(self._TYPE_MIN_VALUE,
                              self._TYPE_MAX_VALUE)  # selects a random number within a sample of types
        self.set_type(random_type)

    def is_empty(self) -> bool:
        return self.type == self._TYPE_EMPTY_VALUE

    def swap(self, other, animation_speed):
        row1, column1 = other.row, other.column
        row2, column2 = self.row, self.column

        self.set_row_and_column(row1, column1, animation_speed)
        other.set_row_and_column(row2, column2, animation_speed)

    def set_row_and_column(self, row, column, animation_speed):
        self.row = row
        self.column = column
        self.gem_model.set_row_and_column(row, column)
        self.gem_view.set_row_and_column(row, column, animation_speed)

    def __eq__(self, other):
        return isinstance(other, GemController) and self.type == other.type
