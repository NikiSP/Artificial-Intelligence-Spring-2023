from Board import BoardUtility
import random
import numpy as np
import copy

ROWS = 6
COLS = 6

class Player:
    def __init__(self, player_piece):
        self.piece = player_piece

    def play(self, board):
        return 0
    
                            
    @staticmethod
    def score_position(game_board, piece):
        """
        compute the game board score for a given piece.
        you can change this function to use a better heuristic for improvement.
        """
        
        if BoardUtility.has_player_won(game_board, piece):
            return 100_000_000_000  # player has won the game give very large score
        if BoardUtility.has_player_won(game_board, 1 if piece == 2 else 2):
            return -100_000_000_000  # player has lost the game give very large negative score
        if BoardUtility.is_draw:
            return 0
        
        scores=[0,0]
       
        for i in range(1,ROWS-2):
            for j in range(1,COLS-2):
                if board[i][j]!=0:
                    scores[board[i][j]-1]+=1 
    
        for i in range(ROWS):
            for j in range(COLS):
                if board[i][j]==board[i][j+1] and board[i][j]!=0:
                    scores[board[i][j]-1]+=1
                    
        for i in range(ROWS):
            for j in range(COLS):
                if board[i][j]==board[i+1][j] and board[i][j]!=0:
                    scores[board[i][j]-1]+=1
                    
        for i in range(ROWS-1):
            for j in range(1,COLS):
                if board[i][j]==board[i-1][j+1] and board[i][j]!=0:
                    scores[board[i][j]-1]+=1
                    
        for i in range(1,ROWS):
            for j in range(1,COLS):
                if board[i][j]==board[i-1][j-1] and board[i][j]!=0:
                    scores[board[i][j]-1]+=1
                                                             
        return (scores[0]-scores[1])
    

class RandomPlayer(Player):
    def play(self, board):
        return [random.choice(BoardUtility.get_valid_locations(board)), random.choice([1, 2, 3, 4]), random.choice(["skip", "clockwise", "anticlockwise"])]


class HumanPlayer(Player):
    def play(self, board):
        move = input("row, col, region, rotation\n")
        move = move.split()
        print(move)
        return [[int(move[0]), int(move[1])], int(move[2]), move[3]]


class MiniMaxPlayer(Player):
    def __init__(self, player_piece, depth=5):
        super().__init__(player_piece)
        self.depth = depth

    def miniMaxAlgorithm(self, maxTurn, depth, piece, board, alpha, beta):

        if depth<self.depth and (not BoardUtility().is_terminal_state(board)):
            move=[-1, -1, -1]
            
            value=np.inf
            if maxTurn:
                value*=-1
            
            nodes=BoardUtility().get_valid_locations(board)
            for n in nodes:
                for region in range(1,5):
                    for rotation in ["skip","clockwise","anticlockwise"]:
                        copyBoard=copy.deepcopy(board)   
                        BoardUtility().make_move(copyBoard, n[0], n[1], region, rotation, 1 if piece==2 else 2)    
                        currentValue=self.miniMaxAlgorithm(not maxTurn, depth+1,piece, copyBoard, alpha, beta)
                        
                        if maxTurn:
                            if value<currentValue:
                                value=currentValue
                                if depth==0:  
                                    move[0]=n
                                    move[1]=region
                                    move[2]=rotation
                        
                            if value>=beta:
                                if depth==0:
                                    return move
                                return value
                            alpha=max(value, alpha) 
                        else:           
                            value=min(value, currentValue)
                            if value<=alpha:
                                return value
                            beta=min(value, beta)       
            if depth==0:
                return move 
            return value

        else:
            return self.score_position(board,piece) 
    
              
    def play(self, board):        
        return (self.miniMaxAlgorithm(True, 0, self.piece, board, -np.Inf, np.Inf))


class MiniMaxProbPlayer(Player):
    def __init__(self, player_piece, depth=5, prob_stochastic=0.1):
        super().__init__(player_piece)
        self.depth = depth
        self.prob_stochastic = prob_stochastic

    
    def miniMaxAlgorithm(self, maxTurn, depth, piece, board, alpha, beta):

        if depth<self.depth and (not BoardUtility().is_terminal_state(board)):
            move=[-1, -1, -1]
            
            value=np.inf
            if maxTurn:
                value*=-1
            
            nodes=BoardUtility().get_valid_locations(board)
            for n in nodes:
                for region in range(1,5):
                    for rotation in ["skip","clockwise","anticlockwise"]:
                        copyBoard=copy.deepcopy(board)   
                        BoardUtility().make_move(copyBoard, n[0], n[1], region, rotation, 1 if piece==2 else 2)    
                        currentValue=self.miniMaxAlgorithm(not maxTurn, depth+1,piece, copyBoard, alpha, beta)
                        
                        if maxTurn:
                            if value<currentValue:
                                value=currentValue
                                if depth==0:  
                                    move[0]=n
                                    move[1]=region
                                    move[2]=rotation
                        
                            if value>=beta:
                                if depth==0:
                                    return move
                                return value
                            alpha=max(value, alpha) 
                        else:           
                            value=min(value, currentValue)
                            if value<=alpha:
                                return value
                            beta=min(value, beta)       
            if depth==0:
                return move 
            return value

        else:
            return self.score_position(board,piece) 
    
    
    def play(self, board):
        
        move=self.miniMaxAlgorithm(True, 0, self.piece, board, -np.Inf, np.Inf)
        nodes=BoardUtility().get_valid_locations(board)
        nodes.remove(move[0])            

        if len(nodes) != 0 and sum(random.choices([True,False], [self.prob_stochastic, 1-self.prob_stochastic], k=1)):
              return [random.choice(nodes), random.choice([1,2,3,4]), random.choice(["skip", "clockwise", "anticlockwise"])]             
                    
        return move

    
 
