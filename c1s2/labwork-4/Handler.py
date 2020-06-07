class Handler:
    """
    A class that handles events for gems.
    Designed to transfer data processing and transfer chain responsibilities.
    """

    def __init__(self, board_controller):
        self._board_controller = board_controller
        self.board_model = board_controller.board_model
        self._gem1 = None
        self._gem2 = None

    def add_gem(self, row, column):
        """
        Adds gems to the processing.
        Performs permutation of two gems.
        Destruction of the resulting groups of gems.
        """
        gem = self.board_model.get_item(row, column)

        if self._is_none_gem1():
            self._gem1 = gem
        elif self._is_none_gem2():
            self._gem2 = gem
            self._make_move()
            self._set_gems_none()

    def check_move(self):
        if self._is_none_gem2():
            return False

        first_row = self._gem1.row
        first_column = self._gem1.column
        second_row = self._gem2.row
        second_column = self._gem2.column

        if abs(first_row - second_row) > 1 or abs(first_column - second_column) > 1:
            return False
        if abs(first_row - second_row) == 1 and abs(first_column - second_column) == 1:
            return False

        return True

    def _make_move(self):
        if self.check_move():
            self._board_controller.swap_gems(self._gem1, self._gem2)

    def _is_none_gem1(self):
        return self._gem1 is None

    def _is_none_gem2(self):
        return self._gem2 is None

    def _set_gems_none(self):
        self._gem1 = None
        self._gem2 = None
