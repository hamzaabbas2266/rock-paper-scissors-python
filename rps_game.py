"""Rock Paper Scissors - a polished tkinter GUI game."""
import random
import tkinter as tk
from tkinter import messagebox

C_BG = "#0f172a"
C_CARD = "#1e293b"
C_CARD_2 = "#334155"
C_PRIMARY = "#6366f1"
C_ACCENT = "#ec4899"
C_WIN = "#10b981"
C_LOSE = "#ef4444"
C_DRAW = "#f59e0b"
C_TEXT = "#f1f5f9"
C_MUTED = "#94a3b8"

CHOICES = ["rock", "paper", "scissors"]
EMOJI = {"rock": "✊", "paper": "✋", "scissors": "✌"}
LABEL = {"rock": "Rock", "paper": "Paper", "scissors": "Scissors"}
BEATS = {"rock": "scissors", "paper": "rock", "scissors": "paper"}


def result_of(player, computer):
    if player == computer:
        return "draw"
    return "win" if BEATS[player] == computer else "lose"


class RockPaperScissors:
    def __init__(self, root):
        self.root = root
        self.root.title("Rock Paper Scissors")
        self.root.geometry("720x640")
        self.root.minsize(640, 580)
        self.root.configure(bg=C_BG)

        self.player_score = 0
        self.computer_score = 0
        self.draws = 0
        self.streak = 0
        self.best_streak = 0
        self.rounds = 0
        self.history = []

        self._build_ui()
        self._update_scoreboard()

    def _btn(self, parent, text, command, bg=C_PRIMARY, fg=C_TEXT, size=11):
        return tk.Button(parent, text=text, command=command, bg=bg, fg=fg,
                         activebackground=C_CARD_2, activeforeground=fg, relief="flat",
                         font=("Segoe UI", size, "bold"), cursor="hand2", bd=0,
                         padx=16, pady=10)

    def _build_ui(self):
        header = tk.Frame(self.root, bg=C_PRIMARY, height=64)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="✊  Rock  ✋  Paper  ✌  Scissors", bg=C_PRIMARY, fg=C_TEXT,
                 font=("Segoe UI", 18, "bold")).pack(side="left", padx=20, pady=12)
        self._btn(header, "Reset", self.reset, bg=C_CARD_2, size=10).pack(side="right", padx=16, pady=12)

        scoreboard = tk.Frame(self.root, bg=C_CARD)
        scoreboard.pack(fill="x")
        self.score_you = tk.Label(scoreboard, text="0", bg=C_CARD, fg=C_WIN,
                                  font=("Segoe UI", 36, "bold"))
        self.score_you.pack(side="left", padx=(60, 0), pady=10)
        tk.Label(scoreboard, text="YOU", bg=C_CARD, fg=C_MUTED,
                font=("Segoe UI", 11, "bold")).pack(side="left", padx=(8, 0), pady=(28, 10))

        mid = tk.Frame(scoreboard, bg=C_CARD)
        mid.pack(side="left", expand=True)
        self.result_label = tk.Label(mid, text="Make your move!", bg=C_CARD, fg=C_TEXT,
                                     font=("Segoe UI", 16, "bold"))
        self.result_label.pack(pady=6)
        self.streak_label = tk.Label(mid, text="Streak: 0   ·   Best: 0   ·   Draws: 0",
                                     bg=C_CARD, fg=C_MUTED, font=("Segoe UI", 10))
        self.streak_label.pack(pady=(0, 6))

        tk.Label(scoreboard, text="CPU", bg=C_CARD, fg=C_MUTED,
                font=("Segoe UI", 11, "bold")).pack(side="right", padx=(0, 8), pady=(28, 10))
        self.score_cpu = tk.Label(scoreboard, text="0", bg=C_CARD, fg=C_LOSE,
                                  font=("Segoe UI", 36, "bold"))
        self.score_cpu.pack(side="right", padx=(0, 60), pady=10)

        arena = tk.Frame(self.root, bg=C_BG)
        arena.pack(fill="both", expand=True, padx=20, pady=16)

        hands = tk.Frame(arena, bg=C_BG)
        hands.pack(pady=(10, 20))
        self.hand_you = tk.Label(hands, text="?", bg=C_CARD, fg=C_TEXT,
                                 font=("Segoe UI", 72), width=3, relief="flat")
        self.hand_you.pack(side="left", padx=30)
        tk.Label(hands, text="VS", bg=C_BG, fg=C_MUTED,
                 font=("Segoe UI", 18, "bold")).pack(side="left", padx=20)
        self.hand_cpu = tk.Label(hands, text="?", bg=C_CARD, fg=C_TEXT,
                                 font=("Segoe UI", 72), width=3, relief="flat")
        self.hand_cpu.pack(side="left", padx=30)

        choices = tk.Frame(arena, bg=C_BG)
        choices.pack(pady=10)
        for choice, color in [("rock", C_LOSE), ("paper", C_WIN), ("scissors", C_ACCENT)]:
            card = tk.Frame(choices, bg=C_CARD, padx=18, pady=14, cursor="hand2")
            card.pack(side="left", padx=14)
            tk.Label(card, text=EMOJI[choice], bg=C_CARD, fg=color,
                     font=("Segoe UI", 44)).pack()
            tk.Label(card, text=LABEL[choice], bg=C_CARD, fg=C_TEXT,
                     font=("Segoe UI", 12, "bold")).pack(pady=(6, 0))
            card.bind("<Button-1>", lambda e, c=choice: self.play(c))
            for child in card.winfo_children():
                child.bind("<Button-1>", lambda e, c=choice: self.play(c))

        hist_frame = tk.Frame(self.root, bg=C_CARD)
        hist_frame.pack(fill="x", padx=20, pady=(0, 12))
        tk.Label(hist_frame, text="Round History", bg=C_CARD, fg=C_MUTED,
                 font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=12, pady=(8, 0))
        self.history_box = tk.Listbox(hist_frame, bg=C_CARD, fg=C_TEXT, selectbackground=C_CARD_2,
                                      selectforeground=C_TEXT, relief="flat", highlightthickness=0,
                                      font=("Segoe UI", 10), height=6, activestyle="none")
        self.history_box.pack(fill="x", padx=12, pady=(4, 12))

    def play(self, player):
        computer = random.choice(CHOICES)
        outcome = result_of(player, computer)

        self.hand_you.config(text=EMOJI[player])
        self.hand_cpu.config(text=EMOJI[computer])

        self.rounds += 1
        if outcome == "win":
            self.player_score += 1
            self.streak += 1
            self.best_streak = max(self.best_streak, self.streak)
            self.result_label.config(text=f"You win! {LABEL[player]} beats {LABEL[computer]}.", fg=C_WIN)
        elif outcome == "lose":
            self.computer_score += 1
            self.streak = 0
            self.result_label.config(text=f"You lose! {LABEL[computer]} beats {LABEL[player]}.", fg=C_LOSE)
        else:
            self.draws += 1
            self.result_label.config(text=f"Draw! Both chose {LABEL[player]}.", fg=C_DRAW)

        self.history.insert(0, f"Round {self.rounds}: You {LABEL[player]}  vs  CPU {LABEL[computer]}  ->  {outcome.upper()}")
        self.history = self.history[:20]
        self.history_box.delete(0, "end")
        for item in self.history:
            self.history_box.insert("end", item)

        self._update_scoreboard()

    def _update_scoreboard(self):
        self.score_you.config(text=str(self.player_score))
        self.score_cpu.config(text=str(self.computer_score))
        self.streak_label.config(text=f"Streak: {self.streak}   ·   Best: {self.best_streak}   ·   Draws: {self.draws}")

    def reset(self):
        if self.rounds == 0:
            return
        if messagebox.askyesno("Reset", "Reset all scores and history?"):
            self.player_score = 0
            self.computer_score = 0
            self.draws = 0
            self.streak = 0
            self.best_streak = 0
            self.rounds = 0
            self.history = []
            self.history_box.delete(0, "end")
            self.hand_you.config(text="?")
            self.hand_cpu.config(text="?")
            self.result_label.config(text="Make your move!", fg=C_TEXT)
            self._update_scoreboard()


def main():
    root = tk.Tk()
    RockPaperScissors(root)
    root.mainloop()


if __name__ == "__main__":
    main()