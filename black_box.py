# Author: Logan Cope
# Date:      8/5/2020
# Description: Creates BlackBoxGame class used for playing the board
#              game called Back Box. There is a 10x10 grid (list of
#              lists) that represents the board. Positions of where
#              atoms should be placed are passed into the class to
#              initialize the board. Then a player can shoot a ray
#              from any border square (aside from corners) which will
#              be manipulated based on the location of the atoms on
#              the board. A player will start with 25 points, a point
#              will be deducted for each new entry or exit and 5 points
#              will be deducted for a new, incorrect guess.


class BlackBoxGame:
    """
    Class used for playing the board game called Back Box. There is a 10x10 grid (list of
    lists) that represents the board. Positions of where atoms should be placed are passed
    into class to initialize the board. Then a player can shoot a ray from any border square
    (aside from corners) which will be travel and be manipulated based on the location of the
    atoms on the board. A player will start with 25 points, a point will be deducted for each
    new entry or exit and 5 points will be deducted for a new, incorrect guess.
    """

    def __init__(self, atom_locations):
        """
        Initialize game board to a 10x10 list of lists. Takes a parameter of a list of
        (row, column) tuples for the locations of the atoms in the black box, and places
        them on the board. Initializes atoms_remaining to the number of atoms passed in the
        atoms_locations list. Initializes the score to 25. Creates a list to represent
        allowed entry points for the user to pass to the shoot_ray method. Initializes
        a list of guesses to an empty list as well as a list of used entry/exit points
        to an empty list.
        :param atom_locations: list of tuples representing locations of atoms in the
                               black box
        """
        self._game_board = [['', '', '', '', '', '', '', '', '', ''],
                            ['', '', '', '', '', '', '', '', '', ''],
                            ['', '', '', '', '', '', '', '', '', ''],
                            ['', '', '', '', '', '', '', '', '', ''],
                            ['', '', '', '', '', '', '', '', '', ''],
                            ['', '', '', '', '', '', '', '', '', ''],
                            ['', '', '', '', '', '', '', '', '', ''],
                            ['', '', '', '', '', '', '', '', '', ''],
                            ['', '', '', '', '', '', '', '', '', ''],
                            ['', '', '', '', '', '', '', '', '', '']]
        self._atom_locations = atom_locations

        # set atoms to specified locations
        for atom in atom_locations:
            self._game_board[atom[0]][atom[1]] = 'A'
        self._atoms_remaining = len(atom_locations)
        self._score = 25
        self._guesses = []

        # use list of tuples to represent allowed entries/exit points
        self._allowed_entry_points = [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8),
                                      (9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (9, 6), (9, 7), (9, 8),
                                      (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0),
                                      (1, 9), (2, 9), (3, 9), (4, 9), (5, 9), (6, 9), (7, 9), (8, 9)]
        self._entry_and_exit_points = []

    def display_board(self):
        """
        Prints out Black Box board one row at a time
        """
        for row in self._game_board:
            print(row)

    def shoot_ray(self, row, column):
        """
        First checks if chosen row and column designates a valid entry point, if it does
        not, then False is returned. Adds this chosen row/column to entry point array if
        it is not already in said list and subtract from points. Then interacts with direction
        method to determine the initial direction the ray is traveling in. Next call the
        check_edge_case_reflection method is called to check the reflection case where a ray
        begins directly next to an atom that is along the "edge" of the board; if this type of
        reflection occurs just return the row and column that was passed in originally. If
        method hasn't already returned then call travel method based on initial direction to
        determine the exit_point. Update entry/exit list if needed, update points if needed,
        and return the exit_point. Note: multiple returns are possible, see return section
        below for more detail on what returns are possible based on given situations

        :param row: integer representing the desired row on the game board
        :param column: integer representing the desired column on the game board
        :return: bool of False if chosed row and column are not valid entries
        :return: None if hit occurs
        :return: tuple (row, column) of the exit point of the ray
        """
        # check if row/column is an allowed entry point
        if (row, column) not in self._allowed_entry_points:
            return False

        # add entry to entry/exit point list and deduct point if entry hasn't already been used
        if (row, column) not in self._entry_and_exit_points:
            self._entry_and_exit_points.append((row, column))
            self._score -= 1

        # determine which direction ray will initially be traveling
        direction = self.check_direction(row, column)

        # Check the reflection edge case where atom is along a border and ray is shot
        # right next to said atom
        if self.check_edge_case_reflection(row, column, direction):
            return (row, column)

        # If we haven't hit a return statement then follow the rest of the ray's path
        # Call the correct method based on the initial direction that the ray is traveling
        # Exit point will hold tuple of exit point or None if a hit occurred
        if direction == 'right':
            exit_point = self.travel_right(row, column)
        elif direction == 'left':
            exit_point = self.travel_left(row, column)
        elif direction == 'up':
            exit_point = self.travel_up(row, column)
        elif direction == 'down':
            exit_point = self.travel_down(row, column)

        # If exit point was not a hit and isn't already an entry/exit point, subtract 1
        # from the score and add exit_point to entry/exit point list
        if exit_point is not None and exit_point not in self._entry_and_exit_points:
            self._entry_and_exit_points.append(exit_point)
            self._score -= 1
        return exit_point

    def check_direction(self, row, column):
        """
        Determines the initial direction that the ray is traveling and returns this to the
        shoot_ray method
        :param row: integer representing the desired row on the game board
        :param column: integer representing the desired column on the game board
        :return: string representing the initial direction array is traveling
        """
        if row == 0:
            return 'down'
        elif row == 9:
            return 'up'
        elif column == 0:
            return 'right'
        elif column == 9:
            return 'left'

    def travel_right(self, row, column):
        """
        Method can be called by shoot_ray if ray is initially traveling in this direction
        or by any other traveling method if a deflection send the ray in this direction.
        This will travel to the right on the board until either a hit occurs, the ray
        reaches the right border, or a deflection sends the ray in a different direction.
        In which case this method will call the method of the direction the ray begins
        traveling in. Note: multiple returns are possible, see return section below
        for more detail on what returns will occur based on given situations

        :param row: Represents the row the ray was on when this method was called
        :param column: Represents the column the ray was on when this method was called
        :return: None if hit occurs
        :return: tuple representing exit point of the array
        """
        # initialize position to current row and column
        curr_row = row
        curr_col = column
        count = 0  # this will be used to determine if we are on the first iteration of while loop

        # we will just continue this loop until we hit a return statement
        while True:
            # if at border, but not on first passed row/column return exit point tuple
            if (curr_row, curr_col) in self._allowed_entry_points and count != 0:
                return (curr_row, curr_col)

            # peek at next position, if it causes a hit, return None
            elif self._game_board[curr_row][curr_col + 1] == 'A':
                return None

            # look diagonally right and up to see if a deflection occurs, go down if so
            elif self._game_board[curr_row - 1][curr_col + 1] == 'A':
                return self.travel_down(curr_row, curr_col)

            # look diagonally right and down to see if a deflection occurs, go up if so
            elif self._game_board[curr_row + 1][curr_col + 1] == 'A':
                return self.travel_up(curr_row, curr_col)

            # otherwise, move ray to the right on board
            else:
                curr_col += 1
            count += 1  # increment count so we know we are not on the first iteration

    def travel_left(self, row, column):
        """
        Method can be called by shoot_ray if ray is initially traveling in this direction
        or by any other traveling method if a deflection send the ray in this direction.
        This will travel to the left on the board until either a hit occurs, the ray
        reaches the left border, or a deflection sends the ray in a different direction.
        In which case this method will call the method of the direction the ray begins
        traveling in. Note: multiple returns are possible, see return section below
        for more detail on what returns will occur based on given situations

        :param row: Represents the row the ray was on when this method was called
        :param column: Represents the column the ray was on when this method was called
        :return: None if hit occurs
        :return: tuple representing exit point of the array
        """
        # initialize position to current row and column
        curr_row = row
        curr_col = column
        count = 0  # this will be used to determine if we are on the first iteration of while loop

        # we will just continue this loop until we hit a return statement
        while True:
            # if at border, but not on first passed row/column return exit point tuple
            if (curr_row, curr_col) in self._allowed_entry_points and count != 0:
                return (curr_row, curr_col)

            # peek at next position, if it causes a hit, return None
            elif self._game_board[curr_row][curr_col - 1] == 'A':
                return None

            # look diagonally left and up to see if a deflection occurs, go down if so
            elif self._game_board[curr_row - 1][curr_col - 1] == 'A':
                return self.travel_down(curr_row, curr_col)

            # look diagonally left and up to see if a deflection occurs, go up if so
            elif self._game_board[curr_row + 1][curr_col - 1] == 'A':
                return self.travel_up(curr_row, curr_col)

            # otherwise, move ray to the left on board
            else:
                curr_col -= 1
            count += 1  # increment count so we know we are not on the first iteration

    def travel_up(self, row, column):
        """
        Method can be called by shoot_ray if ray is initially traveling in this direction
        or by any other traveling method if a deflection send the ray in this direction.
        This will travel up on the board until either a hit occurs, the ray reaches the
        top border, or a deflection sends the ray in a different direction. In which case
        this method will call the method of the direction the ray begins traveling in.
        Note: multiple returns are possible, see return section below for more detail
        on what returns will occur based on given situations

        :param row: Represents the row the ray was on when this method was called
        :param column: Represents the column the ray was on when this method was called
        :return: None if hit occurs
        :return: tuple representing exit point of the array
        """
        # initialize position to current row and column
        curr_row = row
        curr_col = column
        count = 0  # this will be used to determine if we are on the first iteration of while loop

        # we will just continue this loop until we hit a return statement
        while True:
            # if at border, but not on first passed row/column return exit point tuple
            if (curr_row, curr_col) in self._allowed_entry_points and count != 0:
                return (curr_row, curr_col)

            # peek at next position, if it causes a hit, return None
            elif self._game_board[curr_row - 1][curr_col] == 'A':
                return None

            # look diagonally right and up to see if a deflection occurs, go left if so
            elif self._game_board[curr_row - 1][curr_col + 1] == 'A':
                return self.travel_left(curr_row, curr_col)

            # look diagonally left and up to see if a deflection occurs, go right if so
            elif self._game_board[curr_row - 1][curr_col - 1] == 'A':
                return self.travel_right(curr_row, curr_col)

            # otherwise, move ray up on board
            else:
                curr_row -= 1
            count += 1  # increment count so we know we are not on the first iteration

    def travel_down(self, row, column):
        """
        Method can be called by shoot_ray if ray is initially traveling in this direction
        or by any other traveling method if a deflection send the ray in this direction.
        This will travel down on the board until either a hit occurs, the ray reaches the
        lower border, or a deflection sends the ray in a different direction. In which case
        this method will call the method of the direction the ray begins traveling in.
        Note: multiple returns are possible, see return section below for more detail
        on what returns will occur based on given situations

        :param row: Represents the row the ray was on when this method was called
        :param column: Represents the column the ray was on when this method was called
        :return: None if hit occurs
        :return: tuple representing exit point of the array
        """
        # initialize position to current row and column
        curr_row = row
        curr_col = column

        count = 0  # this will be used to determine if we are on the first iteration of while loop

        # we will just continue this loop until we hit a return statement
        while True:
            # if at border, but not on first passed row/column return exit point tuple
            if (curr_row, curr_col) in self._allowed_entry_points and count != 0:
                return (curr_row, curr_col)

            # peek at next position, if it causes a hit, return None
            elif self._game_board[curr_row + 1][curr_col] == 'A':
                return None

            # look diagonally right and down to see if a deflection occurs, go left if so
            elif self._game_board[curr_row + 1][curr_col + 1] == 'A':
                return self.travel_left(curr_row, curr_col)

            # look diagonally left and down to see if a deflection occurs, go right if so
            elif self._game_board[curr_row + 1][curr_col - 1] == 'A':
                return self.travel_right(curr_row, curr_col)

            # otherwise, move ray down on board
            else:
                curr_row += 1
            count += 1  # increment count so we know we are not on the first iteration

    def check_edge_case_reflection(self, row, column, direction):
        """
        Checks the reflection case where a ray begins directly next to an atom that is along
        the "edge" of the board. If it does, True is returned otherwise False is returned
         :param row: integer representing the desired row on the game board
        :param column: integer representing the desired column on the game board
        :param direction: string representing initial direction ray is traveling in so we
                          know which board positions to check
        :return: boolean (True/False) representing whether this reflection edge case occurs
        """
        # For all the following, if there is not a hit but there is an atom directly diagonal
        # of the initial position of the ray then return True
        if direction == 'right':
            if (self._game_board[row][column + 1] != 'A' and
                    (self._game_board[row - 1][column + 1] == 'A' or
                     self._game_board[row + 1][column + 1] == 'A')):
                return True
            else:
                return False
        elif direction == 'left':
            if (self._game_board[row][column - 1] != 'A' and
                    (self._game_board[row - 1][column - 1] == 'A' or
                     self._game_board[row + 1][column - 1] == 'A')):
                return True
            else:
                return False
        elif direction == 'up':
            if (self._game_board[row - 1][column] != 'A' and
                    (self._game_board[row - 1][column + 1] == 'A' or
                     self._game_board[row - 1][column - 1] == 'A')):
                return True
            else:
                return False
        elif direction == 'down':
            if (self._game_board[row + 1][column] != 'A' and
                    (self._game_board[row + 1][column - 1] == 'A' or
                     self._game_board[row + 1][column + 1] == 'A')):
                return True
            else:
                return False

    def guess_atom(self, row, column):
        """
        If guess is correct and hasn't already been guessed, 1 is subtracted from the
        atoms_left and guess is added. Either way if guess is correct True is returned.
        If guess is incorrect, if guess hasn't already been guessed, 5 will be subtracted
        from the user's score and guess will be added to the guess list. False will be
        returned
        :param row: integer representing row of user's guess
        :param column: nteger representing column of user's guess
        :return: boolean (True/False) representing whether user's guess is correct
        """
        # If guess is correct and hasn't already been guessed, subtract 1 from atoms_left
        # and add guess to guesses list
        if (row, column) in self._atom_locations:
            if (row, column) not in self._guesses and self._atoms_remaining != 0:
                self._atoms_remaining -= 1
                self._guesses.append((row, column))
            return True

        # If guess was incorrect, we will fall through to the following logic
        # If location has not already been guessed, subtract 5 and add guess to guesses list
        if (row, column) not in self._guesses:
            self._score -= 5
            self._guesses.append((row, column))
        return False

    def get_score(self):
        """
        Returns the player's current score
        :return: integer of the player's current score
        """
        return self._score

    def atoms_left(self):
        """
        Returns the remaining atoms not yet correctly guessed
        :return: integer of remaining atoms left to be guessed
        """
        return self._atoms_remaining
