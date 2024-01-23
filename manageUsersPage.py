from base import Base
from mongoDBConnection import MongoDBConnection
import tkinter as tk
from tkinter import ttk

class ManageUsersPage(Base):
    def __init__(self, master, user):
        super().__init__(master)
        self.user = user

        self.frame = tk.Frame(master)
        self.frame.grid()

        self.users_collection = MongoDBConnection.getInstance().get_users_collection()

        self.users_treeview = ttk.Treeview(self.frame, columns=('Username', 'Password', 'Role'), show='headings')
        self.users_treeview.pack()
        self.users_treeview.heading('Username', text='Username')
        self.users_treeview.heading('Password', text='Password')
        self.users_treeview.heading('Role', text='Role')
        self.users_treeview.bind('<<TreeviewSelect>>', self.on_treeview_select)

        self.populate_users_treeview()

        self.delete_user_button = tk.Button(self.frame, text="Usuń użytkownika", command=self.delete_user_button_click)
        self.delete_user_button.pack()

        self.username_label = tk.Label(self.frame, text="Login:")
        self.username_label.pack()

        self.username_label.pack()
        self.username_entry = tk.Entry(self.frame)
        self.username_entry.pack()

        self.password_label = tk.Label(self.frame, text="Nowe hasło:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.frame, show="*")
        self.password_entry.pack()

        self.role_label = tk.Label(self.frame, text="Role:")
        self.role_label.pack()
        self.role_var = tk.StringVar()
        self.role_options = ['admin', 'user']
        self.role_dropdown = ttk.OptionMenu(self.frame, self.role_var, 'user' , *self.role_options)
        self.role_dropdown.pack()

        self.add_user_button = tk.Button(self.frame, text="Dodaj użytkownika", command=self.add_user_button_click)
        self.add_user_button.pack()

        self.edit_user_button = tk.Button(self.frame, text="Edytuj użytkownika", command=self.edit_user_button_click)
        self.edit_user_button.pack()

        self.change_password_button = tk.Button(self.frame, text="Zmień hasło", command=self.change_password_button_click)
        self.change_password_button.pack()

        self.back_button = tk.Button(self.frame, text="Powrót", command=self.back_button_click)
        self.back_button.pack()

    def on_treeview_select(self, event):
        selected_items = self.users_treeview.selection()
        if selected_items:
            selected_item = selected_items[0]
            selected_username = self.users_treeview.item(selected_item)['values'][0]
            selected_role = self.users_treeview.item(selected_item)['values'][2]
            self.username_entry.delete(0, tk.END)
            self.username_entry.insert(0, selected_username)
            self.role_var.set(selected_role)


    def add_user_button_click(self):
        username = self.username_entry.get()
        role = self.role_var.get()
        password = self.password_entry.get()
        self.add_user(username, password, role)

    def edit_user_button_click(self):
        username = self.username_entry.get()
        new_role = self.role_var.get()
        password = self.password_entry.get()
        self.edit_user(username, password, new_role)

    def change_password_button_click(self):
        username = self.username_entry.get()
        new_password = self.password_entry.get()
        self.change_password(username, new_password)

    def add_user(self, username, password, role):
        try:
            user = {
                'username': username,
                'password': password,
                'role': role
            }
            self.users_collection.insert_one(user)
            self.populate_users_treeview()
            print('User added successfully.')
        except Exception as e:
            print('Error adding user:', str(e))

    def change_password(self, username, new_password):
        try:
            query = {'username': username}
            new_values = {'$set': {'password': new_password}}
            self.users_collection.update_one(query, new_values)
            print('Password changed successfully.')
        except Exception as e:
            print('Error changing password:', str(e))

    def edit_user(self, username, password, new_role):
        try:
            query = {'username': username}
            new_values = {'$set': {'password:': password, 'role': new_role}}
            self.users_collection.update_one(query, new_values)
            print('User updated successfully.')
        except Exception as e:
            print('Error editing user:', str(e))

    def remove_user(self, username):
        try:
            query = {'username': username}
            self.users_collection.delete_one(query)
            print('User removed successfully.')
        except Exception as e:
            print('Error removing user:', str(e))

    def populate_users_treeview(self):
        for i in self.users_treeview.get_children():
            self.users_treeview.delete(i)  # Clear the users_treeview
        users = self.get_users()  # Get all users from the database
        for user in users:
            self.users_treeview.insert('', 'end', values=(user['username'], user['password'], user['role']))  # Add the user details to the users_treeview

    def get_users(self):
        try:
            users = self.users_collection.find()
            return list(users)
        except Exception as e:
            print('Error getting users:', str(e))

    def delete_user_button_click(self):
        selected_user = self.users_treeview.item(self.users_treeview.selection())['values'][0]
        self.delete_user(selected_user)

    def delete_user(self, username):
        try:
            query = {'username': username}
            self.users_collection.delete_one(query)
            print('User deleted successfully.')
            self.populate_users_treeview()
        except Exception as e:
            print('Error deleting user:', str(e))
    
    def back_button_click(self):
        self.frame.destroy()
        from startingPage import StartingPage
        StartingPage(self, self.user)
            
