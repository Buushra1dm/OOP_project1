# login_manager.py
# This script defines the LoginManager class which handles user authentication.

class LoginManager:
    """
    The LoginManager class manages user authentication.
    """
    
    def __init__(self):
        """
        Initialize the LoginManager with predefined users.
        """
        # Predefined users and passwords
        self.users = {
            "azam": "azam",
            "omar": "omar",
            "ahmed": "ahmed"
        }
        self.Username = ""
        self.PassWord = ""

    def validate_login(self, username, password):
        """
        Validate the username and password against predefined users.
        
        Parameters:
        username (str): The username entered by the user.
        password (str): The password entered by the user.
        
        Returns:
        bool: True if the username and password are valid, False otherwise.
        """
        if username in self.users and self.users[username] == password:
            self.Username = username
            self.PassWord = password
            return True
        else:
            return False