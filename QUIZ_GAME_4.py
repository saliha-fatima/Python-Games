import tkinter as tk
from tkinter import messagebox
import random

class QuizGame:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Quiz Game")
        self.window.geometry("800x600")

        self.current_question = 0
        self.score = 0
        self.timer = 10  # 10 seconds per question
        self.level = 1  # Start at level 1
        self.levels = {
            1: [
                {"question": "What is the capital of France?", "answer": "Paris", "hint": "It's known as the city of lights."},
                {"question": "What is the largest planet in our solar system?", "answer": "Jupiter", "hint": "It's a gas giant."},
                {"question": "Who painted the Mona Lisa?", "answer": "Leonardo da Vinci", "hint": "He was also an inventor."},
            ],
            2: [
                {"question": "What does CPU stand for?", "answer": "Central Processing Unit", "hint": "It's the brain of the computer."},
                {"question": "Which company developed the Windows OS?", "answer": "Microsoft", "hint": "It's a tech giant founded by Bill Gates."},
                {"question": "What is the name of the first computer virus?", "answer": "Creeper", "hint": "It was detected on the ARPANET."},
            ],
            3: [
                {"question": "What does HTML stand for?", "answer": "HyperText Markup Language", "hint": "It's the standard language for web pages."},
                {"question": "Which protocol is used to transfer files over the Internet?", "answer": "FTP", "hint": "It stands for File Transfer Protocol."},
                {"question": "What is the full form of RAM?", "answer": "Random Access Memory", "hint": "It's used for temporary data storage in computers."},
            ]
        }

        self.questions = self.levels[self.level]
        random.shuffle(self.questions)  # Shuffle questions to randomize order

        self.score_label = tk.Label(self.window, text=f"Score: {self.score}", font=("Arial", 18))
        self.score_label.pack(pady=10)

        self.level_label = tk.Label(self.window, text=f"Level: {self.level}", font=("Arial", 18))
        self.level_label.pack(pady=10)

        self.timer_label = tk.Label(self.window, text=f"Time Left: {self.timer}s", font=("Arial", 18), fg="red")
        self.timer_label.pack(pady=10)

        self.question_label = tk.Label(self.window, text="", wraplength=600, font=("Arial", 24))
        self.question_label.pack(pady=20)

        self.answer_entry = tk.Entry(self.window, font=("Arial", 24))
        self.answer_entry.pack(pady=20)

        self.hint_button = tk.Button(self.window, text="Show Hint", command=self.show_hint, font=("Arial", 18))
        self.hint_button.pack(pady=10)

        self.submit_button = tk.Button(self.window, text="Submit", command=self.submit_answer, font=("Arial", 24))
        self.submit_button.pack(pady=20)

        self.colors = ["blue", "green", "yellow", "purple", "SystemButtonFace"]
        self.color_index = 0

        self.display_question()
        self.update_timer()

    def display_question(self):
        question_text = self.questions[self.current_question]["question"]
        self.question_label.config(text=question_text)
        self.answer_entry.delete(0, tk.END)  # Clear the entry field

    def submit_answer(self):
        user_answer = self.answer_entry.get()
        correct_answer = self.questions[self.current_question]["answer"]

        if user_answer.lower() == correct_answer.lower():
            self.score += 1
            messagebox.showinfo("Correct!", "Your answer is correct!")
        else:
            messagebox.showinfo("Incorrect", f"Sorry, the correct answer is {correct_answer}")

        self.score_label.config(text=f"Score: {self.score}")

        # Change background color after each answer
        self.change_color()

        self.current_question += 1
        if self.current_question >= len(self.questions):
            self.next_level_or_end_game()
        else:
            self.reset_timer()
            self.display_question()

    def next_level_or_end_game(self):
        if self.level < 3:  # Move to the next level if there are more levels
            self.level += 1
            self.questions = self.levels[self.level]
            random.shuffle(self.questions)  # Shuffle questions for the new level
            self.current_question = 0  # Reset to first question of the new level
            self.level_label.config(text=f"Level: {self.level}")
            messagebox.showinfo("Level Up!", f"Welcome to Level {self.level}!")
            self.display_question()
        else:
            self.display_result()

    def display_result(self):
        messagebox.showinfo("Result", f"Your final score is {self.score} out of {sum(len(l) for l in self.levels.values())}")
        self.window.destroy()

    def change_color(self):
        # Cycle through the list of colors after each answer
        self.color_index = (self.color_index + 1) % len(self.colors)
        new_color = self.colors[self.color_index]

        self.window.config(bg=new_color)
        self.question_label.config(bg=new_color)
        self.answer_entry.config(bg=new_color)
        self.submit_button.config(bg=new_color)
        self.hint_button.config(bg=new_color)
        self.score_label.config(bg=new_color)
        self.level_label.config(bg=new_color)
        self.timer_label.config(bg=new_color)

    def show_hint(self):
        hint = self.questions[self.current_question].get("hint", "No hint available.")
        messagebox.showinfo("Hint", hint)

    def reset_timer(self):
        self.timer = 10  # Reset the timer to 10 seconds
        self.update_timer()

    def update_timer(self):
        if self.timer > 0:
            self.timer_label.config(text=f"Time Left: {self.timer}s")
            self.timer -= 1
            self.window.after(1000, self.update_timer)
        else:
            messagebox.showinfo("Time's up!", f"You ran out of time! The correct answer was {self.questions[self.current_question]['answer']}")
            self.submit_answer()  # Move to the next question

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = QuizGame()
    game.run()
