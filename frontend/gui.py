import tkinter as tk
from tkinter import messagebox
import random
from typing import List

from backend.flashcard import Flashcard
from backend.csvHandler import saveFlashcards  # optional, used if you want to save

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simple Flashcards — Menu")
        self.geometry("700x460")
        self.resizable(False, False)

        # Deck: list of Flashcard objects (starts empty)
        self.deck: List[Flashcard] = []

        # UI
        self._build_main_menu()

    def _build_main_menu(self):
        frame = tk.Frame(self, padx=20, pady=20)
        frame.pack(expand=True, fill="both")

        title = tk.Label(frame, text="Simple Flashcards", font=("Arial", 22, "bold"))
        title.pack(pady=(4, 8))

        description = tk.Label(
            frame,
            text="No dataset initially — create flashcards using Manage → Add. "
                 "You can delete cards, view all cards, or test yourself.",
            wraplength=640,
            justify="center",
        )
        description.pack(pady=(0, 12))

        btn_frame = tk.Frame(frame)
        btn_frame.pack(pady=10)

        manage_btn = tk.Button(btn_frame, text="1) Manage Flashcards (Add / Delete)",
                               width=48, height=2, command=self.open_manage_window)
        manage_btn.grid(row=0, column=0, pady=6)

        show_btn = tk.Button(btn_frame, text="2) Show All Flashcards",
                              width=48, height=2, command=self.open_show_all_window)
        show_btn.grid(row=1, column=0, pady=6)

        test_btn = tk.Button(btn_frame, text="3) Test",
                              width=48, height=2, command=self.open_test_setup)
        test_btn.grid(row=2, column=0, pady=6)

        exit_btn = tk.Button(btn_frame, text="4) Exit", width=48, height=2, command=self.on_exit)
        exit_btn.grid(row=3, column=0, pady=6)

        self.status_label = tk.Label(frame, text=self._status_text())
        self.status_label.pack(pady=(10, 0))

    def _status_text(self) -> str:
        return f"Flashcards in deck: {len(self.deck)}"

    # ---------- Manage (Add/Delete) ----------
    def open_manage_window(self):
        w = tk.Toplevel(self)
        w.title("Manage Flashcards")
        w.geometry("720x480")
        w.resizable(False, False)

        left = tk.Frame(w, padx=12, pady=12)
        left.pack(side="left", fill="y")

        tk.Label(left, text="Add Flashcard", font=("Arial", 12, "bold")).pack(anchor="w")
        tk.Label(left, text="Question (front):").pack(anchor="w", pady=(6,0))
        front_entry = tk.Entry(left, width=40)
        front_entry.pack(anchor="w", pady=(0,8))

        tk.Label(left, text="Answer (back):").pack(anchor="w")
        back_entry = tk.Entry(left, width=40)
        back_entry.pack(anchor="w", pady=(0,8))

        def add_card():
            f = front_entry.get().strip()
            b = back_entry.get().strip()
            if not f or not b:
                messagebox.showwarning("Invalid", "Question and answer cannot be empty.")
                return
            self.deck.append(Flashcard(front=f, back=b))
            front_entry.delete(0, "end")
            back_entry.delete(0, "end")
            refresh_list()
            self.status_label.config(text=self._status_text())

        add_button = tk.Button(left, text="Add Flashcard", command=add_card, width=18)
        add_button.pack(pady=(6, 12))

        tk.Label(left, text="Delete Selected", font=("Arial", 12, "bold")).pack(anchor="w", pady=(12,0))
        del_button = tk.Button(left, text="Delete Selected", width=18, fg="white", bg="#d9534f")
        del_button.pack(pady=(6,0))
        # ---------- list display ----------
        right = tk.Frame(w, padx=12, pady=12)
        right.pack(side="right", fill="both", expand=True)

        tk.Label(right, text="Deck (select to delete)", font=("Arial", 12, "bold")).pack(anchor="w")
        listbox = tk.Listbox(right, width=60, height=22)
        listbox.pack(side="left", fill="both", expand=True, pady=(6,0))

        sb = tk.Scrollbar(right, orient="vertical", command=listbox.yview)
        sb.pack(side="right", fill="y")
        listbox.config(yscrollcommand=sb.set)

        def refresh_list():
            listbox.delete(0, "end")
            for i, c in enumerate(self.deck, start=1):
                preview = f"{i}. Q: {c.front[:70]}  |  A: {c.back[:70]}"
                listbox.insert("end", preview)

        def delete_selected():
            sel = listbox.curselection()
            if not sel:
                messagebox.showinfo("Delete", "No card selected.")
                return
            idx = sel[0]
            card = self.deck[idx]
            if messagebox.askyesno("Confirm Delete", f"Delete this card?\n\nQ: {card.front}\nA: {card.back}"):
                self.deck.pop(idx)
                refresh_list()
                self.status_label.config(text=self._status_text())

        del_button.config(command=delete_selected)
        refresh_list()

    # ---------- Show All ----------
    def open_show_all_window(self):
        w = tk.Toplevel(self)
        w.title("All Flashcards")
        w.geometry("720x480")
        w.resizable(False, False)

        tk.Label(w, text="All Flashcards", font=("Arial", 14, "bold")).pack(pady=(8,4))
        frame = tk.Frame(w, padx=12, pady=6)
        frame.pack(fill="both", expand=True)

        listbox = tk.Listbox(frame, width=92, height=24)
        listbox.pack(side="left", fill="both", expand=True)
        sb = tk.Scrollbar(frame, orient="vertical", command=listbox.yview)
        sb.pack(side="right", fill="y")
        listbox.config(yscrollcommand=sb.set)

        if not self.deck:
            listbox.insert("end", "No flashcards yet. Use Manage → Add Flashcard to create cards.")
        else:
            for i, c in enumerate(self.deck, start=1):
                listbox.insert("end", f"{i}. Q: {c.front}  —  A: {c.back}")

    # ---------- Test ----------
    def open_test_setup(self):
        if not self.deck:
            messagebox.showinfo("No Cards", "Deck is empty. Add flashcards first.")
            return

        w = tk.Toplevel(self)
        w.title("Test Setup")
        w.geometry("360x220")
        w.resizable(False, False)

        tk.Label(w, text="Test settings", font=("Arial", 12, "bold")).pack(pady=(10,6))

        dir_var = tk.StringVar(value="front_to_back")
        tk.Radiobutton(w, text="Question → Answer (front→back)", variable=dir_var, value="front_to_back").pack(anchor="w", padx=12)
        tk.Radiobutton(w, text="Answer → Question (back→front)", variable=dir_var, value="back_to_front").pack(anchor="w", padx=12)

        tk.Label(w, text="Number of questions (max deck size):").pack(pady=(10,0))
        n_entry = tk.Entry(w, width=6)
        n_entry.insert(0, str(len(self.deck)))
        n_entry.pack(pady=(4,6))

        def start():
            try:
                n = int(n_entry.get())
            except ValueError:
                messagebox.showwarning("Invalid", "Enter a number.")
                return
            n = max(1, min(n, len(self.deck)))
            w.destroy()
            self.open_test_window(direction=dir_var.get(), n_questions=n)

        tk.Button(w, text="Start Test", width=14, command=start).pack(pady=8)

    def open_test_window(self, direction: str = "front_to_back", n_questions: int = 0):
        # prepare pool
        n = n_questions or len(self.deck)
        pool = random.sample(self.deck, k=min(n, len(self.deck)))

        w = tk.Toplevel(self)
        w.title("Test")
        w.geometry("700x360")
        w.resizable(False, False)

        idx = {"i": 0}
        score = {"correct": 0, "total": 0}

        prompt = tk.Label(w, text="", font=("Arial", 14), wraplength=660, justify="left")
        prompt.pack(pady=(16,6))

        answer_entry = tk.Entry(w, width=90)
        answer_entry.pack(pady=(6,6))

        feedback = tk.Label(w, text="", font=("Arial", 11))
        feedback.pack(pady=(6,6))

        def show_card():
            i = idx["i"]
            if i >= len(pool):
                finish()
                return
            answer_entry.delete(0, "end")
            feedback.config(text="")
            c = pool[i]
            if direction == "front_to_back":
                prompt.config(text=f"Q: {c.front}")
            else:
                prompt.config(text=f"A: {c.back}")

        def check_answer():
            i = idx["i"]
            if i >= len(pool):
                return
            c = pool[i]
            user = answer_entry.get().strip()
            if direction == "front_to_back":
                correct = user.lower() == c.back.strip().lower()
                expected = c.back
            else:
                correct = user.lower() == c.front.strip().lower()
                expected = c.front
            score["total"] += 1
            if correct:
                score["correct"] += 1
                feedback.config(text=f"Correct! Expected: {expected}", fg="green")
            else:
                feedback.config(text=f"Incorrect. Expected: {expected}", fg="red")

        def next_card():
            check_answer()
            idx["i"] += 1
            if idx["i"] < len(pool):
                show_card()
            else:
                finish()

        def finish():
            messagebox.showinfo("Test Complete", f"You answered {score['correct']} out of {score['total']} correctly.")
            w.destroy()

        btn_frame = tk.Frame(w)
        btn_frame.pack(pady=(6,8))
        tk.Button(btn_frame, text="Check", width=14, command=check_answer).grid(row=0, column=0, padx=6)
        tk.Button(btn_frame, text="Check & Next", width=14, command=next_card).grid(row=0, column=1, padx=6)
        tk.Button(btn_frame, text="Stop Test", width=14, command=w.destroy).grid(row=0, column=2, padx=6)

        show_card()

    def on_exit(self):
        # optional: prompt to save using csvHandler.saveFlashcards if you want persistence
        if messagebox.askyesno("Exit", "Exit application?"):
            self.destroy()