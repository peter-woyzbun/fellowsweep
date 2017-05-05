import copy

import scipy.ndimage
import numpy as np


class StateUpdater(object):

    """
    Class for updating the 'states' - what cells should be revealed - of
    a minesweeper game.
    
    Parameters
    ----------
    board : numpy array
        An array describing the minesweeper game.
    existing_cell_states : numpy array
        An array indicating what cells are current revealed (1) or
        hidden (0).
    
    """

    def __init__(self, board: np.ndarray, existing_cell_states: np.ndarray):
        self.board = board
        self.existing_cell_states = existing_cell_states
        self.updated_cell_states = copy.deepcopy(existing_cell_states)
        self.unmask = None
        self.game_over = False
        self.game_won = False

    def _check_if_game_won(self):
        if np.count_nonzero(self.updated_cell_states) == self.n_board_rows ** 2 - self.num_mines:
            self.game_won = True

    @property
    def num_mines(self):
        return np.count_nonzero(self.mines)

    @property
    def mines(self):
        return (self.board == -1) * 1

    @property
    def n_board_rows(self):
        return self.board.shape[0]

    @property
    def n_board_cols(self):
        return self.board.shape[1]

    def set_changed_states(self, unmask):
        print(np.where(self.existing_cell_states != unmask))

    def updated_states(self):
        """ Return the value of every cell that is revealed after update. """
        # Get the x,y coords of every cell that has changed state.
        updated_state_coords = np.transpose(np.nonzero(self.unmask))
        updates = list()
        # Get the value for all newly revealed cells.
        for x, y in updated_state_coords:
            state = self.board[x, y]
            if type(type) != str:
                state = int(state)
            updates.append({'x': int(x), 'y': int(y), 'state': state})
        return updates

    @staticmethod
    def _label_empty_cell_groups(empty_cells) -> np.ndarray:
        """
        Return an array that has labels for empty groups of cells. For example,
        
            1 1 0      1 1 0
            0 0 0  ->  0 0 0
            0 1 1      0 2 2
            
        A cell is 'empty' if it does not contain a mine and is not adjacent
        to a mine.
        
        Parameters
        ----------
        empty_cells : numpy array
            A binary array where 1 indicates an empty cell, and 0 indicates a
            cell containing a mine, or a cell adjacent to a mine.
        
        """
        labeled_cells, num_groups = scipy.ndimage.measurements.label(empty_cells)
        return labeled_cells

    @staticmethod
    def _select_group(labeled_cells, group_num):
        """
        Take an array containing labeled groups, and return a binary array where
        1 indicates a member of the given group, and 0 otherwise. For example,
        for group number 2,
        
            1 1 0      0 0 0
            0 0 0  ->  0 0 0
            0 2 2      0 1 1
        
        Parameters
        ----------
        labeled_cells : numpy array
            A binary array whose elements that are greater than zero indicate
            that cell's group, and cells that are equal to 0 indicate 'empty'
            space.
        group_num : int
            The group number to select.
        
        """
        return (labeled_cells == group_num) * 1

    @staticmethod
    def _dilate_group(cell_group):
        """
        'Dilate' the given cell group - i.e. create a 'border' around it by
        adding 1's. For example,
        
            0 0 0      0 0 0
            0 0 0  ->  0 1 1
            0 1 1      1 1 1
        
        Parameters
        ----------
        cell_group : numpy array
            Binary array indicating the cells contained in the group.
            
        """
        dilation_struct = scipy.ndimage.generate_binary_structure(2, 2)
        unmask = scipy.ndimage.binary_dilation(cell_group, structure=dilation_struct).astype(cell_group.dtype)
        return unmask

    def _trigger_empty_cell(self, x, y):
        """
        Trigger an 'empty' cell - one not adjacent to a bomb, and not containing
        a bomb. 
        
        Label: https://docs.scipy.org/doc/scipy-0.16.0/reference/generated/scipy.ndimage.measurements.label.html
        Dilate: https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/
                scipy.ndimage.morphology.generate_binary_structure.html
        """
        # Create a binary array where 1 indicates an empty cell, and 0 a non-empty cell.
        empty_cells = (self.board == 0) * 1
        # Label groups of empty cells and get the required group number given triggered cell position.
        labeled_cells = self._label_empty_cell_groups(empty_cells=empty_cells)
        group_num = labeled_cells[x, y]
        # Create a binary array where 1 indicates a cell in the given group, and 0 not.
        cell_group = self._select_group(labeled_cells=labeled_cells, group_num=group_num)
        # Create a 'border' around the cell group.
        unmask = self._dilate_group(cell_group=cell_group)
        self.unmask = unmask
        # The 'unmask' array indicates what cells have changed state.
        self.updated_cell_states += unmask

    def _reveal_single_cell(self, x, y):
        """ Reveal a single cell. This requires creating an array with a 1 placed in the given coords. """
        unmask = np.zeros((self.n_board_rows, self.n_board_cols))
        unmask.itemset((x, y), 1)
        self.unmask = unmask
        self.updated_cell_states += unmask

    def trigger_cell(self, x, y):
        """
        Trigger the given cell - i.e. determine what cells should be revealed given the
        cell's properties.
        
        """
        point_value = self.board.item((x, y))
        if point_value < 0:
            # If the point value is less than 1, the user has hit a mine.
            self.game_over = True
            self.unmask = np.ones((self.n_board_rows, self.n_board_cols))
            self.updated_cell_states = np.ones((self.n_board_rows, self.n_board_cols))
        elif point_value == 0:
            self._trigger_empty_cell(x=x, y=y)
        else:
            self._reveal_single_cell(x=x, y=y)
            self._check_if_game_won()

