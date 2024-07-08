# quiz_app.py
# This script defines the QuizApp class which handles the quiz functionality,
# including user login, displaying questions, checking answers, and showing the leaderboard.

import tkinter as tk
from tkinter import ttk, messagebox
from question import Question

class QuizApp:
    """
    The QuizApp class manages the quiz application's GUI and functionality.
    """
    
    def __init__(self, master, login_manager):
        """
        Initialize the QuizApp.
        
        Parameters:
        master (tk.Tk): The main Tkinter window.
        login_manager: Manages user login functionality.
        """
        self.master = master
        self.master.title("Quiz Application")
        self.master.configure(bg='#704B9E')  # Kahoot-like purple background

        self.login_manager = login_manager

        # Initialize quiz-related attributes
        self.questions = []
        self.score = 0
        self.current_question_index = 0
        self.leaderboard = []

        # Initialize GUI elements
        self.label_username = None
        self.entry_username = None
        self.label_password = None
        self.entry_password = None
        self.btn_login = None
        self.label_question = None
        self.radio_buttons = []
        self.var_option = None
        self.btn_submit = None
        self.btn_next = None
        self.btn_logout = None

        # Show the login screen
        self.show_login()

    def show_login(self):
        """
        Display the login screen for user authentication.
        """
        self.clear_window()

        # Create and pack username label and entry
        self.label_username = tk.Label(self.master, text="Username:", bg='#704B9E', fg='white', font=('Arial', 14))
        self.label_username.pack(pady=10)
        self.entry_username = ttk.Entry(self.master, font=('Arial', 14))
        self.entry_username.pack()

        # Create and pack password label and entry
        self.label_password = tk.Label(self.master, text="Password:", bg='#704B9E', fg='white', font=('Arial', 14))
        self.label_password.pack(pady=10)
        self.entry_password = ttk.Entry(self.master, show="*", font=('Arial', 14))
        self.entry_password.pack()

        # Create and pack login button
        self.btn_login = ttk.Button(self.master, text="Login", command=self.login, style='TButton')
        self.btn_login.pack(pady=20)

        # Set focus to the username entry
        self.entry_username.focus()

    def login(self):
        """
        Validate the login credentials and show the quiz screen if valid.
        """
        username = self.entry_username.get()
        password = self.entry_password.get()

        if self.login_manager.validate_login(username, password):
            self.show_quiz()
        else:
            messagebox.showerror("Error", "Username and Password are required!")

    def show_quiz(self):
        """
        Display the quiz screen with the current question and answer options.
        """
        self.clear_window()

        # Example questions for demonstration
        self.questions = [
            Question("What is the capital of France?", ["A. London", "B. Paris", "C. Rome", "D. Madrid"], "B"),
            Question("What is 2 + 2?", ["A. 3", "B. 4", "C. 5", "D. 6"], "B"),
            Question("Who painted the Mona Lisa?", ["A. Van Gogh", "B. Leonardo da Vinci", "C. Picasso", "D. Michelangelo"], "B"),
        ]
        
        self.score = 0
        self.current_question_index = 0

        # Create and pack question label
        self.label_question = tk.Label(self.master, text="", bg='#704B9E', fg='white', font=('Arial', 18, 'bold'))
        self.label_question.pack(pady=20)

        # Initialize variable for selected option
        self.var_option = tk.StringVar()

        # Create and pack radio buttons for options
        self.radio_buttons = []
        for i in range(4):
            radio_option = ttk.Radiobutton(self.master, text="", variable=self.var_option, value="", style='TRadiobutton')
            radio_option.pack(pady=5)
            self.radio_buttons.append(radio_option)

        # Create and pack submit button
        self.btn_submit = ttk.Button(self.master, text="Submit", command=self.check_answer, style='TButton')
        self.btn_submit.pack(pady=20)

        # Create and pack next button (initially disabled)
        self.btn_next = ttk.Button(self.master, text="Next", command=self.next_question, state="disabled", style='TButton')
        self.btn_next.pack(pady=20)

        # Create and pack logout button
        self.btn_logout = ttk.Button(self.master, text="Logout", command=self.logout, style='TButton')
        self.btn_logout.pack(pady=20)

        # Load the first question
        self.load_question()

    def load_question(self):
        """
        Load and display the current question and its answer options.
        """
        question = self.questions[self.current_question_index]
        self.label_question.config(text=question.text)

        # Update radio buttons with answer options
        for i, option in enumerate(question.options):
            self.radio_buttons[i].config(text=option, value=option[0])

    def check_answer(self):
        """
        Check the selected answer, update the score, and display feedback.
        """
        answer = self.var_option.get()
        question = self.questions[self.current_question_index]

        if answer.upper() == question.correct_answer:
            self.score += 1
            messagebox.showinfo("Correct", "Correct Answer!")
        else:
            messagebox.showinfo("Incorrect", f"Incorrect! Correct answer is {question.correct_answer}")

        # Disable submit button and enable next button
        self.btn_submit.config(state="disabled")
        self.btn_next.config(state="normal")

    def next_question(self):
        """
        Move to the next question or show the leaderboard if the quiz is finished.
        """
        self.current_question_index += 1

        if self.current_question_index < len(self.questions):
            self.load_question()
            self.var_option.set("")
            self.btn_submit.config(state="normal")
            self.btn_next.config(state="disabled")
        else:
            self.show_leaderboard()

    def show_leaderboard(self):
        """
        Display the leaderboard with scores of all players.
        """
        self.clear_window()

        # Update leaderboard with current user and score
        self.update_leaderboard(self.login_manager.Username, self.score)

        # Create and pack leaderboard label
        label_leaderboard = tk.Label(self.master, text="Leaderboard:", bg='#704B9E', fg='white', font=('Arial', 18, 'bold'))
        label_leaderboard.pack(pady=20)

        # Display each leaderboard entry
        for i, (username, score) in enumerate(self.leaderboard, 1):
            label_score = tk.Label(self.master, text=f"{i}. {username}: {score}", bg='#704B9E', fg='white', font=('Arial', 14))
            label_score.pack()

        # Create and pack logout button
        btn_logout = ttk.Button(self.master, text="Logout", command=self.logout, style='TButton')
        btn_logout.pack(pady=20)

    def update_leaderboard(self, username, score):
        """
        Update and sort the leaderboard by score in descending order.
        
        Parameters:
        username (str): The username of the player.
        score (int): The score of the player.
        """
        self.leaderboard.append((username, score))
        self.leaderboard.sort(key=lambda x: x[1], reverse=True)

    def logout(self):
        """
        Logout the current user and return to the login screen.
        """
        self.show_login()

    def clear_window(self):
        """
        Remove all widgets from the current window.
        """
        for widget in self.master.winfo_children():
            widget.destroy()

# The Question class should be defined in question.py and should include
# attributes for the question text, options, and the correct answer.
# Example:
# class Question:
#     def __init__(self, text, options, correct_answer):
#         self.text = text
#         self.options = options
#         self.correct_answer = correct_answer.upper()  # Ensure correct_answer is uppercase