import tkinter as tk

class CircleButton(tk.Canvas):

    """
    Initialization of the CircleButton class. At the beginning the standard color is red, and then it changes to green if pressed.
    """

    def __init__(self, master, index, send_command, **kwargs):
        super().__init__(master, **kwargs)
        self.index = index
        self.current_color = "red"
        self.bind("<Button-1>", self.toggle_color)
        self.create_oval(5, 5, 45, 45, outline="black", fill=self.current_color)
        self.send_command = send_command

    """
    Function responsible for the color change of the buttons each time they are pressed.
    """

    def toggle_color(self, event):
        self.current_color = "green" if self.current_color == "red" else "red"
        self.itemconfig(tk.ALL, fill=self.current_color)
        command = f"LED{self.index} {'1' if self.current_color == 'green' else '0'}"
        self.send_command(command)

class MainWindow(tk.Frame):
    
    """
    Initialization of the main window
    """

    def __init__(self, master, send_command, request_state, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.send_command = send_command
        self.request_state = request_state

        self.circle_buttons = [] #replication of the button class for 4 times within the main window
        for i in range(4):
            circle_button = CircleButton(self, index=i, send_command=self.send_command, width=50, height=50)
            circle_button.grid(row=0, column=i, padx=10, pady=10)
            self.circle_buttons.append(circle_button)

        self.state_button = tk.Button(self, text="LED Status", command=self.request_state) #creation of the LED Status button
        self.state_button.grid(row=1, column=0, columnspan=4, pady=10)

        self.quit_button = tk.Button(self, text="Exit", command=self.master.quit) #creation of the Exit button, it makes it possible to quit the program
        self.quit_button.grid(row=2, column=0, columnspan=4, pady=10)
