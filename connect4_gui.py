from connect4 import Connect4
from dotenv import load_dotenv
from openai import OpenAI
import os, math, random, pygame

rand = random.Random()
USE_AI = True
SETUP_MESSAGE = "You are a Connect 4 AI. Follow these rules:\
     1. If you can win with your next move, do so.\
     2. If the opponent can win with their next move, block them.\
     3. Otherwise, aim to set up opportunities for future wins, such as\
     creating multiple threats in one move.\
     4. Prioritize control of the center column, as it increases winning\
     chances.\
     5. Avoid placing pieces in columns that allow the opponent to win.\
     The board state is provided below as\
     a 2D grid. Each cell is 0 (empty), -1 (AI's pieces), or 1 (human's\
     pieces). Return the column index (0-6) where you want to drop your piece,\
     based on the current state. Your response should contain the numerical\
     index and absolutely nothing more."

COLORS = {
    "RED": (255, 0, 0),
    "BLUE": (0, 0, 255),
    "BLACK": (0, 0, 0),
    "YELLOW": (255, 255, 0),
    "WHITE": (255, 255, 255),
}

PIECE_COLORS = [COLORS["BLACK"], COLORS["RED"], COLORS["YELLOW"]]


class Connect4_Gui(Connect4):
    SQUARE_SIZE = 100
    WIDTH = Connect4.NUM_COLS * SQUARE_SIZE
    HEIGHT = (1 + Connect4.NUM_ROWS) * SQUARE_SIZE

    SCREEN_SIZE = (WIDTH, HEIGHT)
    RADIUS = int(SQUARE_SIZE / 2 - 5)
    SCREEN = pygame.display.set_mode(SCREEN_SIZE)

    def load_ai_client(self):
        print(os.environ.get("OPENAI_API_KEY"))
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        return client

    def draw_board(self):
        for column in range(self.NUM_COLS):
            for row in range(self.NUM_ROWS):
                # draw board frame
                location_size = (
                    column * self.SQUARE_SIZE,
                    (row + 1) * self.SQUARE_SIZE,
                    self.SQUARE_SIZE,
                    self.SQUARE_SIZE,
                )
                pygame.draw.rect(self.SCREEN, COLORS["BLUE"], location_size)

        for column in range(self.NUM_COLS):
            for row in range(self.NUM_ROWS):
                # draw pieces colored by which player is at that space
                player_at_space = int(self.board[row][column])
                location = (
                    int((column + 0.5) * self.SQUARE_SIZE),
                    int((row + 1.5) * self.SQUARE_SIZE),
                )
                pygame.draw.circle(
                    self.SCREEN, PIECE_COLORS[player_at_space], location, self.RADIUS
                )

        pygame.display.update()

    def run_game(self):
        client = None
        if USE_AI:
            client = self.load_ai_client()

        pygame.init()
        my_font = pygame.font.SysFont("monospace", 75)
        self.draw_board()
        pygame.display.update()

        moves = self.get_available_moves()
        player = 1
        human_player = rand.choice([1])
        winner = False
        exit_flag = False

        while moves != [] and winner == False and exit_flag == False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_flag = True

                # draw hovering piece
                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(
                        self.SCREEN,
                        COLORS["BLACK"],
                        (0, 0, self.WIDTH, self.SQUARE_SIZE),
                    )

                    position_x = event.pos[0]
                    pygame.draw.circle(
                        self.SCREEN,
                        PIECE_COLORS[player],
                        (position_x, int(self.SQUARE_SIZE / 2)),
                        self.RADIUS,
                    )

                    pygame.display.update()

                # handle human move
                if player == human_player and event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.draw.rect(
                        self.SCREEN,
                        COLORS["BLACK"],
                        (0, 0, self.WIDTH, self.SQUARE_SIZE),
                    )
                    position_x = event.pos[0]
                    move = int(math.floor(position_x / self.SQUARE_SIZE))

                    if move in moves:
                        self.make_move(move)
                        self.draw_board()
                        if self.get_winner():
                            label = my_font.render("You win!", 1, PIECE_COLORS[player])
                            self.SCREEN.blit(label, (40, 10))
                            self.draw_board()
                            winner = True
                            break

                        player = -player

                # make CPU move
                elif player == -human_player:
                    move = rand.choice(moves)
                    if USE_AI:
                        completion = client.chat.completions.create(
                            model="gpt-3.5-turbo",
                            messages=[
                                {
                                    "role": "system",
                                    "content": SETUP_MESSAGE,
                                },
                                {
                                    "role": "user",
                                    "content": str(self.board),
                                },
                            ],
                        )
                        move = int(completion.choices[0].message.content)

                    if move in moves:
                        self.make_move(move)
                        self.draw_board()
                        if self.get_winner():
                            label = my_font.render("CPU wins!", 1, PIECE_COLORS[player])
                            self.SCREEN.blit(label, (40, 10))
                            self.draw_board()
                            winner = True
                            break

                        player = -player

            moves = self.get_available_moves()

        if winner == False and moves == []:
            label = my_font.render("It's a draw!", 1, COLORS["WHITE"])
            self.SCREEN.blit(label, (40, 10))
            self.draw_board()

        while exit_flag == False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_flag = True

        pygame.quit()


def main():
    load_dotenv()
    my_game = Connect4_Gui()
    my_game.run_game()


if __name__ == "__main__":
    main()
