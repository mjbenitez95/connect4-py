import numpy as np
import random

rand = random.Random()

class Connect4():
  NUM_ROWS = 6
  NUM_COLS = 7
  NUM_TO_WIN = 4

  def __init__(self):
    self.board = np.zeros((self.NUM_ROWS, self.NUM_COLS))

  def __str__(self):
    str_board = "\n" + str(self.board).replace("0.", "_").replace("-1.", " O").replace("1.", "X") + "\n"
    str_board = str_board.replace("[", " ").replace("]", " ")
    return str_board

  def get_available_moves(self):
    return [m for m in range(self.NUM_COLS) if self.board[0][m] == 0]

  def make_move(self, move):
    if np.sum(self.board) == 0:
      player = 1
    else:
      player = -1

    j = 0

    # this will "drop" the move to the lowest open space
    while j + 1 < self.NUM_ROWS and self.board[j+1][move] == 0: j += 1

    self.board[j][move] = player

  def get_winner(self):
    for i in range(self.NUM_ROWS - self.NUM_TO_WIN + 1):
      for j in range(self.NUM_COLS - self.NUM_TO_WIN + 1):

        sub_board = self.board[i:(i + self.NUM_TO_WIN), j:(j + self.NUM_TO_WIN)]
        if np.max(np.abs(np.sum(sub_board, 0))) == self.NUM_TO_WIN:
          return True
        if np.max(np.abs(np.sum(sub_board, 1))) == self.NUM_TO_WIN:
          return True
        elif np.abs(sum([sub_board[k, k] for k in range(self.NUM_TO_WIN)])) == self.NUM_TO_WIN: # diag
          return True
        elif np.abs(sum([sub_board[k, self.NUM_TO_WIN - 1 - k] for k in range(self.NUM_TO_WIN)])) == self.NUM_TO_WIN: # opp diag
          return True
    return False

def main():
  XO = {-1: "O", 0: "Nobody", 1: "X"}
  my_game = Connect4()
  moves = my_game.get_available_moves()
  print(my_game)

  # game always starts with 1
  player = 1

  # select randomly if human is 1 or -1
  human_player = rand.choice([1, -1])

  # when moves = [], we have a draw
  while moves != []:
    if player == human_player:
      print(f"Available moves are: {moves}")
      move = int(input("Enter human move: "))
    else:
      # computer makes a random move
      move = rand.choice(moves) 
    
    my_game.make_move(move)
    print(my_game)

    if my_game.get_winner():
      print(f"{XO[player]} wins!")
      break

    moves = my_game.get_available_moves()
    player = -player

if __name__ == "__main__":
  main()
