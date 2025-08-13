import numpy as np
import random
import pygame
import sys
import math

# Board dimensions
ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE = 150
RADIUS = int(SQUARESIZE / 2 - 8)

# Screen dimensions
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE
size = (width, height)

# Colors
BLUE = (0, 102, 204)
BACKGROUND  = (173, 216, 230) 
RED = (255, 59, 48)
YELLOW = (255, 204, 0)

# Game variables
RED_COIN = 1
YELLOW_COIN = 2
EMPTY = 0
WINDOW_LENGTH = 4
AI_DIFFICULTY = 4

# Initialize Pygame
pygame.init()

# mixer module for sounds
pygame.mixer.init()
pygame.mixer.music.load("/mnt/c/Ammar/CS50/Final-Project/Static/Sounds/game-background-sound.ogg")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)

myfont = pygame.font.SysFont("monospace", 75)



def main():
    board = create_board()
    print_board(board)
    game_over = False
    turn = 0

    # Initialize the main screen
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Connect Four")

    draw_board(board, screen)
    pygame.display.update()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BACKGROUND, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                if turn == 0:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BACKGROUND, (0, 0, width, SQUARESIZE))
                # Ask for Player 1 Input
                if turn == 0:
                    posx = event.pos[0]
                    col = int(math.floor(posx/SQUARESIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, RED_COIN)

                        if winning_move(board, RED_COIN):
                            label = myfont.render("Player 1 wins!!", 1, RED)
                            pygame.mixer.music.stop()
                            screen.blit(label, (40,10))
                            game_over = True

                        print_board(board)
                        draw_board(board, screen)

                        turn += 1
                        turn = turn % 2

        # AI turn
        if turn == 1 and not game_over:
            col, minimax_score = minimax(board, AI_DIFFICULTY, -math.inf, math.inf, True)

            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, YELLOW_COIN)

                if winning_move(board, YELLOW_COIN):
                    label = myfont.render("AI wins!!", 1, YELLOW)
                    pygame.mixer.music.stop()
                    screen.blit(label, (40,10))
                    game_over = True

                print(col, minimax_score)
                print_board(board)
                draw_board(board, screen)

                turn += 1
                turn = turn % 2

        if game_over:
            pygame.time.wait(3000)



# 2D array representing the board
def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


# Prints the board in the console
def print_board(board):
    # Flips the board so that the pieces are printed from the bottom up
    print(np.flip(board, 0))


# Draws the board in the Pygame window
def draw_board(board, screen):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BACKGROUND, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
    
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):        
            if board[r][c] == RED_COIN:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == YELLOW_COIN: 
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()


# Check's if there is an empty spot in the column
def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0


# gets the bottom most empty row in the column
def get_next_open_row(board, col):

    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


# puts 1, 0, 2 in 2D array
def drop_piece(board, row, col, piece):
    board[row][col] = piece


# Matches the peice with the board rows and coulmn with if conditions
def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check positively sloped diagonals
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Check negatively sloped diagonals
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

# Minimax Algorithm for optimal move
def minimax(board, depth, alpha, beta, MAX):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    # Resulting score after game ends
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, YELLOW_COIN):
                return (None, 100000000000000)
            elif winning_move(board, RED_COIN):
                return (None, -10000000000000)
            else: # Game is over, no more valid moves
                return (None, 0)
        else: # Depth is zero
            return (None, score_position(board, YELLOW_COIN))

    if MAX:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, YELLOW_COIN)
            new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else: # Minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, RED_COIN)
            new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value


# Get all available columns
def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations

# Check if the game is over
def is_terminal_node(board):
    return winning_move(board, RED_COIN) or winning_move(board, YELLOW_COIN) or len(get_valid_locations(board)) == 0


def evaluate_window(window, piece):
    score = 0
    opp_piece = RED_COIN
    if piece == RED_COIN:
        opp_piece = YELLOW_COIN

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score


def score_position(board, piece):
    score = 0

    # Score center column
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    # Score Horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COLUMN_COUNT-3):
            window = row_array[c:c+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Score Vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(ROW_COUNT-3):
            window = col_array[r:r+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Score positive sloped diagonal
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    # Score negative sloped diagonal
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score


if __name__ == "__main__":
    main()