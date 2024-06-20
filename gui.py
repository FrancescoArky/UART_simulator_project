import tkinter as tk

class CircleButton(tk.Canvas):
    def __init__(self, master, index, send_command):
        super().__init__(master, width=50, height=50, highlightthickness=0)
        self.index = index
        self.send_command = send_command
        self.current_color = "gray"
        self.circle = self.create_oval(10, 10, 40, 40, outline="black", width=2, fill=self.current_color)
        self.number = self.create_text(25, 25, text=str(index), font=("Arial", 12))
        self.grid(row=0, column=index - 1, padx=10, pady=10)
        self.bind("<Button-1>", self.on_click)

    def on_click(self, event):
        if self.current_color == "gray":
            self.current_color = "green"
            command = f'LED{self.index} 1'
            print(f'Pulsante {self.index} premuto')
        elif self.current_color == "green":
            self.current_color = "red"
            command = f'LED{self.index} 0'
            print(f'Pulsante {self.index} rilasciato')
        else:
            self.current_color = "green"
            command = f'LED{self.index} 1'
            print(f'Pulsante {self.index} premuto nuovamente')
        self.itemconfig(self.circle, fill=self.current_color)
        self.send_command(command)

def update_circle_color(index, state, circle_buttons):
    color = "green" if state == "ON" else "red"
    for button in circle_buttons:
        if button.index == index:
            button.itemconfig(button.circle, fill=color)

class StateButton(tk.Button):
    def __init__(self, master, request_state):
        super().__init__(master, text="Richiedi Stato", command=request_state)
        self.grid(row=1, column=0, columnspan=4, pady=10)

class MainWindow(tk.Tk):
    def __init__(self, send_command, request_state):
        super().__init__()

        self.title("Applicazione Principale")
        self.geometry("400x150")

        self.circle_buttons = []
        for i in range(1, 5):
            button = CircleButton(self, i, send_command)
            self.circle_buttons.append(button)

        self.state_button = StateButton(self, request_state)
