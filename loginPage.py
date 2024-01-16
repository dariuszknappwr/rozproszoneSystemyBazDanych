from base import Base
from mongoDBConnection import MongoDBConnection
import tkinter as tk
from pymongo import MongoClient, errors

class LoginPage(Base):
    def __init__(self, master):
        super().__init__(master)

        self.frame = tk.Frame(master)
        self.frame.grid()
        
        self.welcomeLabel = tk.Label(self.frame, text="Witaj w systemie zarządzania flotą pojazdów", font=("Arial", 16))
        self.welcomeLabel.grid(row=0, column=0, columnspan=2)
        self.usernameLabel = tk.Label(self.frame, text="Login:")
        self.usernameLabel.grid(row=1, column=0)
        self.usernameEntry = tk.Entry(self.frame, width=25)
        self.usernameEntry.grid(row=1, column=1)
        self.passwordLabel = tk.Label(self.frame, text="Hasło:")
        self.passwordLabel.grid(row=2, column=0)
        self.passwordEntry = tk.Entry(self.frame, width=25)
        self.passwordEntry.grid(row=2, column=1)
        self.button1 = tk.Button(self.frame, text='Zaloguj', width=25, command=self.login)
        self.button1.grid(row=3, column=0, columnspan=2)
        self.errorLabel = tk.Label(self.frame)
        self.errorLabel.grid(row=4, column=0, columnspan=2)  # Add an empty error label

    def login(self):
        try:
            MongoDBConnection.getInstance().client.server_info() #to force to call to the server and check that it is available
        except errors.ServerSelectionTimeoutError as err:
            self.errorLabel.config(text="Nie można połączyć z bazą danych")  # Update the error label text
            return

        users = MongoDBConnection.getInstance().get_users_collection()

        username = self.usernameEntry.get()
        password = self.passwordEntry.get()

        user = users.find_one({'username': username, 'password': password})

        if user is not None:
            from startingPage import StartingPage
            self.change_window(StartingPage, user)
        else:
            self.errorLabel.config(text="Nie znaleziono użytkownika lub hasła")  # Update the error label text
