from niya import Board  
from uct import UCTWins  

def main():
    board = Board()
    mcts = UCTWins(board, time=5)  
    state = board.starting_state()

    print("Initial game board:")
    print(board.display(state, None))

    while not board.is_ended(state):
        current_player = board.current_player(state)

        if current_player == 1:  
            print(f"AI's Turn (Player {current_player}):")
            legal_actions = board.legal_actions(state)
            print("Legal actions:", legal_actions)

            mcts.update(state)
            mcts.update_legal_actions(legal_actions)  
            
            best_action_info = mcts.get_action()
            action_tuple = best_action_info['message']
            
            print(f"Best action chosen by MCTS: {action_tuple}")

            # Apply the AI move and get the new state
            state = board.next_state([state], action_tuple)

        else:  
            print(f"Player {current_player}'s Turn:")
            print(board.display(state, None))
            
            legal_actions = board.legal_actions(state)
            print("Your turn! Choose a position to place your piece:")
            print("Legal moves:", legal_actions)

            while True:
                try:
                    row = int(input("Enter row (0-3): "))
                    col = int(input("Enter column (0-3): "))
                    action_tuple = (row, col) 
                    if action_tuple in legal_actions:
                        break
                    else:
                        print("Invalid move. Please choose a valid position.")
                except ValueError:
                    print("Invalid input. Please enter numbers between 0 and 3.")

            # Apply the user's move and get the new state
            state = board.next_state([state], action_tuple)

        # Display the updated board after each move
        print("Updated game board:")
        print(board.display(state, action_tuple))

    winner = board.winner(state)
    if winner == 3:
        print("The game is a draw!")
    else:
        print(f"Player {winner} wins!")

if __name__ == "__main__":
    main()