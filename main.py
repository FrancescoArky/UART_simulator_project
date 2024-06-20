import tkinter as tk
import threading
import serial
import time
from gui import MainWindow, update_circle_color

port_name_send = 'COM1'  # Porta seriale per inviare dati
port_name_receive = 'COM2'  # Porta seriale per ricevere dati
baud_rate = 9600  # Baud rate

messages_sent = []
messages_received = []

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
            global messages_sent
            messages_sent.append(command)
        except serial.SerialException as e:
            print(f'Errore durante l\'invio del comando sulla porta {port_name_send}: {e}')

def receive_data(ser_receive, circle_buttons):
    global messages_received
    if ser_receive:
        try:
            while True:
                if ser_receive.in_waiting > 0:
                    data = ser_receive.readline().decode().strip()
                    messages_received.append(data)

                    if data.startswith("LED"):
                        led_number = data[3]
                        led_state = data[5]
                        update_circle_color(int(led_number), "ON" if led_state == '1' else "OFF", circle_buttons)
        except serial.SerialException as e:
            print(f'Errore durante la ricezione dei dati sulla porta {port_name_receive}: {e}')

def request_state(circle_buttons):
    states = []
    for button in circle_buttons:
        state = "ON" if button.current_color == "green" else "OFF"
        states.append(f'LED{button.index} {state}')
    print(" ".join(states))

def print_messages_periodically():
    global messages_sent, messages_received
    while True:
        time.sleep(1)
        if messages_sent:
            for message in messages_sent:
                print(f"Messaggio inviato: {message}")
            messages_sent = []
        else:
            print("Comunicazione aperta")
        
        if messages_received:
            for message in messages_received:
                print(f"Dato ricevuto da COM2: {message}")
            messages_received = []

def main():
    ser_send, ser_receive = open_serial_ports()

    root = tk.Tk()
    root.title("Simulatore Seriale")

    main_window = MainWindow(root, lambda command: send_command(ser_send, command), lambda: request_state(main_window.circle_buttons))
    main_window.pack(expand=True, fill=tk.BOTH)

    receive_thread = threading.Thread(target=receive_data, args=(ser_receive, main_window.circle_buttons))
    receive_thread.daemon = True
    receive_thread.start()

    print_thread = threading.Thread(target=print_messages_periodically)
    print_thread.daemon = True
    print_thread.start()

    root.mainloop()

if __name__ == "__main__":
    main()
