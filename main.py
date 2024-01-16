#aplikacja wymaga python3, oraz tkinter
#python3 -m pip install tk
#python3 -m pip install pymongo

import tkinter as tk
from loginPage import LoginPage

def main(): 
    root = tk.Tk()
    app = LoginPage(root)
    root.mainloop()

if __name__ == '__main__':
    main()