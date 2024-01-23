
from base import Base
from mongoDBConnection import MongoDBConnection
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry


class ManageVehiclesPage(Base):
    def __init__(self, master, user):
        super().__init__(master)
        self.user = user

        self.frame = tk.Frame(master)
        self.frame.grid()

        self.vehicles_collection = MongoDBConnection.getInstance().get_vehicles_collection()

        self.vehicles_treeview = ttk.Treeview(self.frame, columns=('Marka', 'Model', 'Data rejestracji', 'nr tablicy rejestracyjnej', 'kierowca'), show='headings')
        self.vehicles_treeview.pack()
        self.vehicles_treeview.heading('Marka', text='Marka')
        self.vehicles_treeview.heading('Model', text='Model')
        self.vehicles_treeview.heading('Data rejestracji', text='Data rejestracji')
        self.vehicles_treeview.heading('nr tablicy rejestracyjnej', text='nr tablicy rejestracyjnej')
        self.vehicles_treeview.heading('kierowca', text='kierowca')
        self.vehicles_treeview.bind('<<TreeviewSelect>>', self.on_treeview_select)

        self.populate_vehicles_treeview()

        self.brand_label = tk.Label(self.frame, text="Marka:")
        self.brand_label.pack()

        self.brand_entry = tk.Entry(self.frame)
        self.brand_entry.pack()

        self.model_label = tk.Label(self.frame, text="Model:")
        self.model_label.pack()

        self.model_entry = tk.Entry(self.frame)
        self.model_entry.pack()

        self.registration_date_label = tk.Label(self.frame, text="Data rejestracji:")
        self.registration_date_label.pack()

        self.registration_date_entry = DateEntry(self.frame)
        self.registration_date_entry.pack()

        self.license_plate_number_label = tk.Label(self.frame, text="nr tablicy rejestracyjnej:")
        self.license_plate_number_label.pack()

        self.license_plate_number_entry = tk.Entry(self.frame)
        self.license_plate_number_entry.pack()

        self.driver_label = tk.Label(self.frame, text="kierowca:")
        self.driver_label.pack()

        self.driver_entry = ttk.Combobox(self.frame, values=self.get_drivers())
        self.driver_entry.pack()

        self.add_vehicle_button = tk.Button(self.frame, text="Dodaj pojazd", command=self.add_vehicle_button_click)
        self.add_vehicle_button.pack()

        self.edit_vehicle_button = tk.Button(self.frame, text="Edytuj pojazd", command=self.edit_vehicle_button_click)
        self.edit_vehicle_button.pack()

        self.delete_vehicle_button = tk.Button(self.frame, text="Usuń pojazd", command=self.delete_vehicle_button_click)
        self.delete_vehicle_button.pack()

        self.back_button = tk.Button(self.frame, text="Powrót", command=self.back_button_click)
        self.back_button.pack()

    def add_vehicle_button_click(self):
        brand = self.brand_entry.get()
        model = self.model_entry.get()
        registration_date = self.registration_date_entry.get_date()
        registration_date = registration_date.strftime('%Y-%m-%d')
        license_plate_number = self.license_plate_number_entry.get()
        driver = self.driver_entry.get()
        if brand and model and registration_date and license_plate_number:
            self.vehicles_collection.insert_one({'brand': brand, 'model': model, 'registration_date': registration_date, 'license_plate_number': license_plate_number, 'driver': driver})
            self.populate_vehicles_treeview()
        else:
            print('Please fill all fields')

    def edit_vehicle_button_click(self):
        selected_items = self.vehicles_treeview.selection()
        if selected_items:
            selected_item = selected_items[0]
            selected_license_plate_number = self.vehicles_treeview.item(selected_item)['values'][3]

            brand = self.brand_entry.get()
            model = self.model_entry.get()
            registration_date = self.registration_date_entry.get_date()
            registration_date = registration_date.strftime('%Y-%m-%d')
            license_plate_number = self.license_plate_number_entry.get()
            driver = self.driver_entry.get()

            if brand and model and registration_date and license_plate_number:
                vehicle = self.vehicles_collection.find_one({'license_plate_number': selected_license_plate_number})
                print(vehicle)
                self.vehicles_collection.update_one({'license_plate_number': selected_license_plate_number}, {'$set': {'brand': brand, 'model': model, 'registration_date': registration_date, 'license_plate_number': license_plate_number, 'driver': driver}})
                self.populate_vehicles_treeview()
                print('Vehicle updated successfully.')
            else:
                print('Please fill all fields')
        else:
            print('Please select a vehicle')

    def delete_vehicle_button_click(self):
        selected_items = self.vehicles_treeview.selection()
        if selected_items:
            selected_item = selected_items[0]
            selected_brand = self.vehicles_treeview.item(selected_item)['values'][0]
            selected_model = self.vehicles_treeview.item(selected_item)['values'][1]
            selected_registration_date = self.vehicles_treeview.item(selected_item)['values'][2]
            selected_license_plate_number = self.vehicles_treeview.item(selected_item)['values'][3]
            selected_driver = self.vehicles_treeview.item(selected_item)['values'][4]

            self.vehicles_collection.delete_one({'brand': selected_brand, 'model': selected_model, 'registration_date': selected_registration_date, 'license_plate_number': selected_license_plate_number, 'driver': selected_driver})
            self.populate_vehicles_treeview()
        else:
            print('Please select a vehicle')

       
    def on_treeview_select(self, event):
        selected_items = self.vehicles_treeview.selection()
        if selected_items:
            selected_item = selected_items[0]
            selected_brand = self.vehicles_treeview.item(selected_item)['values'][0]
            selected_model = self.vehicles_treeview.item(selected_item)['values'][1]
            selected_registration_date = self.vehicles_treeview.item(selected_item)['values'][2]
            selected_license_plate_number = self.vehicles_treeview.item(selected_item)['values'][3]
            selected_driver = self.vehicles_treeview.item(selected_item)['values'][4]

            self.brand_entry.delete(0, tk.END)
            self.brand_entry.insert(0, selected_brand)
            self.model_entry.delete(0, tk.END)
            self.model_entry.insert(0, selected_model)
            self.registration_date_entry.delete(0, tk.END)
            self.registration_date_entry.insert(0, selected_registration_date)
            self.license_plate_number_entry.delete(0, tk.END)
            self.license_plate_number_entry.insert(0, selected_license_plate_number)
            self.driver_entry.delete(0, tk.END)
            self.driver_entry.insert(0, selected_driver)

            

    def populate_vehicles_treeview(self):
        for i in self.vehicles_treeview.get_children():
            self.vehicles_treeview.delete(i)
        vehicles = self.get_vehicles()  
        for vehicle in vehicles:
            self.vehicles_treeview.insert('', 'end', values=(vehicle['brand'], vehicle['model'], vehicle['registration_date'], vehicle['license_plate_number'], vehicle['driver']))

    def get_vehicles(self):
        try:
            vehicles = self.vehicles_collection.find()
            return list(vehicles)
        except Exception as e:
            print('Error getting vehicles:', str(e))
            return []
        
    def get_drivers(self):
        try:
            drivers_collection = MongoDBConnection.getInstance().get_drivers_collection()
            drivers = drivers_collection.find()
            return [driver['name'] for driver in drivers]
        except Exception as e:
            print('Error getting drivers:', str(e))
            return []


    
    def back_button_click(self):
        self.frame.destroy()
        from startingPage import StartingPage
        StartingPage(self, self.user)
            
