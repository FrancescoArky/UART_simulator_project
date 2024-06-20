import tkinter as tk
import threading
import serial
import time
from gui import MainWindow

port_name_send = 'COM1'  # Serial door for the data sending
port_name_receive = 'COM2'  # Serial door for the data receiving
baud_rate = 9600  # Baud rate

def open_serial_ports():

    """
    Such function is responsible for opening the two communication doors for the sending and receiving procedures
    """

    try:
        ser_send = serial.Serial(port_name_send, baud_rate, timeout=1)
        print(f'Serial door {port_name_send} open for message sendings')
    except serial.SerialException as e:
        print(f'Error during the opening of the serial door {port_name_send}: {e}')
        exit(1)

    try:
        ser_receive = serial.Serial(port_name_receive, baud_rate, timeout=1)
        print(f'Serial door {port_name_receive} open for message receiving')
    except serial.SerialException as e:
        print(f'Error during the opening of the serial door {port_name_receive}: {e}')
        if ser_send:
            ser_send.close()
        exit(1)

    return ser_send, ser_receive

def send_command(ser_send, command):
    """
    In case a message is sent then this function will print said message
    """
    if ser_send:
        try:
            ser_send.write(command.encode())
            print(f"Message sent: {command}")
        except serial.SerialException as e:
            print(f'Error during the sending of the command on the door {port_name_send}: {e}')

def print_messages_periodically():

    """
    In case there are no messages sent this function will print a message periodically to show that the communication is still active
    """

    while True:
        time.sleep(1)
        print("Communication open")

def request_state(circle_buttons):
    print("LED states:")
    for button in circle_buttons:
        state = "ON" if button.current_color == "green" else "OFF"
        print(f'LED{button.index} {state}')


def main():
    ser_send, ser_receive = open_serial_ports()

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