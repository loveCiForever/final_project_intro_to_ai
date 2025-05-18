import pygame
import sys
import time

BOARD_SIZE = 9
CELL_SIZE = 60
K_TO_WIN = 4
WIDTH = HEIGHT = CELL_SIZE * BOARD_SIZE
LINE_COLOR = (0, 0, 0)
X_COLOR = (200, 0, 0)
O_COLOR = (0, 0, 200)
BG_COLOR = (255, 255, 255)
LINE_WIDTH = 5  # Width of the winning line

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe 9x9 (K=4)")
font = pygame.font.SysFont(None, CELL_SIZE // 2)
winner_font = pygame.font.SysFont(None, 74)  # Larger font for winner message

board = [["" for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

class Player:
    def __init__(self, symbol):
        self.symbol = symbol

    def get_move(self, board):
        raise NotImplementedError

class HumanPlayer(Player):
    def get_move(self, board):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos[0] // CELL_SIZE, event.pos[1] // CELL_SIZE
                    if board[y][x] == "":
                        return x, y

class RandomAgent(Player):
    def get_move(self, board):
        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                if board[y][x] == "":
                    return x, y
        return None

def draw_board():
    screen.fill(BG_COLOR)
    for row in range(1, BOARD_SIZE):
        pygame.draw.line(screen, LINE_COLOR, (0, row * CELL_SIZE), (WIDTH, row * CELL_SIZE), 1)
    for col in range(1, BOARD_SIZE):
        pygame.draw.line(screen, LINE_COLOR, (col * CELL_SIZE, 0), (col * CELL_SIZE, HEIGHT), 1)

    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            if board[y][x] != "":
                draw_mark(x, y, board[y][x])
    pygame.display.flip()

def draw_mark(x, y, player):
    mark = font.render(player, True, X_COLOR if player == "X" else O_COLOR)
    rect = mark.get_rect(center=(x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2))
    screen.blit(mark, rect)

def draw_winner_line(positions, player):
    color = X_COLOR if player == "X" else O_COLOR
    start_pos = positions[0]
    end_pos = positions[-1]
    
    # Convert board positions to screen coordinates (center of cells)
    start_x = start_pos[1] * CELL_SIZE + CELL_SIZE // 2
    start_y = start_pos[0] * CELL_SIZE + CELL_SIZE // 2
    end_x = end_pos[1] * CELL_SIZE + CELL_SIZE // 2
    end_y = end_pos[0] * CELL_SIZE + CELL_SIZE // 2
    
    pygame.draw.line(screen, color, (start_x, start_y), (end_x, end_y), LINE_WIDTH)
    pygame.display.flip()

def display_winner_message(winner):
    color = X_COLOR if winner == "X" else O_COLOR
    text = f"Player {winner} Wins!"
    text_surface = winner_font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(WIDTH//2, HEIGHT//2))
    
    # Draw semi-transparent background
    s = pygame.Surface((WIDTH, 100))
    s.set_alpha(128)
    s.fill(BG_COLOR)
    screen.blit(s, (0, HEIGHT//2 - 50))
    
    # Draw text
    screen.blit(text_surface, text_rect)
    pygame.display.flip()

def check_winner():
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            if board[y][x] != "":
                player = board[y][x]
                # Check horizontal
                if x <= BOARD_SIZE - K_TO_WIN:
                    if all(board[y][x+i] == player for i in range(K_TO_WIN)):
                        positions = [(y, x+i) for i in range(K_TO_WIN)]
                        return {'winner': player, 'positions': positions}
                
                # Check vertical
                if y <= BOARD_SIZE - K_TO_WIN:
                    if all(board[y+i][x] == player for i in range(K_TO_WIN)):
                        positions = [(y+i, x) for i in range(K_TO_WIN)]
                        return {'winner': player, 'positions': positions}
                
                # Check diagonal
                if x <= BOARD_SIZE - K_TO_WIN and y <= BOARD_SIZE - K_TO_WIN:
                    if all(board[y+i][x+i] == player for i in range(K_TO_WIN)):
                        positions = [(y+i, x+i) for i in range(K_TO_WIN)]
                        return {'winner': player, 'positions': positions}
                
                # Check anti-diagonal
                if x <= BOARD_SIZE - K_TO_WIN and y >= K_TO_WIN - 1:
                    if all(board[y-i][x+i] == player for i in range(K_TO_WIN)):
                        positions = [(y-i, x+i) for i in range(K_TO_WIN)]
                        return {'winner': player, 'positions': positions}
    return None

def is_board_full():
    return all(board[y][x] != "" for y in range(BOARD_SIZE) for x in range(BOARD_SIZE))

def main():
    draw_board()
    from agent.problem import TicTacToeProblem
    from agent.agent import AIPlayer
    problem = TicTacToeProblem()
    player_X = HumanPlayer("X")   
    player_O = AIPlayer("O", problem)     
    current_player = player_X

    while True:
        draw_board()

        move = current_player.get_move(board)
        if move is None:
            print("Tie")
            break
        x, y = move
        if board[y][x] == "":
            board[y][x] = current_player.symbol
        else:
            continue  

        draw_board()
        winner_info = check_winner()
        if winner_info:
            winner = winner_info['winner']
            draw_winner_line(winner_info['positions'], winner)
            display_winner_message(winner)
            time.sleep(2)
            break
        elif is_board_full():
            print("Draw!")
            time.sleep(2)
            break

        current_player = player_O if current_player == player_X else player_X

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
