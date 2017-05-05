import numpy as np
import scipy.signal


class BoardGenerator(object):

    """
    Class for generating a minesweeper game board. The board is
    represented as a numpy array, where, for a given element:
    
        - [0] indicates a cell with no adjacent mines,
        - [1] indicates a cell with 1 adjacent mine,
        - ...
        - [8] indicates a cell with 8 adjacent mines,
        - [-1] indicates a cell with a mine.
    
    """

    def __init__(self, n_rows, n_cols, n_mines):
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.n_mines = n_mines

    def _mine_placements(self):
        """ Place 'mines' - the value 1 - randomly in array of given dimensions."""
        # Start with an array/matrix of zeros.
        mines = np.zeros((self.n_rows, self.n_cols))
        # Randomly place 1's.
        mines.ravel()[np.random.choice(mines.size, self.n_mines, replace=False)] = 1
        return mines

    @staticmethod
    def _make_adjacency_counts(mines):
        """ Generate all adjacency counts, then replace the location of each mine with -1.  """
        counts = scipy.signal.convolve2d(mines, np.ones((3, 3)), mode='same')
        # Elements of the board array that are equal to 1 indicate mines, while in the final
        # board mines are represented by -1, so replace accordingly.
        counts[mines > 0] = -1
        return counts

    def make_board(self):
        mines = self._mine_placements()
        final_board = self._make_adjacency_counts(mines=mines)
        return final_board

    def make_cell_states(self):
        """ Return the initial cell states - everything is hidden (0). """
        return np.zeros((self.n_rows, self.n_cols))





