from base import Base
import tkinter as tk
from mongoDBConnection import MongoDBConnection
from tkinter import ttk

class ManageDriversPage(Base):
    def __init__(self, master, user):
        super().__init__(master)
        self.user = user

        self.frame = tk.Frame(master)
        self.frame.grid()

        self.drivers_collection = MongoDBConnection.getInstance().get_drivers_collection()

        self.drivers_treeview = ttk.Treeview(self.frame, columns=('Imię', 'Nazwisko', 'Identyfikator'), show='headings')
        self.drivers_treeview.pack()
        self.drivers_treeview.heading('Imię', text='Imię')
        self.drivers_treeview.heading('Nazwisko', text='Nazwisko')
        self.drivers_treeview.heading('Identyfikator', text='Identyfikator')
        self.drivers_treeview.bind('<<TreeviewSelect>>', self.on_treeview_select)

        self.info_label = tk.Label(self.frame, text="")
        self.info_label.pack()

        self.populate_drivers_treeview()

        self.delete_driver_button = tk.Button(self.frame, text="Usuń kierowcę", command=self.delete_driver_button_click)
        if self.user['role'] == 'admin':
            self.delete_driver_button.pack()

        self.name_label = tk.Label(self.frame, text="Imię:")
        self.name_label.pack()

        self.name_entry = tk.Entry(self.frame)
        self.name_entry.pack()

        self.surname_label = tk.Label(self.frame, text="Nazwisko:")
        self.surname_label.pack()

        self.surname_entry = tk.Entry(self.frame)
        self.surname_entry.pack()

        self.id_label = tk.Label(self.frame, text="Identyfikator:")
        self.id_label.pack()

        self.id_entry = tk.Entry(self.frame)
        self.id_entry.pack()

        tk.Label(self.frame, text="").pack(pady=10)

        self.add_driver_button = tk.Button(self.frame, text="Dodaj kierowcę", command=self.add_driver_button_click)
        if self.user['role'] == 'admin':
            self.add_driver_button.pack()

        self.edit_driver_button = tk.Button(self.frame, text="Edytuj kierowcę", command=self.edit_driver_button_click)
        if self.user['role'] == 'admin':
            self.edit_driver_button.pack()

        self.back_button = tk.Button(self.frame, text="Powrót", command=self.back_button_click)
        self.back_button.pack()

    def on_treeview_select(self, event):
        selected_items = self.drivers_treeview.selection()
        if len(selected_items) > 0:
            values = self.drivers_treeview.item(selected_items[0])['values']
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, values[0])
            self.surname_entry.delete(0, tk.END)
            self.surname_entry.insert(0, values[1])
            self.id_entry.delete(0, tk.END)
            self.id_entry.insert(0, values[2])

    def populate_drivers_treeview(self):
        self.clear_drivers_treeview()
        drivers = self.drivers_collection.find()
        for driver in drivers:
            self.drivers_treeview.insert('', tk.END, values=(driver['name'], driver['surname'], driver['id']))

    def clear_drivers_treeview(self):
        self.drivers_treeview.delete(*self.drivers_treeview.get_children())

    def delete_driver_button_click(self):
        selected_items = self.drivers_treeview.selection()
        if selected_items:
            selected_item = selected_items[0]
            selected_name = self.drivers_treeview.item(selected_item)['values'][0]
            selected_surname = self.drivers_treeview.item(selected_item)['values'][1]
            selected_id = self.drivers_treeview.item(selected_item)['values'][2]
            self.drivers_collection.delete_one({'name': selected_name, 'surname': selected_surname, 'id': selected_id})
            self.populate_drivers_treeview()
            self.info_label.config(text='Usuwanie kierowcy przebiegło pomyślnie.')
        else:
            self.info_label.config(text='Proszę wybrać kierowcę.')

    def add_driver_button_click(self):
        name = self.name_entry.get()
        surname = self.surname_entry.get()
        id = self.id_entry.get()
        if name and surname and id:
            self.drivers_collection.insert_one({'name': name, 'surname': surname, 'id': id})
            self.populate_drivers_treeview()
        else:
            self.info_label.config(text='Proszę wypełnić wszystkie pola.')

    def edit_driver_button_click(self):
        selected_items = self.drivers_treeview.selection()
        if selected_items:
            selected_item = selected_items[0]
            selected_name = self.drivers_treeview.item(selected_item)['values'][0]
            selected_surname = self.drivers_treeview.item(selected_item)['values'][1]
            selected_id = self.drivers_treeview.item(selected_item)['values'][2]

            name = self.name_entry.get()
            surname = self.surname_entry.get()
            id = self.id_entry.get()

            if name and surname and id:
                self.drivers_collection.update_one({'name': selected_name, 'surname': selected_surname, 'id': selected_id}, {'$set': {'name': name, 'surname': surname, 'id': id}})
                self.populate_drivers_treeview()
                self.info_label.config(text='Edycja kierowcy przebiegła pomyślnie.')
            else:
                self.info_label.config(text='Proszę wypełnić wszystkie pola.')
        else:
            self.info_label.config(text='Proszę wybrać kierowcę.')

    def back_button_click(self):
        self.frame.destroy()
        from startingPage import StartingPage
        StartingPage(self.master, self.user)


