# main.py
import tkinter as tk
from login_manager import LoginManager
from quiz_app import QuizApp

def main():
    root = tk.Tk()
    login_manager = LoginManager()
    app = QuizApp(root, login_manager)
    root.mainloop()

if __name__ == "__main__":
    main()