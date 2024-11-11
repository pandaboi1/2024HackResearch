from connect import Board  # Import Board class from board.py
from uct import UCTWins  # Import MCTS algorithm

def main():
    # Initialize the game board for Connect Four
    board = Board()

    # Initialize the MCTS search algorithm
    mcts = UCTWins(board, time=0.005)  # Run MCTS for 5 seconds

    # Start with the initial game state
    state = board.starting_state()  # This should be a tuple (p1, p2, player)

    # Display the initial state of the board
    print("Initial game board:")
    print(board.display(board.to_json_state(state), None))

    # Main game loop
    while not board.is_ended(state):
        # Run MCTS to get the best action (AI move)
        legal_actions = board.legal_actions(state)
        print(f"Legal actions: {legal_actions}")
        state_dict = {
                    'pieces': board.to_json_state(state)['pieces'],
                    'player': state[2]
                }
        mcts.update(state_dict)
        mcts.update_legal_actions(legal_actions)  # Update legal actions in MCTS

        best_action = mcts.get_action()

        # The 'message' field contains the best action's column
        action_column = best_action['message']['column']

        print(f"Best action chosen by MCTS: Column {action_column}")

        # Apply the MCTS move and get the new state
        state = board.next_state([state], action_column)

        # Display the updated board after the MCTS move
        print("Updated game board after MCTS move:")
        print(board.display(board.to_json_state(state), best_action['message']))

        # Check if the game has ended after the MCTS move
        if board.is_ended(state):
            break

        # Now, ask the user for their move
        legal_actions = board.legal_actions(state)
        print("Your turn! Choose a column to drop your piece:")
        print("Legal columns:", legal_actions)

        while True:
            try:
                # Get user input for the column
                user_input = int(input("Enter a column number (0-6): "))
                if user_input not in legal_actions:
                    print("Invalid move. Please choose a valid column from the legal moves.")
                else:
                    break
            except ValueError:
                print("Invalid input. Please enter a number between 0 and 6.")

        # Apply the user's move and get the new state
        state = board.next_state([state], user_input)

        # Display the updated board after the user's move
        print("Updated game board after your move:")
        print(board.display(board.to_json_state(state), {'column': user_input}))

        # Check if the game has ended after the user's move
        if board.is_ended(state):
            # Game has ended
            break
    winner = board.winner(state)
    if winner == 3:
        print("The game is a draw!")
    else:
        print(f"Player {winner} wins!")


if __name__ == "__main__":
    main()
