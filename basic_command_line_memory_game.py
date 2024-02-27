import random

# Initialise the board
symbols = list(range(1, 9)) * 2  # Generate 8 pairs of symbols (basic game to use digits for simplicity)
random.shuffle(symbols)
board = [symbols[i:i + 4] for i in range(0, 16, 4)]  # Generate 4x4 grid from the shuffled symbols list
found_pairs = [[False] * 4 for _ in range(4)]  # Initialise 4x4 grid, all values set to False (to keep track of found pairs)

# Display current state of board for player
def print_board(show_all=False, show_card_choices=False, card_choices=[]):
    for i in range(4):
        for j in range(4):
            # If a match has been found (or show_all is True), display card value from associated board position
            if show_all or found_pairs[i][j] or (show_card_choices and (i, j)) in card_choices:
                print(board[i][j], end=' ')
            # Otherwise, print an underscore to indicate an unmatched/hidden symbol
            else:
                print('_', end=' ')
        print() # New line after each grid row

# Check whether board position values associated with player input are equal 
# e.g. r1, c1 = location of player's first card input, as requested in play_game()
def check_match(r1, c1, r2, c2):
    return board[r1][c1] == board[r2][c2]

# Entry point for game
# Manages game state and progress; integrates various game components for a continuous experience. 
def play_game(card_choices=False):
    print("Welcome to the Memory Game! Here's the initial board:")
    print_board()
    moves = 0
    
    # Core gameplay loop
    while not all(all(row) for row in found_pairs):  # Check for game completion 
        # Input validation and error handling
        try:  # Convert input to integers and validate positions
            r1, c1 = map(int, input("Enter the row and column of the first card to flip (e.g., '1 2'): ").split())
            r2, c2 = map(int, input("Enter the row and column of the second card to flip (e.g., '3 4'): ").split())
            card_choices = (r1, c1), (r2, c2)
            #print_board(show_card_choices=True, card_choices=card_choices)
            if r1 == r2 and c1 == c2:
                print("You selected the same card twice. Please choose two different cards.")
                continue
            if found_pairs[r1][c1] or found_pairs[r2][c2]:
                print("One or both selected cards have already been matched. Please choose different cards.")
                continue
        except (ValueError, IndexError):  # Handle invalid input or positions out of range
            print("Invalid input. Please enter the row and column as two integers separated by a space.")
            continue
        
        # Reveal card choices
        print("Flipping cards...")
        print_board(show_card_choices=True, card_choices=card_choices)

        # Check for a match
        if check_match(r1, c1, r2, c2):
            print("It's a match!")
            found_pairs[r1][c1] = True
            found_pairs[r2][c2] = True
        else:
            print("Not a match.")
        
        print_board()  # Progress update (display current board state)
        moves += 1  # Track number of moves
    
    print(f"Congratulations, you've matched all pairs in {moves} moves!")
    print("Final board:")
    print_board(show_all=True)

# Uncomment to play the game:
play_game()

'''
TODO: First improvement - flip/reveal chosen cards so the player sees them whether they're a match or not. 
Currently, the cards don't actually get 'flipped'/revealed for the player, unless both card
choices make a match. If the cards were revealled when selected, the player could use their growing
knowledge of the board as it has been revealed so far, to select the next cards.

Change this version so that the board is displayed with the chosen cards revealed before
the 'match status' is displayed. After check_match(), print_board can display its state 
(i.e all matched pairs). 
'''
