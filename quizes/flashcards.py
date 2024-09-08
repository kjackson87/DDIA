import json
import tkinter as tk
from tkinter import messagebox
import argparse

class QuizApp:
    def __init__(self, master, quiz_file):
        self.master = master
        self.master.title("Quiz Flashcards")
        self.master.geometry("600x400")

        self.questions = self.load_questions(quiz_file)
        self.current_question = 0

        # Create main content frame
        self.content_frame = tk.Frame(master)
        self.content_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        self.question_label = tk.Label(self.content_frame, text="", wraplength=550, justify="center")
        self.question_label.pack(expand=True)

        self.answer_label = tk.Label(self.content_frame, text="", wraplength=550, justify="center")
        self.answer_label.pack(expand=True)

        # Create bottom frame for buttons
        self.button_frame = tk.Frame(master)
        self.button_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=20)

        self.show_answer_button = tk.Button(self.button_frame, text="Show Answer", command=self.show_answer)
        self.show_answer_button.pack(side=tk.LEFT, padx=(0, 10))

        self.next_button = tk.Button(self.button_frame, text="Next Question", command=self.next_question)
        self.next_button.pack(side=tk.RIGHT)

        self.next_question()

    def load_questions(self, file_path):
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            return data['questions']
        except FileNotFoundError:
            messagebox.showerror("Error", f"File not found: {file_path}")
            raise
        except json.JSONDecodeError:
            messagebox.showerror("Error", f"Invalid JSON in file: {file_path}")
            raise
        except KeyError:
            messagebox.showerror("Error", f"Missing 'questions' key in JSON file: {file_path}")
            raise

    def next_question(self):
        if self.current_question < len(self.questions):
            question = self.questions[self.current_question]['question']
            self.question_label.config(text=question)
            self.answer_label.config(text="")
            self.show_answer_button.config(state=tk.NORMAL)
            self.current_question += 1
        else:
            messagebox.showinfo("Quiz Completed", "You've completed all questions!")
            self.current_question = 0
            self.next_question()

    def show_answer(self):
        if self.current_question > 0:
            answer = self.questions[self.current_question - 1]['answer']
            page = self.questions[self.current_question - 1]['page']
            self.answer_label.config(text=f"Answer: {answer}\n\nPage: {page}")
            self.show_answer_button.config(state=tk.DISABLED)

def parse_arguments():
    parser = argparse.ArgumentParser(description="Quiz Flashcard Application")
    parser.add_argument("quiz_file", help="Path to the JSON file containing quiz questions")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()

    try:
        root = tk.Tk()
        app = QuizApp(root, args.quiz_file)
        root.mainloop()
    except Exception as e:
        print(f"An error occurred: {e}")