import random

# Initialise the board   TODO: update to reflect player's chosen board size
# symbols = list(range(1, 9)) * 2  # Generate 8 pairs of symbols (basic game to use digits for simplicity)
# random.shuffle(symbols)
# board = [symbols[i:i + 4] for i in range(0, 16, 4)]  # Generate 4x4 grid from the shuffled symbols list
# found_pairs = [[False] * 4 for _ in range(4)]  # Initialise 4x4 grid, all values set to False (to keep track of found pairs)
def initialise_board(length, width):
    total_cards = length * width
    symbols = list(range(1, (total_cards // 2) + 1)) * 2
    random.shuffle(symbols)
    board = [symbols[i:i + length] for i in range(0, total_cards, length)]
    found_pairs = [[False] * length for _ in range(width)]
    return board, found_pairs

# Take player's board preferences
def get_board_size():
    # Capture and validate user input
    while True:   # Loop allows re-prompting, if validation fails
        try:
            dimensions = input('''Enter a single integer for a square board or two integers, separated by a space, for a rectangular board. 
                                Total number of cards should not exceed 100. ''')
            dimensions = [int(dim) for dim in dimensions.split()]

            # Validate the number of dimensions provided
            # Square board
            if len(dimensions) == 1:
                n = dimensions[0]
                if n * n > 100:
                    print("The total number of cards should not exceed 100. Choose a number between 2 and 10.")
                    continue
                elif (n * n) % 2 != 0:
                    print("The total number of cards must be even. Choose a different number.")
                    continue
                return n, n   # Return dimensions for square board 
            
            # Rectangular board
            elif len(dimensions) == 2:
                length, width = dimensions
                if length * width > 100:
                    print("The total number of cards should not exceed 100. Choose smaller numbers.")
                    continue
                elif length * width % 2 != 0:
                    print("The total number of cards must be even. Choose different numbers.")
                    continue
                return length, width # Return dimensions for rectangular board
            
            else:
                print("Invalid input. Please enter one or two integers.")

        except ValueError:
            print("Invalid input. Try again.")

# Display current state of board for player   TODO: update to reflect player's chosen board size
def print_board(board, found_pairs, length, width, show_all=False, show_card_choices=False, card_choices=[]):
    for i in range(length):
        for j in range(width):
            # If a match has been found (or show_all is True), display card value from associated board position
            if show_all or found_pairs[i][j] or (show_card_choices and (i, j)) in card_choices:
                print(board[i][j], end=' ')
            # Otherwise, print an underscore to indicate an unmatched/hidden symbol
            else:
                print('_', end=' ')
        print() # New line after each grid row

# Check whether board position values associated with player input are equal 
# e.g. r1, c1 = location of player's first card input, as requested in play_game()
def check_match(r1, c1, r2, c2, board):
    return board[r1][c1] == board[r2][c2]

# Entry point for game
# Manages game state and progress; integrates various game components for a continuous experience 
def play_game(card_choices=False):
    print("Welcome to the Memory Game!")
    length, width = get_board_size()
    print(f"length is {length}, width is {width}")  #DEBUGGING
    board, found_pairs = initialise_board(length, width)
    print(f"board_initialised. Board: {board}\nFound pairs: {found_pairs}")  #DEBUGGING
    print("Printing board:")  #DEBUGGING
    print_board(board, found_pairs, length, width)
    moves = 0
    
    # Core gameplay loop
    while not all(all(row) for row in found_pairs):  # Check for game completion 
        # Input validation and error handling
        try:  # Convert input to integers and validate positions
            # First card selection
            r1, c1 = map(int, input("Enter the row and column of the first card to flip (e.g., '1 2'): ").split())
            card_choices = [(r1, c1)]
            print_board(board, found_pairs, length, width, show_card_choices=True, card_choices=card_choices)
            
            # Second card selection
            r2, c2 = map(int, input("Enter the row and column of the second card to flip (e.g., '3 4'): ").split())
            
            # Validation
            if r1 == r2 and c1 == c2:
                print("You selected the same card twice. Please choose two different cards.")
                continue
            if found_pairs[r1][c1] or found_pairs[r2][c2]:
                print("One or both selected cards have already been matched. Please choose different cards.")
                continue
            else:
                # Valid second card selection, add to card_choices & reveal
                card_choices.append((r2, c2))
                print_board(board, found_pairs, length, width, show_card_choices=True, card_choices=card_choices)
        
        except (ValueError, IndexError):  # Handle invalid input or positions out of range
            print("Invalid input. Please enter the row and column as two integers separated by a space.")
            continue

        # Check for a match
        if check_match(r1, c1, r2, c2, board):
            print("It's a match!")
            found_pairs[r1][c1] = True
            found_pairs[r2][c2] = True
        else:
            print("Not a match.")
        
        print_board(board, found_pairs, length, width)  # Progress update (display current board state)
        moves += 1  # Track number of moves
    
    print(f"Congratulations, you've matched all pairs in {moves} moves!")
    print("Final board:")
    print_board(board, found_pairs, length, width, show_all=True)

# Uncomment to play the game:
play_game()


#TODO: Third improvement - allow player to choose size of board (regular shape, <100 cards). 
