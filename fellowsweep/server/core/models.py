import numpy as np

from django.db import models
from django.contrib.auth.models import User

from fellowsweep import minesweeper
from .fields import ArrayField


class MinesweeperGame(models.Model):
    user = models.ForeignKey(User)
    game_over = models.BooleanField(default=False)
    won = models.BooleanField(default=False)
    board = ArrayField(default=np.zeros((1, 1)), max_length=5000)
    cell_states = ArrayField(default=np.zeros((1, 1)), max_length=5000)
    num_mines = models.IntegerField(default=10)

    @property
    def cell_state_values(self):
        """
        Return a list of lists containing cell values. Any cell that is not
        current revealed (equal to 1 in the cell_states array) is 'hidden'.
         
        """
        hidden = (self.cell_states == 0).tolist()
        board = self.board.tolist()
        values = list()
        for i, row in enumerate(board):
            row_list = list()
            for j, cell in enumerate(row):
                if hidden[i][j]:
                    row_list.append('hidden')
                else:
                    row_list.append(cell)
            values.append(row_list)
        return values

    @property
    def data(self):
        won = 1 if self.won else 0
        data_dict = {'num_mines': self.num_mines,
                     'user': self.user.username,
                     'num_cells': self.board.shape[0] ** 2,
                     'won': won}
        return data_dict

    @property
    def cell_states_list(self):
        return [cell_state for row_list in self.cell_state_values for cell_state in row_list]


