import sys

import pygame as pg

# Initialize Pygame
pg.init()

# Window settings
WIDTH = 400
HEIGHT = 500
BOARD_SIZE = 400
CELL_SIZE = BOARD_SIZE // 3
FPS = 30

WHITE = (255, 255, 255)
BLACK = (25, 25, 35)
RED = (240, 70, 70)
BLUE = (60, 130, 240)
GRAY = (190, 195, 205)

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Tic-Tac-Toe")

clock = pg.time.Clock()
font = pg.font.Font(None, 32)

# Game state
board = [[None for _ in range(3)] for _ in range(3)]
current_player = "X"
winner = None
draw = False
game_over_time = None


def draw_board():
    screen.fill(WHITE)

    # Grid lines
    for i in range(1, 3):
        pg.draw.line(
            screen, BLACK,
            (i * CELL_SIZE, 0),
            (i * CELL_SIZE, BOARD_SIZE), 5
        )
        pg.draw.line(
            screen, BLACK,
            (0, i * CELL_SIZE),
            (BOARD_SIZE, i * CELL_SIZE), 5
        )

    # Draw X and O
    for row in range(3):
        for col in range(3):
            x = col * CELL_SIZE
            y = row * CELL_SIZE

            if board[row][col] == "X":
                margin = 30
                pg.draw.line(
                    screen, BLUE,
                    (x + margin, y + margin),
                    (x + CELL_SIZE - margin, y + CELL_SIZE - margin), 8
                )
                pg.draw.line(
                    screen, BLUE,
                    (x + CELL_SIZE - margin, y + margin),
                    (x + margin, y + CELL_SIZE - margin), 8
                )

            elif board[row][col] == "O":
                pg.draw.circle(
                    screen, RED,
                    (x + CELL_SIZE // 2, y + CELL_SIZE // 2),
                    45, 8
                )

    # Status bar
    pg.draw.rect(screen, BLACK, (0, BOARD_SIZE, WIDTH, 100))

    if winner:
        message = f"{winner} wins! Click to restart"
    elif draw:
        message = "Draw! Click to restart"
    else:
        message = f"{current_player}'s turn"

    text = font.render(message, True, WHITE)
    screen.blit(text, text.get_rect(center=(WIDTH // 2, 450)))


def check_winner():
    # Rows
    for row in board:
        if row[0] and row[0] == row[1] == row[2]:
            return row[0]

    # Columns
    for col in range(3):
        if (board[0][col]
                and board[0][col] == board[1][col] == board[2][col]):
            return board[0][col]

    # Diagonals
    if board[0][0] and board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]

    if board[0][2] and board[0][2] == board[1][1] == board[2][0]:
        return board[0][2]

    return None


def reset_game():
    global board, current_player, winner, draw, game_over_time

    board = [[None for _ in range(3)] for _ in range(3)]
    current_player = "X"
    winner = None
    draw = False
    game_over_time = None


def handle_click(position):
    global current_player, winner, draw, game_over_time

    x, y = position

    # Ignore clicks outside the board
    if y >= BOARD_SIZE:
        return

    # Do not allow moves after the game ends
    if winner or draw:
        reset_game()
        return

    row = y // CELL_SIZE
    col = x // CELL_SIZE

    # Ignore occupied cells
    if board[row][col] is not None:
        return

    board[row][col] = current_player

    winner = check_winner()

    if winner:
        game_over_time = pg.time.get_ticks()
    elif all(cell is not None for row in board for cell in row):
        draw = True
        game_over_time = pg.time.get_ticks()
    else:
        current_player = "O" if current_player == "X" else "X"


# Main game loop
running = True

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            handle_click(event.pos)

        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_r:
                reset_game()

    # Automatically restart 2 seconds after a finished game
    if game_over_time is not None:
        if pg.time.get_ticks() - game_over_time >= 2000:
            reset_game()

    draw_board()
    pg.display.flip()
    clock.tick(FPS)

pg.quit()
sys.exit()
