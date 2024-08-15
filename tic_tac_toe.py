import random
import tkinter as tk
from tkinter import messagebox
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class Player:
    """
    Represents a player in the Tic Tac Toe game.
    
    Attributes:
        symbol (str): The symbol ('X' or 'O') representing the player.
    """
    def __init__(self, symbol):
        """
        Initializes a Player with the given symbol.
        
        Args:
            symbol (str): The symbol representing the player.
        """
        self.symbol = symbol
        logging.debug(f'Player initialized with symbol: {self.symbol}')

    def make_move(self, board, row, col):
        """
        Makes a move on the board for the player.
        
        Args:
            board (Board): The game board.
            row (int): The row index.
            col (int): The column index.
        
        Returns:
            bool: True if the move is successful, False otherwise.
        """
        logging.debug(f'Player making move at ({row}, {col})')
        if board.make_move(row, col, self.symbol):
            return True
        else:
            messagebox.showerror("Invalid Move", "That position is already taken.")
            return False


class Computer:
    """
    Represents the computer player in the Tic Tac Toe game.
    
    Attributes:
        symbol (str): The symbol ('X' or 'O') representing the computer.
    """
    def __init__(self, symbol):
        """
        Initializes a Computer with the given symbol.
        
        Args:
            symbol (str): The symbol representing the computer.
        """
        self.symbol = symbol
        logging.debug(f'Computer initialized with symbol: {self.symbol}')

    def make_move(self, board):
        """
        Makes a move on the board for the computer.
        
        Args:
            board (Board): The game board.
        
        Returns:
            tuple: The row and column indices of the move made by the computer.
        """
        best_move = self.find_best_move(board)
        logging.debug(f'Computer making move at {best_move}')
        
        # Check if the chosen move by find_best_move is already occupied
        while not board.is_valid_move(best_move[0], best_move[1]):
            logging.debug(f'Move {best_move} is invalid, finding new move')
            best_move = self.find_best_move(board)
        
        board.make_move(best_move[0], best_move[1], self.symbol)
        return best_move  # Return the move made by the computer

    def find_best_move(self, board):
        """
        Finds the best move for the computer to make.
        
        Args:
            board (Board): The game board.
        
        Returns:
            tuple: The row and column indices of the best move.
        """
        logging.debug('Computer finding best move')
        opponent_symbol = 'X' if self.symbol == 'O' else 'O'

        # If the player starts and does not play in the center, the computer plays in the center
        if board.current_turn == 'computer' and board.board[1][1] == ' ':
            player_first_move = [(i, j) for i in range(3) for j in range(3) if board.board[i][j] == opponent_symbol]
            if len(player_first_move) == 1 and player_first_move[0] != (1, 1):
                logging.debug('Computer playing in the center')
                return (1, 1)

        # Look for a direct win
        for i in range(3):
            for j in range(3):
                if board.is_valid_move(i, j):
                    board.make_move(i, j, self.symbol)
                    if board.is_winner(self.symbol):
                        board.board[i][j] = ' '  # Undo the simulated move
                        logging.debug(f'Computer found winning move at ({i}, {j})')
                        return (i, j)
                    board.board[i][j] = ' '  # Undo the simulated move

        # Defense: Block if the opponent can win
        for i in range(3):
            for j in range(3):
                if board.is_valid_move(i, j):
                    board.make_move(i, j, opponent_symbol)
                    if board.is_winner(opponent_symbol):
                        board.board[i][j] = ' '  # Undo the simulated move
                        logging.debug(f'Computer blocking opponent move at ({i}, {j})')
                        return (i, j)
                    board.board[i][j] = ' '  # Undo the simulated move
                    
        # Prioritize corners
        corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
        random.shuffle(corners)  # Shuffle the order of corners

        for move in corners:
            if board.is_valid_move(move[0], move[1]):
                logging.debug(f'Computer prioritizing corner move at {move}')
                return move

        # If no direct threat is detected, play in the center if possible
        if board.is_valid_move(1, 1):
            logging.debug('Computer playing in the center')
            return (1, 1)

        # Play the first empty spot found
        for i in range(3):
            for j in range(3):
                if board.is_valid_move(i, j):
                    logging.debug(f'Computer playing at first empty spot ({i}, {j})')
                    return (i, j)

        # As a precaution, return an invalid move
        logging.debug('Computer did not find a valid move')
        return (-1, -1)


class Board:
    """
    Represents the game board for Tic Tac Toe.
    
    Attributes:
        board (list): A 3x3 list representing the game board.
        current_turn (str): The current turn ('player' or 'computer').
        player_score (int): The score of the player.
        computer_score (int): The score of the computer.
        tie_count (int): The count of tie games.
    """
    def __init__(self):
        """
        Initializes the game board and scores.
        """
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_turn = 'player'  # Initial turn set to player
        self.player_score = 0
        self.computer_score = 0
        self.tie_count = 0
        logging.debug('Board initialized')

    def display(self):
        """
        Displays the current state of the game board and scores.
        """
        for row in self.board:
            print("|".join(row))
            print("-" * 5)
        print(f"Player Score: {self.player_score}  Computer Score: {self.computer_score}  Ties: {self.tie_count}")
        print()

    def is_winner(self, symbol):
        """
        Checks if the given symbol has won the game.
        
        Args:
            symbol (str): The symbol to check for a win.
        
        Returns:
            bool: True if the symbol has won, False otherwise.
        """
        # Check rows for a win
        for row in self.board:
            if row[0] == row[1] == row[2] == symbol:
                logging.debug(f'{symbol} wins on a row')
                return True

        # Check columns for a win
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] == symbol:
                logging.debug(f'{symbol} wins on a column')
                return True

        # Check diagonals for a win
        if self.board[0][0] == self.board[1][1] == self.board[2][2] == symbol:
            logging.debug(f'{symbol} wins on a diagonal')
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] == symbol:
            logging.debug(f'{symbol} wins on a diagonal')
            return True

        return False

    def get_winning_positions(self, symbol):
        """
        Gets the positions of the winning combination.
        
        Args:
            symbol (str): The symbol to check for a win.
        
        Returns:
            list: A list of tuples representing the winning positions.
        """
        winning_positions = []

        # Check rows for a win
        for i, row in enumerate(self.board):
            if row[0] == row[1] == row[2] == symbol:
                winning_positions = [(i, 0), (i, 1), (i, 2)]
                return winning_positions

        # Check columns for a win
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] == symbol:
                winning_positions = [(0, col), (1, col), (2, col)]
                return winning_positions

        # Check diagonals for a win
        if self.board[0][0] == self.board[1][1] == self.board[2][2] == symbol:
            winning_positions = [(0, 0), (1, 1), (2, 2)]
            return winning_positions
        if self.board[0][2] == self.board[1][1] == self.board[2][0] == symbol:
            winning_positions = [(0, 2), (1, 1), (2, 0)]
            return winning_positions

        return winning_positions

    def is_full(self):
        """
        Checks if the game board is full.
        
        Returns:
            bool: True if the board is full, False otherwise.
        """
        for row in self.board:
            if ' ' in row:
                return False
        logging.debug('Board is full')
        return True

    def make_move(self, row, col, symbol):
        """
        Makes a move on the board at the specified position.
        
        Args:
            row (int): The row index.
            col (int): The column index.
            symbol (str): The symbol to place on the board.
        
        Returns:
            bool: True if the move is successful, False otherwise.
        """
        if self.board[row][col] == ' ':
            self.board[row][col] = symbol
            logging.debug(f'Move made at ({row}, {col}) by {symbol}')
            return True
        logging.debug(f'Invalid move attempted at ({row}, {col}) by {symbol}')
        return False

    def is_valid_move(self, row, col):
        """
        Checks if the move at the specified position is valid.
        
        Args:
            row (int): The row index.
            col (int): The column index.
        
        Returns:
            bool: True if the move is valid, False otherwise.
        """
        # Check if the coordinates are within the board limits
        if 0 <= row < 3 and 0 <= col < 3:
            # Check if the spot is empty
            return self.board[row][col] == ' '
        return False

    def switch_turn(self):
        """
        Switches the turn between player and computer.
        """
        if self.current_turn == 'player':
            self.current_turn = 'computer'
        else:
            self.current_turn = 'player'
        logging.debug(f'Turn switched to {self.current_turn}')

    def reset_board(self):
        """
        Resets the game board to its initial empty state.
        """
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        logging.debug('Board reset')


class TicTacToeGUI:
    def __init__(self, root):
        """
        Initializes the Tic Tac Toe GUI.
        
        Args:
            root (tk.Tk): The root window of the Tkinter application.
        """
        self.root = root
        self.root.title("Tic Tac Toe")
        self.board = Board()
        self.player = Player('X')
        self.computer = Computer('O')
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.create_board()
        self.update_score_display()
        logging.debug('TicTacToeGUI initialized')

    def create_board(self):
        """
        Creates the game board with buttons for each cell.
        """
        for i in range(3):
            for j in range(3):
                button = tk.Button(self.root, fg="blue", font=('normal', 40), width=5, height=2,
                                   command=lambda i=i, j=j: self.player_move(i, j))
                button.grid(row=i, column=j)
                self.buttons[i][j] = button
        logging.debug('Board created')

    def player_move(self, row, col):
        """
        Handles the player's move.
        
        Args:
            row (int): The row index of the move.
            col (int): The column index of the move.
        """
        logging.debug(f'Player move at ({row}, {col})')
        if self.board.current_turn == 'player':
            if self.player.make_move(self.board, row, col):
                self.update_button(row, col, self.player.symbol, 'blue')
                self.root.update_idletasks()  # Force GUI update
                if self.check_winner_or_tie(self.player.symbol, "Player wins!"):
                    return
                self.board.switch_turn()
                self.computer_move()

    def computer_move(self):
        """
        Handles the computer's move.
        """
        logging.debug('Computer move')
        if self.board.current_turn == 'computer':
            move = self.computer.make_move(self.board)
            self.update_button(move[0], move[1], self.computer.symbol, 'red')
            self.root.update_idletasks()  # Force GUI update
            if self.check_winner_or_tie(self.computer.symbol, "Computer wins!"):
                return
            self.board.switch_turn()

    def update_button(self, row, col, symbol, color='black', font=('normal', 40)):
        """
        Updates the button text and state after a move.
        
        Args:
            row (int): The row index of the button.
            col (int): The column index of the button.
            symbol (str): The symbol to display on the button.
            color (str): The color of the symbol.
            font (tuple): The font of the symbol.
        """
        self.buttons[row][col].config(text=symbol, fg=color, font=font)
        logging.debug(f'Button at ({row}, {col}) updated with symbol {symbol}, color {color}, and font {font}')

    def check_winner_or_tie(self, symbol, win_message):
        """
        Checks if there is a winner or a tie.
        
        Args:
            symbol (str): The symbol to check for a win.
            win_message (str): The message to display if the symbol wins.
        
        Returns:
            bool: True if there is a winner or a tie, False otherwise.
        """
        if self.board.is_winner(symbol):
            winning_positions = self.board.get_winning_positions(symbol)
            for pos in winning_positions:
                self.update_button(pos[0], pos[1], symbol, 'green', ('normal', 40))
            self.root.update_idletasks()  # Force GUI update
            messagebox.showinfo("Game Over", win_message)
            if symbol == self.player.symbol:
                self.board.player_score += 1
            else:
                self.board.computer_score += 1
            self.update_score_display()
            self.reset_game()
            logging.debug(f'{symbol} wins the game')
            return True
        elif self.board.is_full():
            self.root.update_idletasks()  # Force GUI update
            messagebox.showinfo("Game Over", "It's a tie!")
            self.board.tie_count += 1
            self.update_score_display()
            self.reset_game()
            logging.debug('Game is a tie')
            return True
        return False


    def reset_game(self):
        """
        Resets the game for a new round.
        """
        self.board.reset_board()
        self.reset_buttons()
        self.switch_starting_player()
        logging.debug('Game reset')

    def reset_buttons(self):
        """
        Resets the buttons on the game board.
        """
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text=' ', state=tk.NORMAL, fg='black')
        self.root.update_idletasks()  # Force GUI update
        logging.debug('Buttons reset')

    def update_score_display(self):
        """
        Updates the score display in the window title.
        """
        self.root.title(f"Tic Tac Toe - Player Score: {self.board.player_score}  Computer Score: {self.board.computer_score}  Ties: {self.board.tie_count}")
        self.root.update_idletasks()  # Force GUI update
        logging.debug('Score display updated')

    def switch_starting_player(self):
        """
        Switches the starting player for the next game.
        """
        if self.board.current_turn == 'player':
            self.board.current_turn = 'computer'
            self.computer_move()
        else:
            self.board.current_turn = 'player'
        logging.debug(f'Starting player switched to {self.board.current_turn}')

# Call the main function to start the game
if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToeGUI(root)
    root.mainloop()
    logging.debug('Game started')



