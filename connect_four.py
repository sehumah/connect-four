# import libraries
import sys
import math
import numpy as np
import pygame


""" define constant variables """
# colors
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# board's row & column size
ROW_COUNT = 6
COLUMN_COUNT = 7

# screen size, radius of circle, width and height & set size of GUI board
SQUARE_SIZE = 100
RADIUS = int(SQUARE_SIZE / 2 - 5)
WIDTH = COLUMN_COUNT * SQUARE_SIZE
HEIGHT = (ROW_COUNT + 1) * SQUARE_SIZE
SIZE = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size=SIZE)


def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0  # if condition is true, we can drop pieces there, else the column is occupied


def get_next_open_row(board, col):
    for row in range(ROW_COUNT):
        if board[row][col] == 0:
            return row


def print_board(board):
    print(np.flip(board, 0))  # np.flip reverses array elements order along the specified axis, preserving the shape of the array


def winning_move(board, piece):
    # check horizontal locations for the win
    for col in range(COLUMN_COUNT - 3):
        for row in range(ROW_COUNT):
            if board[row][col] == piece and board[row][col + 1] == piece and board[row][col + 2] == piece and board[row][col + 3] == piece:
                return True

    # check vertical locations for the win
    for col in range(COLUMN_COUNT - 3):
        for row in range(ROW_COUNT):
            if board[row][col] == piece and board[row + 1][col] == piece and board[row + 2][col] == piece and board[row + 3][col] == piece:
                return True

    # check positively sloped diagonals
    for col in range(COLUMN_COUNT - 3):
        for row in range(ROW_COUNT):
            if board[row][col] == piece and board[row + 1][col + 1] == piece and board[row + 2][col + 2] == piece and board[row + 3][col + 3] == piece:
                return True

    # check negatively sloped diagonals
    for col in range(COLUMN_COUNT - 3):
        for row in range(ROW_COUNT):
            if board[row][col] == piece and board[row - 1][col + 1] == piece and board[row - 2][col + 2] == piece and board[row - 3][col + 3] == piece:
                return True


def draw_board(board):  # draw GUI board
    for col in range(COLUMN_COUNT):
        for row in range(ROW_COUNT):
            pygame.draw.rect(surface=screen, color=BLUE, rect=(col * SQUARE_SIZE, row * SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(surface=screen, color=BLACK, center=(int(col * SQUARE_SIZE + SQUARE_SIZE / 2), int(row * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2)), radius=RADIUS)

    for col in range(COLUMN_COUNT):
        for row in range(ROW_COUNT):
            if board[row][col] == 1:  # player1's piece
                pygame.draw.circle(surface=screen, color=RED, center=(int(col * SQUARE_SIZE + SQUARE_SIZE / 2), HEIGHT - int(row * SQUARE_SIZE + SQUARE_SIZE / 2)), radius=RADIUS)
            elif board[row][col] == 2:  # player2's piece
                pygame.draw.circle(surface=screen, color=YELLOW, center=(int(col * SQUARE_SIZE + SQUARE_SIZE / 2), HEIGHT - int(row * SQUARE_SIZE + SQUARE_SIZE / 2)), radius=RADIUS)
    pygame.display.update()


def main():
    # get user's names
    # player1 = input("Player 1, enter your name: ")
    # player2 = input("Player 2, enter your name: ")

    # define things needed for gameplay
    board = create_board()
    print_board(board=board)
    game_over = False
    turn = 0

    # initialize game
    pygame.init()

    # call draw_board() again
    draw_board(board=board)
    pygame.display.update()

    # define font to be used
    font = pygame.font.SysFont(name='monospace', size=75)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(surface=screen, color=BLACK, rect=(0, 0, WIDTH, SQUARE_SIZE))
                posx = event.pos[0]
                if turn == 0:
                    pygame.draw.circle(surface=screen, color=RED, center=(posx, int(SQUARE_SIZE / 2)), radius=RADIUS)
                else:
                    pygame.draw.circle(surface=screen, color=YELLOW, center=(posx, int(SQUARE_SIZE / 2)), radius=RADIUS)

            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(surface=screen, color=BLACK, rect=(0, 0, WIDTH, SQUARE_SIZE))
                # ask for player1 input
                if turn == 0:
                    posx = event.pos[0]
                    # col = int(input("Player 1, make your selection (0-6): "))
                    col = int(math.floor(posx / SQUARE_SIZE))  # get player's column number
                    if is_valid_location(board=board, col=col):
                        row = get_next_open_row(board=board, col=col)
                        drop_piece(board=board, row=row, col=col, piece=1)
                        # check for winning move
                        if winning_move(board=board, piece=1):
                            label = font.render("Player 1 wins!", 1, RED)
                            # label = font.render(f"{player1} wins!", 1, RED)
                            screen.blit(label, (40, 10))
                            game_over = True
                # ask for player2 input
                else:
                    posx = event.pos[0]
                    # col = int(input("Player 2, make your selection (0-6): "))
                    col = int(math.floor(posx / SQUARE_SIZE))
                    # check if location is valid
                    if is_valid_location(board=board, col=col):
                        row = get_next_open_row(board=board, col=col)
                        drop_piece(board=board, row=row, col=col, piece=2)
                        # check for winning move
                        if winning_move(board=board, piece=2):
                            label = font.render("Player 2 wins!", 1, YELLOW)
                            # label = font.render(f"{player2} wins!", 1, YELLOW)
                            screen.blit(label, (40, 10))
                            game_over = True

                # update console and gui boards
                print_board(board=board)
                draw_board(board=board)
                print()

                # enable players to take turns
                turn += 1
                turn %= 2

                # wait before closing game window
                if game_over:
                    pygame.time.wait(3000)


if __name__ == '__main__':
    main()

# tutorial source: https://www.askpython.com/python/examples/connect-four-game

'''
Future work:
    1. modify and include AI functionality
    2. allow multiple rounds of gameplay and display player's info and scores on screen
    3. make an AI vs AI game
    4. build a connect four solving engine
'''
