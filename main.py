import tkinter as tk
import threading
import serial
import time
from gui import MainWindow

port_name_send = 'COM1'  # Porta seriale per inviare dati
port_name_receive = 'COM2'  # Porta seriale per ricevere dati
baud_rate = 9600  # Baud rate

def open_serial_ports():
    try:
        ser_send = serial.Serial(port_name_send, baud_rate, timeout=1)
        print(f'Porta seriale {port_name_send} aperta per invio')
    except serial.SerialException as e:
        print(f'Errore durante l\'apertura della porta seriale {port_name_send}: {e}')
        exit(1)

    try:
        ser_receive = serial.Serial(port_name_receive, baud_rate, timeout=1)
        print(f'Porta seriale {port_name_receive} aperta per ricezione')
    except serial.SerialException as e:
        print(f'Errore durante l\'apertura della porta seriale {port_name_receive}: {e}')
        if ser_send:
            ser_send.close()
        exit(1)

    return ser_send, ser_receive

def send_command(ser_send, command):
    if ser_send:
        try:
            ser_send.write(command.encode())
            print(f"Messaggio inviato: {command}")  # Stampa direttamente il messaggio inviato
        except serial.SerialException as e:
            print(f'Errore durante l\'invio del comando sulla porta {port_name_send}: {e}')

def print_messages_periodically():
    while True:
        time.sleep(1)  # Attendi un secondo
        print("Comunicazione aperta")

def request_state(circle_buttons):
    print("LED states:")
    for button in circle_buttons:
        state = "ON" if button.current_color == "green" else "OFF"
        print(f'LED{button.index} {state}')


def main():
    ser_send, _ = open_serial_ports()  # Non è necessario ricevere dati in questo esempio

    root = tk.Tk()
    root.title("Simulatore Seriale")

    main_window = MainWindow(root, lambda command: send_command(ser_send, command), lambda: request_state(main_window.circle_buttons))
    main_window.pack(expand=True, fill=tk.BOTH)

    print_thread = threading.Thread(target=print_messages_periodically)
    print_thread.daemon = True
    print_thread.start()

    root.mainloop()


if __name__ == "__main__":
    main()