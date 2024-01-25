from base import Base
from mongoDBConnection import MongoDBConnection
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry


class ManageRoutesPage(Base):
    def __init__(self, master, user):
        super().__init__(master)
        self.user = user

        self.frame = tk.Frame(master)
        self.frame.grid()

        self.routes_collection = MongoDBConnection.getInstance().get_routes_collection()
        self.drivers_collection = MongoDBConnection.getInstance().get_drivers_collection()
        self.vehicles_collection = MongoDBConnection.getInstance().get_vehicles_collection()

        self.routes_treeview = ttk.Treeview(self.frame, columns=('Data', 'Kierowca', 'Pojazd', 'Punkt docelowy'), show='headings')
        self.routes_treeview.pack()
        self.routes_treeview.heading('Data', text='Data')
        self.routes_treeview.heading('Kierowca', text='Kierowca')
        self.routes_treeview.heading('Pojazd', text='Pojazd')
        self.routes_treeview.heading('Punkt docelowy', text='punkt docelowy')
        self.routes_treeview.bind('<<TreeviewSelect>>', self.on_treeview_select)

        self.info_label = tk.Label(self.frame, text="")
        self.info_label.pack()

        self.sort_order = {col: 'ascending' for col in self.routes_treeview['columns']}

        for col in self.routes_treeview['columns']:
            self.routes_treeview.heading(col, text=col, command=lambda _col=col: self.on_heading_click(_col))

        self.filter_label = tk.Label(self.frame, text="Kliknij na nagłówku tabeli aby posortować")
        self.filter_label.pack()

        self.filter_label = tk.Label(self.frame, text="Filtruj punkty docelowe:")
        self.filter_label.pack()

        self.filter_entry = tk.Entry(self.frame)
        self.filter_entry.pack()
        self.filter_entry.bind('<KeyRelease>', self.on_filter_change)

        self.populate_routes_treeview()

        self.delete_route_button = tk.Button(self.frame, text="Usuń trasę", command=self.delete_route_button_click)
        self.delete_route_button.pack()

        self.date_label = tk.Label(self.frame, text="Data:")
        self.date_label.pack()

        self.date_entry = DateEntry(self.frame)
        self.date_entry.pack()

        self.driver_label = tk.Label(self.frame, text="Kierowca:")
        self.driver_label.pack()

        self.driver_entry = ttk.Combobox(self.frame, values=self.get_drivers())
        self.driver_entry.pack()

        self.vehicle_label = tk.Label(self.frame, text="Pojazd:")
        self.vehicle_label.pack()

        self.vehicle_entry = ttk.Combobox(self.frame, values=self.get_vehicles())
        self.vehicle_entry.pack()

        self.route_label = tk.Label(self.frame, text="Punkt docelowy:")
        self.route_label.pack()

        self.route_entry = tk.Entry(self.frame)
        self.route_entry.pack()

        self.add_route_button = tk.Button(self.frame, text="Dodaj trasę", command=self.add_route_button_click)
        self.add_route_button.pack()

        self.edit_route_button = tk.Button(self.frame, text="Edytuj trasę", command=self.edit_route_button_click)
        if self.user['role'] == 'admin':
            self.edit_route_button.pack()

        self.back_button = tk.Button(self.frame, text="Powrót", command=self.back_button_click)
        self.back_button.pack()

    def on_treeview_select(self, event):
        selected_items = self.routes_treeview.selection()
        if len(selected_items) > 0:
            values = self.routes_treeview.item(selected_items[0])['values']
            self.date_entry.delete(0, tk.END)
            self.date_entry.insert(0, values[0])
            self.driver_entry.delete(0, tk.END)
            self.driver_entry.insert(0, values[1])
            self.vehicle_entry.delete(0, tk.END)
            self.vehicle_entry.insert(0, values[2])
            self.route_entry.delete(0, tk.END)
            self.route_entry.insert(0, values[3])

    def populate_routes_treeview(self, filter_text=''):
        self.clear_routes_treeview()
        routes = self.routes_collection.find()
        for route in routes:
            if filter_text.lower() in route['route'].lower():
                self.routes_treeview.insert('', tk.END, values=(route['date'], route['driver'], route['vehicle'], route['route']))

    def clear_routes_treeview(self):
        self.routes_treeview.delete(*self.routes_treeview.get_children())

    def delete_route_button_click(self):
        selected_items = self.routes_treeview.selection()
        if selected_items:
            selected_item = selected_items[0]
            selected_date = self.routes_treeview.item(selected_item)['values'][0]
            selected_driver = self.routes_treeview.item(selected_item)['values'][1]
            selected_vehicle = self.routes_treeview.item(selected_item)['values'][2]
            selected_route = self.routes_treeview.item(selected_item)['values'][3]
            self.routes_collection.delete_one({'date': selected_date, 'driver': selected_driver, 'vehicle': selected_vehicle, 'route': selected_route})
            self.populate_routes_treeview()

    def add_route_button_click(self):
        date = self.date_entry.get()
        driver = self.driver_entry.get()
        vehicle = self.vehicle_entry.get()
        route = self.route_entry.get()
        if date and driver and vehicle and route:
            self.routes_collection.insert_one({'date': date, 'driver': driver, 'vehicle': vehicle, 'route': route})
            self.populate_routes_treeview()
        else:
            self.info_label.config(text='Proszę wypełnić wszystkie pola.')

    def edit_route_button_click(self):
        selected_items = self.routes_treeview.selection()
        if selected_items:
            selected_item = selected_items[0]
            selected_date = self.routes_treeview.item(selected_item)['values'][0]
            selected_driver = self.routes_treeview.item(selected_item)['values'][1]
            selected_vehicle = self.routes_treeview.item(selected_item)['values'][2]
            selected_route = self.routes_treeview.item(selected_item)['values'][3]

            date = self.date_entry.get()
            driver = self.driver_entry.get()
            vehicle = self.vehicle_entry.get()
            route = self.route_entry.get()

            if date and driver and vehicle and route:
                self.routes_collection.update_one({'date': selected_date, 'driver': selected_driver, 'vehicle': selected_vehicle, 'route': selected_route}, {'$set': {'date': date, 'driver': driver, 'vehicle': vehicle, 'route': route}})
                self.populate_routes_treeview()
                self.info_label.config(text='Edycja trasy przebiegła pomyślnie.')
            else:
                self.info_label.config(text='Proszę wypełnić wszystkie pola.')
        else:
            self.info_label.config(text='Proszę wybrać trasę.')

    def get_drivers(self):
        drivers = self.drivers_collection.find()
        drivers_list = []
        for driver in drivers:
            drivers_list.append(driver['name'] + ' ' + driver['surname'])
        return drivers_list
    
    def get_vehicles(self):
        vehicles = self.vehicles_collection.find()
        vehicles_list = []
        for vehicle in vehicles:
            vehicles_list.append(vehicle['brand'] + ' ' + vehicle['model'] + ' ' + vehicle['license_plate_number'])
        return vehicles_list
    
    def get_routes(self):
        routes = self.routes_collection.find()
        routes_list = []
        for route in routes:
            routes_list.append(route['route'])
        return routes_list
    
    def on_filter_change(self, event):
        filter_text = self.filter_entry.get()
        self.populate_routes_treeview(filter_text)

    def on_heading_click(self, col):
        # Switch the sort order for the clicked column
        self.sort_order[col] = 'descending' if self.sort_order[col] == 'ascending' else 'ascending'

        # Rearrange the items in the treeview
        data = [(self.routes_treeview.set(child, col), child) for child in self.routes_treeview.get_children('')]
        data.sort(reverse=(self.sort_order[col] == 'descending'))

        for indx, item in enumerate(data):
            self.routes_treeview.move(item[1], '', indx)

    


    def back_button_click(self):
        self.frame.destroy()
        from startingPage import StartingPage
        StartingPage(self.master, self.user)
