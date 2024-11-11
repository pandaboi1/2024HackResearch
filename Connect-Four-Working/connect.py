import six
from six.moves import range


class Board(object):
    num_players = 2
    rows = 6
    cols = 7

    def __init__(self, *args, **kwargs):
        pass

    def starting_state(self):
        return (0, 0, 1)

    def display(self, state, action):
        piece = {0: " ", 1: u"\u25cb", 2: u"\u25cf"}
        header = "   {0}".format(
            " ".join(str(i) for i in range(self.cols)))
        bar = "  +{0}+".format("-"*(2*self.cols-1))
        msg = "{0}Player {1} to move.".format(
            "Played: {0}\n".format(
                self.to_notation(self.to_compact_action(action))) if action else '',
            state['player']
        )

        P = [[0 for c in range(self.cols)] for r in range(self.rows)]
        for p in state['pieces']:
            P[p['row']][p['column']] = p['player']

        board = u"\n".join(
            u"  |{0}|".format(u"|".join(piece[x] for x in row))
            for row in reversed(P)
        )

        board = u"\n".join((header, bar, board, bar, header, msg))
        return board

    def to_compact_state(self, data):
        player = data['player']
        state = {1: 0, 2: 0}
        for item in data['pieces']:
            index = 1 << (item['column'] * self.rows + item['row'])
            state[item['player']] += index

        return (state[1], state[2], player)

    def to_json_state(self, state):
        p1, p2, player = state
        pieces = []
        for c in range(self.cols):
            for r in range(self.rows):
                index = 1 << (c * self.rows + r)
                if index & p1:
                    pieces.append({'type': 'disc', 'player': 1, 'row': r, 'column': c})
                if index & p2:
                    pieces.append({'type': 'disc', 'player': 2, 'row': r, 'column': c})

        return {
            'pieces': pieces,
            'player': player,
            'previous_player': 3 - player,
        }

    def to_compact_action(self, action):
        return action['column']

    def to_json_action(self, action):
        return {'column': action}

    def from_notation(self, notation):
        return int(notation)

    def to_notation(self, action):
        return str(action)

    def is_legal(self, state, action):
        p1, p2, player = state
        occupied = p1 | p2
        column = (occupied >> (self.rows * action)) & 0b111111
        return column <= 0b11111

    def legal_actions(self, state):
        p1, p2, player = state
        occupied = p1 | p2
        legal = []
        for c in range(self.cols):
            column = (occupied >> (self.rows * c)) & 0b111111
            if column != 0b111111:  # Check if the column is not full
                legal.append(c)
        return legal

    def next_state(self, history, action):
        state = history[-1]
        p1, p2, player = state
        occupied = p1 | p2
        column = (occupied >> (self.rows * action)) & 0b111111
        column += 1
        column <<= self.rows * action
        if player == 1:
            p1 |= column
        else:
            p2 |= column
        return (p1, p2, 3 - player)

    def previous_player(self, state):
        return 3 - state[-1]

    def current_player(self, state):
        return state[-1]

    def winner(self, state):
        p1, p2, player = state
        occupied = p1 | p2

        top_row_mask = 0x1f7df7df7df
        bottom_row_mask = 0x3efbefbefbe

        for p_num, p_val in ((1, p1), (2, p2)):
            # W
            g = p_val
            g &= (g >> 6) & p_val
            g &= (g >> 6) & p_val
            g &= (g >> 6) & p_val
            if g:
                return p_num

            # E
            g = p_val
            g &= (g << 6) & p_val
            g &= (g << 6) & p_val
            g &= (g << 6) & p_val
            if g:
                return p_num

            # N
            g = p_val
            g &= (g << 1) & p_val & bottom_row_mask
            g &= (g << 1) & p_val & bottom_row_mask
            g &= (g << 1) & p_val & bottom_row_mask
            if g:
                return p_num

            # S
            g = p_val
            g &= (g >> 1) & p_val & top_row_mask
            g &= (g >> 1) & p_val & top_row_mask
            g &= (g >> 1) & p_val & top_row_mask
            if g:
                return p_num

            # NW
            g = p_val
            g &= (g >> 5) & p_val & bottom_row_mask
            g &= (g >> 5) & p_val & bottom_row_mask
            g &= (g >> 5) & p_val & bottom_row_mask
            if g:
                return p_num

            # NE
            g = p_val
            g &= (g << 7) & p_val & bottom_row_mask
            g &= (g << 7) & p_val & bottom_row_mask
            g &= (g << 7) & p_val & bottom_row_mask
            if g:
                return p_num

            # SW
            g = p_val
            g &= (g >> 7) & p_val & top_row_mask
            g &= (g >> 7) & p_val & top_row_mask
            g &= (g >> 7) & p_val & top_row_mask
            if g:
                return p_num

            # SE
            g = p_val
            g &= (g << 5) & p_val & top_row_mask
            g &= (g << 5) & p_val & top_row_mask
            g &= (g << 5) & p_val & top_row_mask
            if g:
                return p_num

        if occupied == 0x3ffffffffff:
            return 3

        return 0

    def is_ended(self, state):
        return bool(self.winner(state))

    def win_values(self, state):
        winner = self.winner(state)
        if not winner:
            return

        if winner == 3:
            return {1: 0.5, 2: 0.5}
        return {winner: 1, 3 - winner: 0}

    points_values = win_values

    def winner_message(self, winners):
        winners = sorted((v, k) for k, v in six.iteritems(winners))
        value, winner = winners[-1]
        if value == 0.5:
            return "Stalemate."
        return "Winner: Player {0}.".format(winner)
