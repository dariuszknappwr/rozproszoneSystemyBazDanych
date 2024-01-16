from pymongo import MongoClient
import tkinter as tk

class ManageUsersPage(Base):
    def __init__(self):
        super().__init__()

        client = MongoClient('mongodb://localhost:27017/')
        db = client['your_database_name']
        self.users_collection = db['users']

        self.username_label = tk.Label(self.root, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        # Role label and entry field
        self.role_label = tk.Label(self.root, text="Role:")
        self.role_label.pack()
        self.role_entry = tk.Entry(self.root)
        self.role_entry.pack()

        # Add User button
        self.add_user_button = tk.Button(self.root, text="Add User", command=self.add_user_button_click)
        self.add_user_button.pack()

        # Edit User button
        self.edit_user_button = tk.Button(self.root, text="Edit User", command=self.edit_user_button_click)
        self.edit_user_button.pack()

        # Remove User button
        self.remove_user_button = tk.Button(self.root, text="Remove User", command=self.remove_user_button_click)
        self.remove_user_button.pack()

    def add_user(self, username, role):
        user = {
            'username': username,
            'role': role
        }
        self.users_collection.insert_one(user)
        print('User added successfully.')

    def edit_user(self, username, new_role):
        query = {'username': username}
        new_values = {'$set': {'role': new_role}}
        self.users_collection.update_one(query, new_values)
        print('User updated successfully.')

    def remove_user(self, username):
        query = {'username': username}
        self.users_collection.delete_one(query)
        print('User removed successfully.')

    def add_user_button_click(self):
        username = self.username_entry.get()
        role = self.role_entry.get()
        self.add_user(username, role)

    def edit_user_button_click(self):
        username = self.username_entry.get()
        new_role = self.role_entry.get()
        self.edit_user(username, new_role)

    def remove_user_button_click(self):
        username = self.username_entry.get()
        self.remove_user(username)

    def run(self):
        # Start the Tkinter event loop
        self.root.mainloop()

# Create an instance of ManageUsersPage and run it
manage_users_page = ManageUsersPage()
manage_users_page.run()
