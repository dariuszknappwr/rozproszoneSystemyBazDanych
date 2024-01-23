from base import Base
import tkinter as tk

class StartingPage(Base):
    def __init__(self, master, user):
        super().__init__(master)
        self.user = user

        self.frame = tk.Frame(master)
        self.frame.grid()

        if self.check_admin_privileges(user):
            self.manageUsersButton = tk.Button(self.frame, text='Zarządzaj użytkownikami', width=25, command=self.manage_users)
            self.manageUsersButton.pack()

        self.manageVehiclesButton = tk.Button(self.frame, text='Zarządzaj pojazdami', width=25, command=self.manage_vehicles)
        self.manageVehiclesButton.pack()
        
        self.manageDriversButton = tk.Button(self.frame, text='Zarządzaj kierowcami', width=25, command=self.manage_drivers)
        self.manageDriversButton.pack()

        #self.manageDriversButton = tk.Button(self.frame, text='Przypisz kierowcę do pojazdu', width=25, command=self.manage_drivers_vehicles_connection)
        #self.manageDriversButton.pack()

        self.manageRoutesButton = tk.Button(self.frame, text='Zarządzaj trasami', width=25, command=self.manage_routes)
        self.manageRoutesButton.pack()

        self.quitButton = tk.Button(self.frame, text='Wyloguj', width=25, command=self.logout)
        self.quitButton.pack()

    def check_admin_privileges(self, user):
        return user.get('role') == 'admin'

    def manage_users(self):
        self.frame.destroy()
        from manageUsersPage import ManageUsersPage
        ManageUsersPage(self, self.user)

    def manage_vehicles(self):
        self.frame.destroy()
        from manageVehiclesPage import ManageVehiclesPage
        ManageVehiclesPage(self, self.user)
    
    def manage_drivers(self):
        self.frame.destroy()
        from manageDriversPage import ManageDriversPage
        ManageDriversPage(self, self.user)

    def manage_drivers_vehicles_connection(self):
        self.frame.destroy()
        from manageDriverVehicleConnectionPage import ManageDriverVehicleConnectionPage
        ManageDriverVehicleConnectionPage(self, self.user)

    def manage_routes(self):
        self.frame.destroy()
        from manageRoutesPage import ManageRoutesPage
        ManageRoutesPage(self, self.user)

    def logout(self):
        from loginPage import LoginPage
        self.frame.destroy()
        LoginPage(None)