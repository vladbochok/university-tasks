from Controller import GemController


class BoardModel:
    """
    Performs all computational actions on the board.
    Generates new gems, checks their affiliation.
    Performs gems exchange operations, field shifting, and integrity restoration
    """
    _FAST_ANIMATION = 6
    _SLOW_ANIMATION = 1
    _NUMBER_POINT_FROM_ONE_GEM = 1

    def __init__(self, width: int, height: int):
        self._width = width
        self._height = height
        self._score_point = 0
        self._create_board()

    def set_gem(self, row: int, column: int, gem_controller: GemController):
        """inserts the gem in the specified position"""
        self._gem_controllers[row][column] = gem_controller

    def fix_board(self):
        """Changes the playing field so that there are no groups of 3 or more adjacent gems"""
        self._fix_board()

    def swap_gems(self, gem_controller1, gem_controller2):
        """
        Swaps gems, checks if formed groups of 3 or more adjacent elements.
        and removes them, otherwise returns gems to their original locations
        """
        row1 = gem_controller1.row
        column1 = gem_controller1.column
        row2 = gem_controller2.row
        column2 = gem_controller2.column

        self._swap_gems(gem_controller1, gem_controller2, 1)
        if self._is_streak(row1, column1) or self._is_streak(row2, column2):
            self.remove_gems()
        else:
            self._swap_gems(gem_controller1, gem_controller2, 1)

    def remove_gems(self):
        """removes groups of identical gems while they are on the field"""
        while self._remove_gems():
            pass

    def get_item(self, row: int, column: int) -> GemController:
        try:
            return self._gem_controllers[row][column]
        except ValueError:
            return None

    def _fix_board(self):
        for i in range(self._height):
            for j in range(self._width):
                while self._is_streak(i, j):  # if found 3 or more neighbor gems
                    self._gem_controllers[i][j].set_random_type()

    def _add_point(self):
        self._score_point += self._NUMBER_POINT_FROM_ONE_GEM  # updates statistics of number destroyed gems

    def get_points(self) -> int:
        return self._score_point

    def _create_board(self):
        self._gem_controllers = [[0] * self._height for _ in range(self._width)]  # initializes a two-dimensional array

    def _is_streak(self, i: int, j: int):
        return self._is_vertical_streak(i, j) or self._is_horizontal_streak(i,
                                                                            j)  # checks for groups of 3 or more gems of the same type

    def _is_vertical_streak(self, x: int, y: int):
        streak = 1
        tmp_x = x
        # counts the same gems on the left
        while tmp_x > 0 and self._gem_controllers[tmp_x - 1][y] == self._gem_controllers[x][y]:
            streak += 1
            tmp_x -= 1

        tmp_x = x
        # counts the same gems on the right
        while tmp_x + 1 < self._height and self._gem_controllers[tmp_x + 1][y] == self._gem_controllers[x][y]:
            streak += 1
            tmp_x += 1

        return streak >= 3

    def _is_horizontal_streak(self, x, y):
        streak = 1
        tmp_y = y
        # counts the same gems from the bottom
        while tmp_y > 0 and self._gem_controllers[x][tmp_y - 1] == self._gem_controllers[x][y]:
            streak += 1
            tmp_y -= 1

        tmp_y = y
        # counts the same gems from the top
        while tmp_y + 1 < self._width and self._gem_controllers[x][tmp_y + 1] == self._gem_controllers[x][y]:
            streak += 1
            tmp_y += 1

        return streak >= 3

    def _remove_gems(self) -> bool:
        list_gem = []
        for i in range(self._width):
            for j in range(self._width):
                if self._is_streak(i, j):
                    list_gem.append(self._gem_controllers[i][j])

        self._remove_steak(list_gem)  # delete groups
        self._make_fall()  # moves the gems down
        self._fill_board()  # fills in the blanks with new random gems

        return len(list_gem) > 0

    def _remove_steak(self, list_gem_to_remove: list):
        for gem in list_gem_to_remove:
            self._add_point()  # update statistics
            gem.set_empty_type()

    def _swap_gems(self, gem_controller1, gem_controller2, animation_speed):
        row1 = gem_controller1.row
        column1 = gem_controller1.column
        row2 = gem_controller2.row
        column2 = gem_controller2.column

        self._gem_controllers[row1][column1], self._gem_controllers[row2][column2] \
            = self._gem_controllers[row2][column2], self._gem_controllers[row1][column1]

        self._gem_controllers[row1][column1].swap(self._gem_controllers[row2][column2], animation_speed)

    def _make_fall(self):
        for _ in range(self._height): # find the first "zero" gem and lift it up
            for j in range(self._height - 1, 0, -1): # passing from bottom to top
                for i in range(self._width):
                    if self._gem_controllers[i][j].is_empty() and not self._gem_controllers[i][j - 1].is_empty():
                        self._swap_gems(self._gem_controllers[i][j - 1], self._gem_controllers[i][j],
                                        self._FAST_ANIMATION)

    def _fill_board(self):
        for i in range(self._width):
            for j in range(self._height):
                if self._gem_controllers[i][j].is_empty(): # changes only places where there are no gems
                    self._gem_controllers[i][j].set_random_type()
