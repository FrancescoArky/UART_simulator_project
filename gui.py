import tkinter as tk

class CircleButton(tk.Canvas):
    def __init__(self, master, index, send_command, **kwargs):
        super().__init__(master, **kwargs)
        self.index = index
        self.current_color = "red"  # Default color is red
        self.bind("<Button-1>", self.toggle_color)
        self.create_oval(5, 5, 45, 45, outline="black", fill=self.current_color)  # Adjusted size for button
        self.send_command = send_command

    def toggle_color(self, event):
        self.current_color = "green" if self.current_color == "red" else "red"
        self.itemconfig(tk.ALL, fill=self.current_color)
        # Invia il comando corrispondente quando il pulsante viene premuto
        command = f"LED{self.index} {'1' if self.current_color == 'green' else '0'}"
        self.send_command(command)

def update_circle_color(index, state, circle_buttons):
    circle_button = circle_buttons[index]
    circle_button.current_color = "green" if state == "ON" else "red"
    circle_button.itemconfig(tk.ALL, fill=circle_button.current_color)

class MainWindow(tk.Frame):
    def __init__(self, master, send_command, request_state, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.send_command = send_command
        self.request_state = request_state

        self.circle_buttons = []
        for i in range(4):
            circle_button = CircleButton(self, index=i, send_command=self.send_command, width=50, height=50)  # Adjusted size for button
            circle_button.grid(row=0, column=i, padx=10, pady=10)
            self.circle_buttons.append(circle_button)

        self.state_button = tk.Button(self, text="Stato", command=self.request_state)
        self.state_button.grid(row=1, column=0, columnspan=4, pady=10)

        self.quit_button = tk.Button(self, text="Esci", command=self.master.quit)
        self.quit_button.grid(row=2, column=0, columnspan=4, pady=10)
