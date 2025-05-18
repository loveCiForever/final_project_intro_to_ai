class TicTacToeProblem:
    
    def __init__(self, board_size=9, win_length=4, defense_weight=1.2):
        self.board_size = board_size
        self.win_length = win_length
        self.defense_weight = defense_weight  # Defense weight (default 1.2)
        
        # Cache for directions and positions
        self.directions = [(1,0), (0,1), (1,1), (1,-1)]
        self.center = self.board_size // 2
        self.center_area = [(i, j) 
                           for i in range(self.center-1, self.center+2)
                           for j in range(self.center-1, self.center+2)]
        
        # Base scores for different patterns
        self.BASE_SCORES = {
            'CENTER': 30, # Center position
        }

    def get_valid_moves(self, state):
        valid_moves = []
        for i in range(self.board_size):
            for j in range(self.board_size):
                if state[i][j] == "":
                    valid_moves.append((j, i))
        return valid_moves

    def make_move(self, state, move, player):
        x, y = move
        if state[y][x] == "":
            new_state = [row[:] for row in state]
            new_state[y][x] = player
            return new_state
        return None

    def is_terminal(self, state):
        return self.get_winner(state) is not None or self.is_board_full(state)

    def get_winner(self, state):
        # Check horizontal lines
        for i in range(self.board_size):
            for j in range(self.board_size - self.win_length + 1):
                if state[i][j] != "" and all(state[i][j] == state[i][j+k] for k in range(self.win_length)):
                    return state[i][j]

        # Check vertical lines
        for i in range(self.board_size - self.win_length + 1):
            for j in range(self.board_size):
                if state[i][j] != "" and all(state[i][j] == state[i+k][j] for k in range(self.win_length)):
                    return state[i][j]

        # Check main diagonal
        for i in range(self.board_size - self.win_length + 1):
            for j in range(self.board_size - self.win_length + 1):
                if state[i][j] != "" and all(state[i][j] == state[i+k][j+k] for k in range(self.win_length)):
                    return state[i][j]

        # Check anti-diagonal
        for i in range(self.board_size - self.win_length + 1):
            for j in range(self.win_length - 1, self.board_size):
                if state[i][j] != "" and all(state[i][j] == state[i+k][j-k] for k in range(self.win_length)):
                    return state[i][j]

        return None

    def is_board_full(self, state):
        return all(cell != "" for row in state for cell in row)

    def evaluate_state(self, state, player):
        opponent = "O" if player == "X" else "X"
        score = 0
        def evaluate_line(line, symbol):
            points = 0
            str_line = ''.join(cell if cell != "" else "." for cell in line)

            patterns = {
                f'{symbol}{symbol}{symbol}{symbol}': 10000,  # Win pattern
                f'.{symbol}{symbol}{symbol}.': 1000,        # Three in a row with both ends open
                f'{symbol}{symbol}{symbol}.': 500,          # Three in a row with one end open
                f'.{symbol}{symbol}{symbol}': 500,          # Three in a row with one end open
                f'.{symbol}{symbol}.': 100,                 # Two in a row with both ends open
                f'{symbol}{symbol}.': 50,                   # Two in a row with one end open
                f'.{symbol}{symbol}': 50,                   # Two in a row with one end open
            }

            for pattern, value in patterns.items():
                count = str_line.count(pattern)
                points += count * value

            return points

        def get_lines(state):
            lines = []
            size = self.board_size

            # Get rows and columns
            for i in range(size):
                lines.append([state[i][j] for j in range(size)])  # row
                lines.append([state[j][i] for j in range(size)])  # column

            # Get diagonals (main and anti)
            for r in range(size - self.win_length + 1):
                for c in range(size - self.win_length + 1):
                    # Main diagonal
                    diag1 = [state[r+i][c+i] for i in range(self.win_length)]
                    lines.append(diag1)
                    
                    # Anti diagonal
                    if c + self.win_length <= size:
                        diag2 = [state[r+i][c+self.win_length-1-i] for i in range(self.win_length)]
                        lines.append(diag2)

            return lines

        # Evaluate all lines
        for line in get_lines(state):
            # Attack score
            score += evaluate_line(line, player)
            # Defense score (with weight)
            score -= evaluate_line(line, opponent) * self.defense_weight

        # Bonus for center positions
        for i, j in self.center_area:
            if state[i][j] == player:
                score += self.BASE_SCORES['CENTER']
            elif state[i][j] == opponent:
                score -= self.BASE_SCORES['CENTER'] * self.defense_weight

        return score 