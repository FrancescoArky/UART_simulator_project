import tkinter as tk

class CircleButton(tk.Canvas):
    def __init__(self, master, index, send_command):
        """
        Costruttore per il pulsante circolare.

        Args:
            master (tk.Tk or tk.Frame): Il genitore del widget.
            index (int): Numero identificativo del pulsante (da 1 a 4).
            send_command (function): Funzione per inviare comandi al dispositivo esterno.
        """
        super().__init__(master, width=50, height=50, highlightthickness=0)
        self.index = index  # Numero identificativo del pulsante (da 1 a 4)
        self.send_command = send_command
        self.current_color = "gray"
        self.circle = self.create_oval(10, 10, 40, 40, outline="black", width=2, fill=self.current_color)
        self.number = self.create_text(25, 25, text=str(index), font=("Arial", 12))
        self.grid(row=0, column=index - 1, padx=10, pady=10)
        self.bind("<Button-1>", self.on_click)

    def on_click(self, event):
        """
        Gestisce l'evento di click sul pulsante.

        Args:
            event (tk.Event): Evento di click del mouse.
        """
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

# Funzione per aggiornare il colore dei cerchi dall'esterno
def update_circle_color(index, state):
    """
    Aggiorna il colore del cerchio del pulsante indicato.

    Args:
        index (int): Numero identificativo del pulsante.
        state (str): Stato del LED ("ON" o "OFF").
    """
    color = "green" if state == "ON" else "red"
    for widget in tk._default_root.children.values():
        if isinstance(widget, CircleButton) and widget.index == index:
            widget.itemconfig(widget.circle, fill=color)

# Finestra principale
class MainWindow(tk.Tk):
    def __init__(self, send_command):
        """
        Costruttore per la finestra principale dell'applicazione.

        Args:
            send_command (function): Funzione per inviare comandi al dispositivo esterno.
        """
        super().__init__()

        # Titolo e dimensione finestra
        self.title("Applicazione Principale")
        self.geometry("400x100")

        # Pulsanti numerati
        for i in range(1, 5):
            button = CircleButton(self, i, send_command)
