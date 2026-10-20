
import random
import tkinter as tk
from tkinter import messagebox


WORDS = ["python", "hangman", "computer", "developer", "program"]


class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("CodeAlpha | Hangman Game")
        self.root.geometry("800x650")
        self.root.resizable(False, False)
        self.root.configure(bg="#101827")

        self.bg = "#101827"
        self.panel = "#1c293b"
        self.text = "#f1f5f9"
        self.muted = "#9caec4"
        self.accent = "#38bdf8"
        self.green = "#34d399"
        self.red = "#fb7185"

        self.build_ui()
        self.new_game()

        self.root.bind("<KeyPress>", self.keyboard_guess)

    def build_ui(self):
        tk.Label(
            self.root,
            text="CODEALPHA",
            font=("Arial", 12, "bold"),
            fg=self.accent,
            bg=self.bg
        ).pack(pady=(18, 3))

        tk.Label(
            self.root,
            text="HANGMAN",
            font=("Arial", 30, "bold"),
            fg=self.text,
            bg=self.bg
        ).pack()

        tk.Label(
            self.root,
            text="Guess the hidden word before your attempts run out!",
            font=("Arial", 11),
            fg=self.muted,
            bg=self.bg
        ).pack(pady=(5, 15))

        self.word_label = tk.Label(
            self.root,
            text="",
            font=("Consolas", 28, "bold"),
            fg=self.accent,
            bg=self.panel,
            pady=15
        )
        self.word_label.pack(fill="x", padx=35)

        self.status_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 12, "bold"),
            fg=self.text,
            bg=self.bg
        )
        self.status_label.pack(pady=10)

        self.canvas = tk.Canvas(
            self.root,
            width=220,
            height=180,
            bg=self.panel,
            highlightthickness=0
        )
        self.canvas.pack(pady=5)

        tk.Label(
            self.root,
            text="CHOOSE A LETTER",
            font=("Arial", 11, "bold"),
            fg=self.muted,
            bg=self.bg
        ).pack(pady=(12, 8))

        self.letters_frame = tk.Frame(self.root, bg=self.bg)
        self.letters_frame.pack()

        self.letter_buttons = {}

        for index, letter in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
            button = tk.Button(
                self.letters_frame,
                text=letter,
                width=3,
                font=("Arial", 10, "bold"),
                bg=self.panel,
                fg=self.text,
                activebackground=self.accent,
                activeforeground=self.bg,
                relief="flat",
                cursor="hand2",
                command=lambda char=letter.lower(): self.guess(char)
            )
            button.grid(
                row=index // 13,
                column=index % 13,
                padx=3,
                pady=4
            )
            self.letter_buttons[letter.lower()] = button

        self.message_label = tk.Label(
            self.root,
            text="You have 6 incorrect attempts.",
            font=("Arial", 10),
            fg=self.muted,
            bg=self.bg
        )
        self.message_label.pack(pady=10)

        tk.Button(
            self.root,
            text="↻  PLAY AGAIN",
            font=("Arial", 11, "bold"),
            bg=self.accent,
            fg=self.bg,
            activebackground="#7dd3fc",
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=8,
            command=self.new_game
        ).pack(pady=(0, 15))

    def new_game(self):
        self.word = random.choice(WORDS)
        self.guessed = set()
        self.incorrect = set()
        self.game_over = False

        for button in self.letter_buttons.values():
            button.config(
                state="normal",
                bg=self.panel,
                fg=self.text
            )

        self.message_label.config(
            text="You have 6 incorrect attempts.",
            fg=self.muted
        )
        self.status_label.config(
            text="Good luck! Find the hidden word.",
            fg=self.text
        )

        self.update_display()
        self.draw_hangman()

    def guess(self, letter):
        if self.game_over:
            return

        if letter in self.guessed or letter in self.incorrect:
            return

        button = self.letter_buttons[letter]
        button.config(state="disabled")

        if letter in self.word:
            self.guessed.add(letter)
            button.config(bg="#14532d", fg="#bbf7d0")
            self.status_label.config(
                text="Correct guess!",
                fg=self.green
            )
        else:
            self.incorrect.add(letter)
            button.config(bg="#7f1d1d", fg="#fecaca")
            self.status_label.config(
                text="Wrong guess! Try another letter.",
                fg=self.red
            )

        self.update_display()
        self.draw_hangman()

        remaining = 6 - len(self.incorrect)
        self.message_label.config(
            text=f"Incorrect attempts remaining: {remaining}"
        )

        if all(char in self.guessed for char in self.word):
            self.game_over = True
            self.status_label.config(
                text="🎉 YOU WON!",
                fg=self.green
            )
            self.disable_keyboard()
            messagebox.showinfo(
                "Congratulations!",
                f"You guessed the word: {self.word.upper()}"
            )

        elif remaining == 0:
            self.game_over = True
            self.status_label.config(
                text="GAME OVER!",
                fg=self.red
            )
            self.word_label.config(
                text="  ".join(self.word.upper())
            )
            self.disable_keyboard()
            messagebox.showinfo(
                "Game Over",
                f"The hidden word was: {self.word.upper()}"
            )

    def update_display(self):
        shown = [
            char.upper() if char in self.guessed else "_"
            for char in self.word
        ]
        self.word_label.config(text="  ".join(shown))

    def draw_hangman(self):
        self.canvas.delete("all")

        color = self.red
        width = 4
        wrong = len(self.incorrect)

        # Gallows
        self.canvas.create_line(
            25, 160, 105, 160, fill=self.muted, width=width
        )
        self.canvas.create_line(
            65, 160, 65, 20, fill=self.muted, width=width
        )
        self.canvas.create_line(
            65, 20, 145, 20, fill=self.muted, width=width
        )
        self.canvas.create_line(
            145, 20, 145, 40, fill=self.muted, width=width
        )

        # Body parts appear after incorrect guesses
        if wrong >= 1:
            self.canvas.create_oval(
                127, 40, 163, 76, outline=color, width=width
            )
        if wrong >= 2:
            self.canvas.create_line(
                145, 76, 145, 115, fill=color, width=width
            )
        if wrong >= 3:
            self.canvas.create_line(
                145, 85, 120, 103, fill=color, width=width
            )
        if wrong >= 4:
            self.canvas.create_line(
                145, 85, 170, 103, fill=color, width=width
            )
        if wrong >= 5:
            self.canvas.create_line(
                145, 115, 122, 143, fill=color, width=width
            )
        if wrong >= 6:
            self.canvas.create_line(
                145, 115, 168, 143, fill=color, width=width
            )

    def keyboard_guess(self, event):
        letter = event.char.lower()
        if letter in self.letter_buttons:
            self.guess(letter)

    def disable_keyboard(self):
        for button in self.letter_buttons.values():
            button.config(state="disabled")


if __name__ == "__main__":
    window = tk.Tk()
    game = HangmanGame(window)
    window.mainloop()
