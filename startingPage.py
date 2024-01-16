from base import Base
import tkinter as tk

class StartingPage(Base):
    def __init__(self, master, user):
        super().__init__(master)

        if self.check_admin_privileges(user):
            self.manageUsersButton = tk.Button(self.frame, text='Zarządzaj użytkownikami', width=25, command=self.manage_users)
            self.manageUsersButton.pack()

        self.manageVehiclesButton = tk.Button(self.frame, text='Zarządzaj pojazdami', width=25, command=self.manage_vehicles)
        self.manageVehiclesButton.pack()
        
        self.manageDriversButton = tk.Button(self.frame, text='Zarządzaj kierowcami', width=25, command=self.manage_drivers)
        self.manageDriversButton.pack()

        self.manageRoutesButton = tk.Button(self.frame, text='Zarządzaj trasami', width=25, command=self.manage_routes)
        self.manageRoutesButton.pack()

        self.quitButton = tk.Button(self.frame, text='Wyloguj', width=25, command=self.logout)
        self.quitButton.pack()

    def check_admin_privileges(self, user):
        return user.get('role') == 'admin'

    def manage_users(self):
        from manageUsersPage import ManageUsersPage
        self.change_window(StartingPage, user)

    def manage_vehicles(self):
        print("Button 'zarządzaj pojazdami' clicked")
    
    def manage_drivers(self):
        print("Button 'zarządzaj kierowcami' clicked")

    def manage_routes(self):
        print("Button 'zarządzaj trasami' clicked")

        

    def logout(self):
        from loginPage import LoginPage
        self.logout(LoginPage)