import tkinter as tk

class Base(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.create_widgets()
        self.master.frames = []  # Add a stack of frames

    def create_widgets(self):
        pass

    def change_window(self, frame_class, user=None):
        if self.master.current_frame is not None:
            self.master.current_frame.grid_remove()  # Hide the current frame
            self.master.frames.append(self.master.current_frame)  # Push the current frame onto the stack

        new_frame = frame_class(self.master, user)
        self.master.current_frame = new_frame
        self.master.current_frame.grid()  # Show the new frame

    def go_back(self):
        if self.master.frames:
            self.master.current_frame.grid_remove()  # Hide the current frame
            self.master.current_frame = self.master.frames.pop()  # Pop the previous frame off the stack
            self.master.current_frame.grid()  # Show the previous frame

    def logout(self):
        self.master.current_frame.grid_remove()  # Hide the current frame
        self.master.current_frame = LoginPage(self.master)
        self.master.current_frame.grid()  # Show the login page