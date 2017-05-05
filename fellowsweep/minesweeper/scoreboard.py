import pandas as pd


class Scoreboard(object):

    """
    Class for creating a dataframe of user scores, which are
    adjusted based on the game difficulty (ratio of mines to cells).
    
    """

    def __init__(self, scores_df: pd.DataFrame):
        self.scores_df = scores_df

    @staticmethod
    def _flatten_header(df):
        mi = df.columns
        new_index_lis = []
        # Todo: Find better way of doing this...
        for e in mi.tolist():
            if e[1] == '':
                new_index_lis.append(e[0])
            else:
                new_index_lis.append(e[1])

        ind = pd.Index(new_index_lis)
        df.columns = ind
        return df

    def df(self):
        """  """
        self.scores_df['mine_cell_ratio'] = self.scores_df['num_mines'] / self.scores_df['num_cells']
        self.scores_df['game_score'] = self.scores_df['mine_cell_ratio'] * self.scores_df['won']
        aggregations = {
            'mine_cell_ratio': {
                'avg_difficulty': 'mean',
            },
            'won': {
                'wins': 'sum',
                'games_played': 'count'
            },
            'game_score': {
                'score': 'sum',
            },
        }
        agg_df = self.scores_df.groupby('user').agg(aggregations)
        final_df = self._flatten_header(df=agg_df)
        return final_df