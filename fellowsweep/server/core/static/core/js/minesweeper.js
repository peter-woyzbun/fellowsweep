

function getStateDiv(state) {
    return $('.cell-states').children('.cell-state').filter('[data-state="' + state + '"]').clone();
}


function setInitialStates(post_url, csrf_token) {
    $.ajax
    ({
        url: post_url,
        data: {"csrfmiddlewaretoken": csrf_token},
        dataType: 'json',
        type: 'post',
        success: function (data) {
            var cell_states = data['states'];
            $('#game-container').find('.game-cell').each(function (index) {
                var cell_state = cell_states[index];
                var state_div = getStateDiv(cell_state);
                $(this).append(state_div);
            });
        }
    });
}


function updateCellState(x, y, new_state) {
    var game_cell = $('.game-cell[data-x="' + x + '"][data-y="' + y + '"]');
    game_cell.empty();
    game_cell.append(getStateDiv(new_state));
}


function updateCellStates(new_states) {
    $.each(new_states, function (key, value) {
            updateCellState(value.x, value.y, value.state)
        }
    );
}


function triggerCell(cell, post_url, csrf_token){
    var x = cell.parent().data('x');
    var y = cell.parent().data('y');

        $.ajax
        ({
            url: post_url,
            data: {"x": x, "y": y, "csrfmiddlewaretoken": csrf_token},
            type: 'post',
            success: function (data) {
                var game_over = 'game_over' in data;
                var game_won = 'game_won' in data;
                if (game_over){
                    if (game_won){
                        alert("GAME WON!");
                    } else{
                        alert("GAME LOST!");
                        $('.cell-trigger').off('click');
                    }
                    updateCellStates(data['updated_states']);
                } else {
                    updateCellStates(data['updated_states']);
                }
            }
        });
}