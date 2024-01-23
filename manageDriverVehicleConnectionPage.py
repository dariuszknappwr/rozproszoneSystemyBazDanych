from base import Base
import tkinter as tk
from mongoDBConnection import MongoDBConnection
from tkinter import ttk

class ManageDriverVehicleConnectionPage(Base):
    def __init__(self, master, user):
        super().__init__(master)
        self.user = user

        self.frame = tk.Frame(master)
        self.frame.grid()

        self.drivers_collection = MongoDBConnection.getInstance().get_drivers_collection()
        self.vehicles_collection = MongoDBConnection.getInstance().get_vehicles_collection()
        self.drivers_vehicles_collection = MongoDBConnection.getInstance().get_drivers_vehicles_collection()

        self.drivers_vehicles_treeview = ttk.Treeview(self.frame, columns=('Imię', 'Nazwisko', 'Identyfikator', 'Marka', 'Model', 'Data rejestracji', 'nr tablicy rejestracyjnej'), show='headings')
        self.drivers_vehicles_treeview.pack()
        self.drivers_vehicles_treeview.heading('Imię', text='Imię')
        self.drivers_vehicles_treeview.heading('Nazwisko', text='Nazwisko')
        self.drivers_vehicles_treeview.heading('Identyfikator', text='Identyfikator')
        self.drivers_vehicles_treeview.heading('Marka', text='Marka')
        self.drivers_vehicles_treeview.heading('Model', text='Model')
        self.drivers_vehicles_treeview.heading('Data rejestracji', text='Data rejestracji')
        self.drivers_vehicles_treeview.heading('nr tablicy rejestracyjnej', text='nr tablicy rejestracyjnej')
        self.drivers_vehicles_treeview.bind('<<TreeviewSelect>>', self.on_treeview_select)

        self.populate_drivers_vehicles_treeview()

        self.disconnect_driver_vehicle_button = tk.Button(self.frame, text="Rozłącz kierowcę z pojazdem", command=self.disconnect_driver_vehicle_button_click)
        self.disconnect_driver_vehicle_button.pack()
        

        self.drivers_treeview = ttk.Treeview(self.frame, columns=('Imię', 'Nazwisko', 'Identyfikator'), show='headings')
        self.drivers_treeview.pack()
        self.drivers_treeview.heading('Imię', text='Imię')
        self.drivers_treeview.heading('Nazwisko', text='Nazwisko')
        self.drivers_treeview.heading('Identyfikator', text='Identyfikator')
        self.drivers_treeview.bind('<<TreeviewSelect>>', self.on_treeview_select)

        self.populate_drivers_treeview()

        self.vehicles_treeview = ttk.Treeview(self.frame, columns=('Marka', 'Model', 'Data rejestracji', 'nr tablicy rejestracyjnej', 'kierowca'), show='headings')
        self.vehicles_treeview.pack()
        self.vehicles_treeview.heading('Marka', text='Marka')
        self.vehicles_treeview.heading('Model', text='Model')
        self.vehicles_treeview.heading('Data rejestracji', text='Data rejestracji')
        self.vehicles_treeview.heading('nr tablicy rejestracyjnej', text='nr tablicy rejestracyjnej')
        self.vehicles_treeview.heading('kierowca', text='kierowca')
        self.vehicles_treeview.bind('<<TreeviewSelect>>', self.on_treeview_select)

        self.populate_vehicles_treeview()

        self.connect_driver_vehicle_button = tk.Button(self.frame, text="Połącz kierowcę z pojazdem", command=self.connect_driver_vehicle_button_click)
        self.connect_driver_vehicle_button.pack()



        self.back_button = tk.Button(self.frame, text="Powrót", command=self.back_button_click)
        self.back_button.pack()

    def on_treeview_select(self, event):
        selected_items = self.drivers_vehicles_treeview.selection()
        if len(selected_items) > 0:
            values = self.drivers_vehicles_treeview.item(selected_items[0])['values']
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, values[0])
            self.surname_entry.delete(0, tk.END)
            self.surname_entry.insert(0, values[1])
            self.id_entry.delete(0, tk.END)
            self.id_entry.insert(0, values[2])
            self.brand_entry.delete(0, tk.END)
            self.brand_entry.insert(0, values[3])
            self.model_entry.delete(0, tk.END)
            self.model_entry.insert(0, values[4])
            self.registration_date_entry.delete(0, tk.END)
            self.registration_date_entry.insert(0, values[5])
            self.license_plate_number_entry.delete(0, tk.END)
            self.license_plate_number_entry.insert(0, values[6])

    def populate_drivers_vehicles_treeview(self):
        self.clear_drivers_vehicles_treeview()
        drivers_vehicles = self.drivers_vehicles_collection.find()
        for driver_vehicle in drivers_vehicles:
            driver = self.drivers_collection.find_one({'id': driver_vehicle['driver_id']})
            vehicle = self.vehicles_collection.find_one({'_id': driver_vehicle['vehicle_id']})
            self.drivers_vehicles_treeview.insert('', tk.END, values=(driver['name'], driver['surname'], driver['id'], vehicle['brand'], vehicle['model'], vehicle['registration_date'], vehicle['license_plate_number']))

    def clear_drivers_vehicles_treeview(self):
        self.drivers_vehicles_treeview.delete(*self.drivers_vehicles_treeview.get_children())

    def populate_drivers_treeview(self):
        self.clear_drivers_treeview()
        drivers = self.drivers_collection.find()
        for driver in drivers:
            self.drivers_treeview.insert('', tk.END, values=(driver['name'], driver['surname'], driver['id']))

    def clear_drivers_treeview(self):
        self.drivers_treeview.delete(*self.drivers_treeview.get_children())

    def populate_vehicles_treeview(self):
        self.clear_vehicles_treeview()
        vehicles = self.vehicles_collection.find()
        for vehicle in vehicles:
            self.vehicles_treeview.insert('', tk.END, values=(vehicle['brand'], vehicle['model'], vehicle['registration_date'], vehicle['license_plate_number'], vehicle['driver']))

    def clear_vehicles_treeview(self):
        self.vehicles_treeview.delete(*self.vehicles_treeview.get_children())

    def disconnect_driver_vehicle_button_click(self):
        selected_items = self.drivers_vehicles_treeview.selection()
        if selected_items:
            selected_item = selected_items[0]
            selected_name = self.drivers_vehicles_treeview.item(selected_item)['values'][0]
            selected_surname = self.drivers_vehicles_treeview.item(selected_item)['values'][1]
            selected_id = self.drivers_vehicles_treeview.item(selected_item)['values'][2]
            selected_brand = self.drivers_vehicles_treeview.item(selected_item)['values'][3]
            selected_model = self.drivers_vehicles_treeview.item(selected_item)['values'][4]
            selected_registration_date = self.drivers_vehicles_treeview.item(selected_item)['values'][5]
            selected_license_plate_number = self.drivers_vehicles_treeview.item(selected_item)['values'][6]
            driver = self.drivers_collection.find_one({'name': selected_name, 'surname': selected_surname, 'id': selected_id})
            vehicle = self.vehicles_collection.find_one({'brand': selected_brand, 'model': selected_model, 'registration_date': selected_registration_date, 'license_plate_number': selected_license_plate_number})
            self.drivers_vehicles_collection.delete_one({'driver_id': driver['_id'], 'vehicle_id': vehicle['_id']})
            self.populate_drivers_vehicles_treeview()
            print('Driver disconnected from vehicle successfully.')
        else:
            print('Please select a driver-vehicle connection')

    def connect_driver_vehicle_button_click(self):
        selected_items = self.drivers_treeview.selection()
        if selected_items:
            selected_item = selected_items[0]
            selected_name = self.drivers_treeview.item(selected_item)['values'][0]
            selected_surname = self.drivers_treeview.item(selected_item)['values'][1]
            selected_id = self.drivers_treeview.item(selected_item)['values'][2]
            selected_brand = self.vehicles_treeview.item(selected_item)['values'][0]
            selected_model = self.vehicles_treeview.item(selected_item)['values'][1]
            selected_registration_date = self.vehicles_treeview.item(selected_item)['values'][2]
            selected_license_plate_number = self.vehicles_treeview.item(selected_item)['values'][3]
            driver = self.drivers_collection.find_one({'name': selected_name, 'surname': selected_surname, 'id': selected_id})
            vehicle = self.vehicles_collection.find_one({'brand': selected_brand, 'model': selected_model, 'registration_date': selected_registration_date, 'license_plate_number': selected_license_plate_number})
            self.drivers_vehicles_collection.insert_one({'driver_id': driver['_id'], 'vehicle_id': vehicle['_id']})
            self.populate_drivers_vehicles_treeview()
            print('Driver connected to vehicle successfully.')
        else:
            print('Please select a driver')

    def back_button_click(self):
        self.frame.destroy()
        from startingPage import StartingPage
        StartingPage(self.master, self.user)


