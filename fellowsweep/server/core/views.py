import pandas as pd

from fellowsweep import minesweeper

from django.shortcuts import render, redirect
from django.views import View
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import LogoutView, LoginView
from .models import MinesweeperGame, User


# =============================================
# User Management
# ---------------------------------------------

class Login(LoginView):

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(reverse('core:home'))


class Logout(LogoutView):

    def post(self, request):
        logout(request)
        return redirect(reverse('core:home'))


class Register(View):

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        new_user = User(username=username, password=password)
        new_user.save()
        login(request, new_user)
        return redirect(reverse('core:home'))


# =============================================
# Dashboard/Home
# ---------------------------------------------

class Dashboard(View):
    """
    This is the 'home' page of the game.
    
    """

    def get(self, request):
        all_games = MinesweeperGame.objects.all()
        score_df = pd.DataFrame([game.data for game in all_games])
        scoreboard = minesweeper.Scoreboard(scores_df=score_df)
        df = scoreboard.df()
        scoreboard_html = df.to_html()
        return render(request, 'core/dashboard.html', context={'games': None, 'scoreboard': scoreboard_html})


# =============================================
# New Game Creation
# ---------------------------------------------

class NewGame(View):

    """
    View for creating a new minesweeper game. On the user side this is 
    called via a modal/pop-up.
    
    """

    def post(self, request):
        n_rows = int(request.POST.get("game_size"))
        n_mines = int(request.POST.get("num_mines"))
        user = request.user
        new_game = self._create_new_game(user=user, n_rows=n_rows, n_cols=n_rows, n_mines=n_mines)
        return redirect(reverse('core:game', kwargs={'game_id': new_game.id}))

    @staticmethod
    def _create_new_game(user, n_rows, n_cols, n_mines):
        board_generator = minesweeper.BoardGenerator(n_rows=n_rows, n_cols=n_cols, n_mines=n_mines)
        board_array = board_generator.make_board()
        cell_states_array = board_generator.make_cell_states()
        new_game = MinesweeperGame(user=user, board=board_array, cell_states=cell_states_array, num_mines=n_mines)
        new_game.save()
        return new_game


# =============================================
# Game State Handling
# ---------------------------------------------

class Game(View):

    """
    View for the actual minesweeper game.

    """

    def get(self, request, game_id):
        game = MinesweeperGame.objects.get(id=game_id)
        return render(request, 'core/game.html', context={'game': game})


class GameCellStates(View):

    """
    View for return JSON containing the state of all game cells. This is
    called via jquery in order to set the initial states of a game when
    it is loaded.

    """

    def post(self, request, game_id):
        user = request.user
        game = MinesweeperGame.objects.get(id=game_id, user=user)
        return JsonResponse({'states': game.cell_states_list})


class TriggerCell(View):

    """
    View for 'triggering' a game board cell. It takes the x, y coordinates 
    of the clicked cell and uses the StateUpdater class to determine the outcome.
    It returns a JSON response containing a list of all cells that have now changed,
    and their 'new' values.

    """

    def post(self, request, game_id):
        user = request.user
        x = int(request.POST.get("x"))
        y = int(request.POST.get("y"))
        game = MinesweeperGame.objects.get(id=game_id, user=user)
        state_updater = minesweeper.StateUpdater(board=game.board, existing_cell_states=game.cell_states)
        state_updater.trigger_cell(x=x, y=y)
        if state_updater.game_over:
            game.cell_states = state_updater.updated_cell_states
            game.game_over = True
            game.save()
            return JsonResponse({'game_over': True,
                                 'updated_states': state_updater.updated_states(),
                                 'game_won': state_updater.game_won})
        else:
            print(state_updater.updated_cell_states)
            game.cell_states = state_updater.updated_cell_states
            game.save()
            return JsonResponse({'updated_states': state_updater.updated_states()})
