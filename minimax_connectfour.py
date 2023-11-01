import copy
import time
import abc
import random

class Game(object):
    """A connect four game."""

    def __init__(self, grid):
        """Instances differ by their board."""
        self.grid = copy.deepcopy(grid)  # No aliasing!

    def display(self):
        """Print the game board."""
        for row in self.grid:
            for mark in row:
                print(mark, end='')
            print()
        print()

    def possible_moves(self):
        """Return a list of possible moves given the current board."""
        moves = []
        for col in range(len(self.grid[0])):
            if self.grid[0][col] == '-':
                moves.append(col)
        return moves

    def neighbor(self, col, color):
        """Return a Game instance like this one but with a move made into the specified column."""
        new_grid = copy.deepcopy(self.grid)
        for row in range(len(self.grid)-1, -1, -1):
            if new_grid[row][col] == '-':
                new_grid[row][col] = color
                break
        return Game(new_grid)

    def utility(self):
        """Return the minimax utility value of this game"""
        winning_state = self.winning_state()
        if winning_state == float('inf'):
            return 1
        elif winning_state == float('-inf'):
            return -1
        else:
            return 0

    
    def winning_state(self):
        """Returns float("inf") if Red wins; float("-inf") if Black wins;
           0 if board full; None if not full and no winner"""
        # YOU FILL THIS IN
            
        for row in self.grid:
            for i in range(len(row) - 3):
                if row[i:i+4] == ['R'] * 4:
                   return float("inf")
                elif row[i:i+4] == ['B'] * 4:
                   return float("-inf")
    # Check for vertical wins
        for i in range(len(self.grid[0])):
            col = [row[i] for row in self.grid]
            for j in range(len(col) - 3):
                if col[j:j+4] == ['R'] * 4:
                   return float("inf")
                elif col[j:j+4] == ['B'] * 4:
                   return float("-inf")
    # Check for diagonal wins
        for i in range(len(self.grid) - 3):
            for j in range(len(self.grid[0]) - 3):
                if self.grid[i][j] == self.grid[i+1][j+1] == self.grid[i+2][j+2] == self.grid[i+3][j+3] == 'R':
                   return float("inf")
                elif self.grid[i][j] == self.grid[i+1][j+1] == self.grid[i+2][j+2] == self.grid[i+3][j+3] == 'B':
                   return float("-inf")
        for i in range(len(self.grid) - 3):
            for j in range(3, len(self.grid[0])):
                if self.grid[i][j] == self.grid[i+1][j-1] == self.grid[i+2][j-2] == self.grid[i+3][j-3] == 'R':
                   return float("inf")
                elif self.grid[i][j] == self.grid[i+1][j-1] == self.grid[i+2][j-2] == self.grid[i+3][j-3] == 'B':
                   return float("-inf")
    # Check if board is full
        if all(mark != '-' for row in self.grid for mark in row):
            return 0
    # If game is not over yet
        return None

    


class Agent(object):
    """Abstract class, extended by classes RandomAgent, FirstMoveAgent, MinimaxAgent.
    Do not make an instance of this class."""

    def __init__(self, color):
        """Agents use either RED or BLACK chips."""
        self.color = color

    @abc.abstractmethod
    def move(self, game):
        """Abstract. Must be implemented by a class that extends Agent."""
        pass

class RandomAgent(Agent):
    """Naive agent -- always performs a random move"""

    def move(self, game):
        """Returns a random move"""
        possible_moves = game.possible_moves()
        return random.choice(possible_moves)

class FirstMoveAgent(Agent):
    """Naive agent -- always performs the first move"""

    
    def move(self, game):
        """Returns the first possible move"""
        possible_moves = game.possible_moves()
        return possible_moves[0]


class MinimaxAgent(Agent):
    """Smart agent -- uses minimax to determine the best move"""


    def move(self, game):
        """Returns the best move using minimax"""
        maxplayer = self.color
        minplayer = 'B' if self.color == 'R' else 'R'

        # The max player tries to maximize the utility value
        # The min player tries to minimize the utility value
        def minimax(game, depth, player):
            if game.winning_state() is not None or depth == 0:
                return game.utility(), None

            if player == maxplayer:
                best_val = float("-inf")
                best_move = None
                for move in game.possible_moves():
                    next_game = game.neighbor(move, maxplayer)
                    val, _ = minimax(next_game, depth - 1, minplayer)
                    if val > best_val:
                        best_val = val
                        best_move = move
            else: # player == minplayer
                best_val = float("inf")
                best_move = None
                for move in game.possible_moves():
                    next_game = game.neighbor(move, minplayer)
                    val, _ = minimax(next_game, depth - 1, maxplayer)
                    if val < best_val:
                        best_val = val
                        best_move = move

            return best_val, best_move

        _, best_move = minimax(game, depth=3, player=maxplayer)
        return best_move

def tournament(simulations=50):
    """Simulate connect four games, of a minimax agent playing
    against a random agent"""

    redwin, blackwin, tie = 0,0,0
    for i in range(simulations):

        game = single_game(io=False)

        print(i, end=" ")
        if game.winning_state() == float("inf"):
            redwin += 1
        elif game.winning_state() == float("-inf"):
            blackwin += 1
        elif game.winning_state() == 0:
            tie += 1

    print("Red %d (%.0f%%) Black %d (%.0f%%) Tie %d" % (redwin,redwin/simulations*100,blackwin,blackwin/simulations*100,tie))

    return redwin/simulations


def single_game(io=True):
    """Create a game and have two agents play it."""

    game = Game([['-' for i in range(8)] for j in range(8)])   # 8x8 empty board
    if io:
        game.display()

    maxplayer = MinimaxAgent('R')
    minplayer = RandomAgent('B')

    while True:

        m = maxplayer.move(game)
        game = game.neighbor(m, maxplayer.color)
        if io:
            time.sleep(1)
            game.display()

        if game.winning_state() is not None:
            break

        m = minplayer.move(game)
        game = game.neighbor(m, minplayer.color)
        if io:
            time.sleep(1)
            game.display()

        if game.winning_state() is not None:
            break

    if game.winning_state() == float("inf"):
        print("RED WINS!")
    elif game.winning_state() == float("-inf"):
        print("BLACK WINS!")
    elif game.winning_state() == 0:
        print("TIE!")

    return game


if __name__ == '__main__':
    single_game(io=True)
    #tournament(simulations=50)
