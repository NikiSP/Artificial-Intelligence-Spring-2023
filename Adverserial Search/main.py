from Game import Game
from Player import HumanPlayer, RandomPlayer, MiniMaxPlayer, MiniMaxProbPlayer


# # example 1:
# # player1 = RandomPlayer(1)
# player2 = RandomPlayer(2)

# # example 2:
# player1 = MiniMaxPlayer(1, depth=3)
# # player2 = MiniMaxPlayer(2, depth=1)

# game = Game(player1, player2)
# game.start_game()




def get_game_result(player1, player2, num_game):
    win, lose, draw = 0, 0, 0
    for i in range(num_game):
        game = Game(player1, player2, graphics=True)
        result = game.start_game()
        if result == 1:
            win += 1
        elif result == 2:
            lose += 1
        else:
            draw += 1
    return win, lose, draw
        
def mark():
    player1 = MiniMaxPlayer(1, depth=3)
    player2 = RandomPlayer(2)
    player3 = MiniMaxProbPlayer(2, depth=3, prob_stochastic=0.8)
    win1, lose1, draw1 = get_game_result(player1, player2, 10)
    win2, lose2, draw2 = get_game_result(player3, player2, 10)
    print(f'minimax player vs random player win={win1}, lose={lose1}, draw={draw1}')
    print(f'minimax prob player vs random player win={win2}, lose={lose2}, draw={draw2}')
    print(f'score: {win1 + win2}')

mark()