from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static

from .views import Dashboard, NewGame, Game, TriggerCell, GameCellStates, Login, Logout, Register


urlpatterns = [
    # Dashboard
    url(r'^$', Dashboard.as_view(), name='home'),
    # New game
    url(r'^new-game/', NewGame.as_view(), name='new_game'),
    # Login
    url(r'^login/', Login.as_view(), name='login'),
    # Logout
    url(r'^logout/', Logout.as_view(), name='logout'),
    # Register
    url(r'^register/', Register.as_view(), name='register'),
    # Game URLs
    url(r'^game/(?P<game_id>[\w-]+)/', include([
        # Minesweeper game
        url(r'^$', Game.as_view(), name='game'),
        # Cell trigger
        url(r'^trigger-cell/$', TriggerCell.as_view(), name='trigger_cell'),
        # Cell states
        url(r'^cell-states/$', GameCellStates.as_view(), name='cell_states'),
    ])),
]