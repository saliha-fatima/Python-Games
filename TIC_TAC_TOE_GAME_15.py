import tkinter as tk
from tkinter import messagebox
import random
import time

# Initialize global variables for tracking scores
player1_score = 0
player2_score = 0
total_games = 0
draw_games = 0  # Added to track the number of draws

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.player1 = ""
        self.player2 = ""
        self.current_player = ""
        self.board = [""] * 9
        self.colors = ["#FF5733", "#33FF57", "#3357FF", "#FF33F6", "#FFDB33", "#33FFF3", "#E133FF", "#F3FF33", "#33FFBD"]
        self.timer_label = tk.Label(root, text="Timer: 0s", font=("Arial", 12), bg="#FFFFFF")
        self.timer_label.pack()

        self.start_time = None
        self.turn_time = 10  # seconds for each turn (customizable in settings)
        self.create_registration()

    def create_registration(self):
        # Create Registration Frame
        self.registration_frame = tk.Frame(self.root)
        self.registration_frame.pack()

        tk.Label(self.registration_frame, text="Player 1 Name: ").grid(row=0, column=0)
        tk.Label(self.registration_frame, text="Player 2 Name: ").grid(row=1, column=0)

        self.player1_name_entry = tk.Entry(self.registration_frame)
        self.player2_name_entry = tk.Entry(self.registration_frame)

        self.player1_name_entry.grid(row=0, column=1)
        self.player2_name_entry.grid(row=1, column=1)

        settings_button = tk.Button(self.registration_frame, text="Settings", command=self.open_settings)
        settings_button.grid(row=2, column=0)

        start_button = tk.Button(self.registration_frame, text="Start Game", command=self.start_game)
        start_button.grid(row=2, column=1)

    def open_settings(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        tk.Label(settings_window, text="Turn Timer (seconds):").grid(row=0, column=0)

        self.timer_entry = tk.Entry(settings_window)
        self.timer_entry.grid(row=0, column=1)
        self.timer_entry.insert(0, str(self.turn_time))

        save_button = tk.Button(settings_window, text="Save", command=lambda: self.save_settings(settings_window))
        save_button.grid(row=1, columnspan=2)

    def save_settings(self, window):
        self.turn_time = int(self.timer_entry.get())
        window.destroy()

    def start_game(self):
        # Get player names
        self.player1 = self.player1_name_entry.get()
        self.player2 = self.player2_name_entry.get()

        if not self.player1 or not self.player2:
            messagebox.showwarning("Warning", "Please enter both player names!")
            return

        self.current_player = self.player1
        self.registration_frame.destroy()  # Remove registration screen

        # Setup game UI
        self.create_game_ui()

    def create_game_ui(self):
        # Create a frame for the game board
        self.game_frame = tk.Frame(self.root)
        self.game_frame.pack()

        self.buttons = []
        for i in range(9):
            button = tk.Button(self.game_frame, text="", width=10, height=3, bg=random.choice(self.colors),
                               command=lambda i=i: self.handle_turn(i))
            button.grid(row=i // 3, column=i % 3, sticky="nsew")
            self.buttons.append(button)

        self.status_label = tk.Label(self.root, text=f"Turn: {self.current_player}", font=("Arial", 16))
        self.status_label.pack()

        # Updated score label to include draw count
        self.score_label = tk.Label(self.root, text=f"{self.player1}: {player1_score} Wins | {self.player2}: {player2_score} Wins | Draws: {draw_games} | Total Games: {total_games}", font=("Arial", 14))
        self.score_label.pack()

        self.reset_button = tk.Button(self.root, text="Reset Game", command=self.reset_game)
        self.reset_button.pack()

        # Background color
        self.root.configure(bg=random.choice(self.colors))

        # Start the timer for the turn
        self.start_timer()

        # Make the board responsive
        for i in range(3):
            self.game_frame.grid_columnconfigure(i, weight=1)
            self.game_frame.grid_rowconfigure(i, weight=1)

    def start_timer(self):
        self.start_time = time.time()
        self.update_timer()

    def update_timer(self):
        elapsed_time = time.time() - self.start_time
        remaining_time = int(self.turn_time - elapsed_time)

        if remaining_time > 0:
            self.timer_label.config(text=f"Timer: {remaining_time}s", fg="black" if remaining_time > 3 else "red")
            self.root.after(1000, self.update_timer)
        else:
            messagebox.showinfo("Time's Up!", f"{self.current_player} ran out of time!")
            self.switch_turns()

    def handle_turn(self, index):
        if self.board[index] == "":
            self.board[index] = self.current_player

            if self.current_player == self.player1:
                self.buttons[index].config(text="X", state="disabled", bg="red")
            else:
                self.buttons[index].config(text="O", state="disabled", bg="blue")

            if self.check_winner():
                self.end_game(f"{self.current_player} wins!")
            elif "" not in self.board:
                self.end_game("It's a draw!")  # Handle draw case
            else:
                self.switch_turns()

    def switch_turns(self):
        self.current_player = self.player2 if self.current_player == self.player1 else self.player1
        self.status_label.config(text=f"Turn: {self.current_player}")
        self.root.configure(bg=random.choice(self.colors))

        self.start_timer()  # Restart the timer for the new player

    def check_winner(self):
        winning_combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                                (0, 3, 6), (1, 4, 7), (2, 5, 8),
                                (0, 4, 8), (2, 4, 6)]
        for combo in winning_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != "":
                self.highlight_winning_combination(combo)
                return True
        return False

    def highlight_winning_combination(self, combo):
        for index in combo:
            self.buttons[index].config(bg="yellow")

    def end_game(self, result):
        global player1_score, player2_score, total_games, draw_games  # Added draw_games

        messagebox.showinfo("Game Over", result)
        total_games += 1

        if self.current_player == self.player1 and "wins" in result:
            player1_score += 1
        elif self.current_player == self.player2 and "wins" in result:
            player2_score += 1
        elif "draw" in result:  # Handle draw result
            draw_games += 1

        # Update score label to reflect wins, losses, and draws
        self.score_label.config(text=f"{self.player1}: {player1_score} Wins | {self.player2}: {player2_score} Wins | Draws: {draw_games} | Total Games: {total_games}")

        self.reset_board()

    def reset_board(self):
        self.board = [""] * 9
        for button in self.buttons:
            button.config(text="", state="normal", bg=random.choice(self.colors))
        self.current_player = self.player1
        self.start_timer()

    def reset_game(self):
        global player1_score, player2_score, total_games, draw_games  # Reset draw_games as well
        player1_score, player2_score, total_games, draw_games = 0, 0, 0, 0
        self.reset_board()
        self.status_label.config(text=f"Turn: {self.current_player}")
        self.score_label.config(text=f"{self.player1}: {player1_score} Wins | {self.player2}: {player2_score} Wins | Draws: {draw_games} | Total Games: {total_games}")
        self.timer_label.config(text="Timer: 0s")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x450")  # Set a fixed window size
    game = TicTacToe(root)
    root.mainloop()
