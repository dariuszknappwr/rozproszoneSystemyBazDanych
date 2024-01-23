#aplikacja wymaga python3, oraz tkinter
# apt-get install python3-tk  lub  python3 -m pip install tk, a jak nie działa to dać jeszcze apt-get update i apt-get install -y tk (któreś zadziała)
#python3 -m pip install pymongo

import tkinter as tk
from loginPage import LoginPage

def main(): 
    root = tk.Tk()
    app = LoginPage(root)
    root.mainloop()

if __name__ == '__main__':
    main()