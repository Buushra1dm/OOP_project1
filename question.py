# question.py

class Question:
    def __init__(self, text, options, correct_answer):
        self.text = text
        self.options = options
        self.correct_answer = correct_answer.upper()  # Ensure correct_answer is uppercase