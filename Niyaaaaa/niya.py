import random

class Board:
    def __init__(self):
        self.num_players = 2
        self.rows = 4
        self.cols = 4
        self.symbols = [
            ('L', 'F'), ('I', 'B'), ('I', 'F'), ('P', 'R'), 
            ('C', 'F'), ('P', 'F'), ('C', 'B'), ('C', 'S'),
            ('P', 'S'), ('L', 'S'), ('C', 'R'), ('I', 'S'),
            ('L', 'R'), ('I', 'R'), ('L', 'B'), ('P', 'B')
        ]
        self.first_move = True

    def starting_state(self):
        shuffled_symbols = self.symbols.copy()
        random.shuffle(shuffled_symbols)
        board = tuple(tuple(shuffled_symbols[i:i+4]) for i in range(0, 16, 4))
        return board

    def display(self, state, action):
        piece = {1: "○", 2: "●"}
        header = "   " + "  ".join(str(i) for i in range(self.cols))
        bar = "+---" * self.cols + "+"
        
        rows = [
            "{}|{}|{}|{}|{}|".format(
                i,
                piece.get(state[i][0], " ") if state[i][0] in piece else state[i][0],
                piece.get(state[i][1], " ") if state[i][1] in piece else state[i][1],
                piece.get(state[i][2], " ") if state[i][2] in piece else state[i][2],
                piece.get(state[i][3], " ") if state[i][3] in piece else state[i][3]
            ) for i in range(self.rows)
        ]
        
        board_str = "\n".join([header, bar] + rows + [bar])
        
        msg = "Player {} to move.".format(self.current_player(state))
        if action is not None:
            row, col = action
            msg = "Played: ({}, {})\n".format(row, col) + msg
        
        return board_str + "\n" + msg

    def legal_actions(self, state):
        legal_moves = []
        
        for r in range(self.rows):
            for c in range(self.cols):
                if state[r][c] not in {1, 2}:  
                    legal_moves.append((r, c))  # Return as tuple (row, column)

        return legal_moves

    def next_state(self, history, action):
        state = history[-1]
        new_board = [list(row) for row in state]
        
        row, col = action  # Unpack row and column from tuple
        
        player = self.current_player(state)
        
        new_board[row][col] = player  # Use player number instead of symbols
        
        return tuple(tuple(row) for row in new_board)

    def winner(self, state):
        for i in range(self.rows):
            if all(state[i][j] == 1 for j in range(self.cols)):
                return 1
            if all(state[i][j] == 2 for j in range(self.cols)):
                return 2

        for j in range(self.cols):
            if all(state[i][j] == 1 for i in range(self.rows)):
                return 1
            if all(state[i][j] == 2 for i in range(self.rows)):
                return 2

        if all(state[i][i] == 1 for i in range(self.rows)):
            return 1  
        if all(state[i][i] == 2 for i in range(self.rows)):
            return 2

        if all(state[i][self.cols - 1 - i] == 1 for i in range(self.rows)):
            return 1  
        if all(state[i][self.cols - 1 - i] == 2 for i in range(self.rows)):
            return 2

        return 0  

    def is_ended(self, state):
        return bool(self.winner(state)) or all(cell in {1, 2} for row in state for cell in row)

    def current_player(self, state):
        return 1 if sum(cell in {1, 2} for row in state for cell in row) % 2 == 0 else 2

    def previous_player(self, state):
        return 3 - self.current_player(state)

    def win_values(self, state):
        winner = self.winner(state)
        
        if winner == 1:
            return {1: 1, 2: 0}   
        elif winner == 2:
            return {1: 0, 2: 1}   
        elif winner == -1:
            return {1: .5, 2: .5} 
        else:
            return {1: .0, 2: .0}     

    def to_json_action(self, action):
        return action
    
    def to_compact_state(self, state):
        compact_state = []
        
        for r in range(self.rows):
            row_repr = []
            for c in range(self.cols):
                cell_value = state[r][c]
                if cell_value == "○":
                    row_repr.append(1)   
                elif cell_value == "●":
                    row_repr.append(2)   
                else:
                    row_repr.append(0)   
            compact_state.append(row_repr)
        
        return compact_state


# Example usage
if __name__ == "__main__":
    board = Board()
    initial_state = board.starting_state()
    print("Initial game board:")
    print(board.display(initial_state, None))