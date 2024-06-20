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
            command = f'LED{self.index}1'
            print(f'Pulsante {self.index} premuto')
        elif self.current_color == "green":
            self.current_color = "red"
            command = f'LED{self.index}0'
            print(f'Pulsante {self.index} rilasciato')
        else:
            self.current_color = "green"
            command = f'LED{self.index}1'
            print(f'Pulsante {self.index} premuto nuovamente')
        self.itemconfig(self.circle, fill=self.current_color)
        self.send_command(command)

def update_circle_color(index, state):
    color = "green" if state == "ON" else "red"
    for widget in tk._default_root.children.values():
        if isinstance(widget, CircleButton) and widget.index == index:
            widget.itemconfig(widget.circle, fill=color)

class MainWindow(tk.Tk):
    def __init__(self, send_command):
        super().__init__()
        self.title("Applicazione Principale")
        self.geometry("400x150")

        self.circle_buttons = []
        for i in range(1, 5):
            button = CircleButton(self, i, send_command)
            button.grid(row=0, column=i - 1, padx=10, pady=10)
            self.circle_buttons.append(button)

        self.state_button = tk.Button(self, text="Richiedi Stato", command=self.request_state)
        self.state_button.grid(row=1, column=0, columnspan=4, pady=10)

    def request_state(self):
        states = [f'Pulsante {btn.index}: {"Premuto" if btn.current_color == "green" else "Non Premuto"}' for btn in self.circle_buttons]
        print("\n".join(states))
