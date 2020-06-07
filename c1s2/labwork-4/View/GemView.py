from tkinter import *

import Handler


class GemView:
    """
    A class that represents a graphical representation of gems
    Saves and displays images
    Performs a click response from the user
    """
    _SIZE_IMAGE = 32
    _MOVE_ANIMATION_DELAY = 5
    _IMG_GEM_FROM_TYPE = {
        0: ["images/gem0.gif", None],
        1: ["images/gem1.gif", None],
        2: ["images/gem2.gif", None],
        3: ["images/gem3.gif", None],
        4: ["images/gem4.gif", None],
        5: ["images/gem5.gif", None],
        6: ["images/gem6.gif", None],
        7: ["images/gem7.gif", None]
    }

    def __init__(self, root: Tk, type: int, row: int, column: int, handler: Handler, canvas: Canvas):
        self.root = root
        self.control = handler
        self.canvas = canvas
        self.type = type
        self.row = row
        self.column = column

        self._create_item()
        self._create_bind()

    def on_mouse_click(self, event: Event):
        """Process mouse click as an event."""
        self.control.add_gem(self.row, self.column)

    def set_type(self, type: int):
        """Changes the type and at the same time changes the graphic display."""
        self.type = type
        self.canvas.itemconfig(self.item, image=self._get_image())

    def set_row_and_column(self, row: int, column: int, animation_speed: int):
        """Сhanges coordinates using animation at a given speed."""
        self._animation_move_to(row, column, animation_speed)
        self.row = row
        self.column = column

    def _animation_move_to(self, row, column, step):
        # determines the size of the required movement
        diff_x = (row - self.row) * self._SIZE_IMAGE
        diff_y = (column - self.column) * self._SIZE_IMAGE

        step_x = step
        step_y = step

        if diff_x < 0:  # determines the direction of movement to the left or right
            step_x = -step

        if diff_y < 0:  # determines the direction of movement to the bottom or top
            step_y = -step
        # frame by frame we perform the movement
        while abs(diff_x) > abs(step_x):
            self._animation_move_tick(step_x, 0)
            diff_x -= step_x

        while abs(diff_y) > abs(step_y):
            self._animation_move_tick(0, step_y)
            diff_y -= step_y
        # if the image is not yet in the desired position, then move on
        self.canvas.move(self.item, diff_x, diff_y)

    def _animation_move_tick(self, diff_x, diff_y):
        """Display single-frame movement with a specified delay"""
        self.root.after(self._MOVE_ANIMATION_DELAY, self.canvas.move(self.item, diff_x, diff_y))
        self.canvas.update()

    def _get_image(self):
        # create objects for images in place and memorize them
        if self.type in self._IMG_GEM_FROM_TYPE:
            if self._IMG_GEM_FROM_TYPE[self.type][1] is None:
                self._IMG_GEM_FROM_TYPE[self.type][1] = PhotoImage(file=self._IMG_GEM_FROM_TYPE[self.type][0])
            return self._IMG_GEM_FROM_TYPE[self.type][1]

    def _create_item(self):
        self.item = self.canvas.create_image((self.row + 1) * self._SIZE_IMAGE, (self.column + 1) * self._SIZE_IMAGE,
                                             image=self._get_image())  # create image gem

    def _create_bind(self):
        self.canvas.tag_bind(self.item, '<Button-1>', self.on_mouse_click)  # set the event handler by right-clicking
