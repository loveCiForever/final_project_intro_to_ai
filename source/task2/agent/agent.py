from .problem import TicTacToeProblem
import math
import random

class AIPlayer:
    
    def __init__(self, symbol, problem, max_depth=2):
        
        self.symbol = symbol
        self.opponent = "O" if symbol == "X" else "X"
        self.problem = problem
        self.max_depth = max_depth

    def get_move(self, state):
        
        valid_moves = self.problem.get_valid_moves(state)
        if not valid_moves:
            return None

        if self._is_first_move(state):
            center_moves = self._get_center_moves(valid_moves)
            if center_moves:
                return random.choice(center_moves)

        best_score = -math.inf
        best_moves = []
        alpha = -math.inf
        beta = math.inf

        for move in valid_moves:
            new_state = self.problem.make_move(state, move, self.symbol)
            if new_state is None:
                continue

            score = self._minimax(new_state, self.max_depth - 1, False, alpha, beta)
            
            if score > best_score:
                best_score = score
                best_moves = [move]
            elif score == best_score:
                best_moves.append(move)

            alpha = max(alpha, best_score)
            if beta <= alpha:
                break

        return random.choice(best_moves) if best_moves else valid_moves[0]

    def _minimax(self, state, depth, is_maximizing, alpha, beta):
        
        if depth == 0 or self.problem.is_terminal(state):
            return self.problem.evaluate_state(state, self.symbol)

        valid_moves = self.problem.get_valid_moves(state)
        
        if is_maximizing:
            max_eval = -math.inf
            for move in valid_moves:
                new_state = self.problem.make_move(state, move, self.symbol)
                if new_state is None:
                    continue
                eval = self._minimax(new_state, depth - 1, False, alpha, beta)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = math.inf
            for move in valid_moves:
                new_state = self.problem.make_move(state, move, self.opponent)
                if new_state is None:
                    continue
                eval = self._minimax(new_state, depth - 1, True, alpha, beta)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def _is_first_move(self, state):
        return all(cell == "" for row in state for cell in row)

    def _get_center_moves(self, valid_moves):
        center = self.problem.board_size // 2
        center_range = (center - 1, center, center + 1)
        return [(x, y) for x, y in valid_moves 
                if x in center_range and y in center_range] 