import serial
import threading
from gui import MainWindow, update_circle_color

port_name_send = 'COM1'  # Porta seriale per inviare dati
port_name_receive = 'COM2'  # Porta seriale per ricevere dati
baud_rate = 9600  # Baud rate

def open_serial_ports():
    """
    Apre le porte seriali per l'invio e la ricezione dei dati.
    """
    try:
        ser_send = serial.Serial(port_name_send, baud_rate, timeout=1)
        ser_send.flush()  # Flush della porta seriale per l'invio
        print(f'Porta seriale {port_name_send} aperta per invio')
    except serial.SerialException as e:
        print(f'Errore durante l\'apertura della porta seriale {port_name_send}: {e}')
        exit(1)

    try:
        ser_receive = serial.Serial(port_name_receive, baud_rate, timeout=1)
        ser_receive.flush()  # Flush della porta seriale per la ricezione
        print(f'Porta seriale {port_name_receive} aperta per ricezione')
    except serial.SerialException as e:
        print(f'Errore durante l\'apertura della porta seriale {port_name_receive}: {e}')
        if ser_send:
            ser_send.close()
        exit(1)

    return ser_send, ser_receive

def send_command(ser_send, command):
    """
    Invia un comando attraverso la porta seriale specificata.
    """
    if ser_send:
        try:
            ser_send.write(command.encode())
            ser_send.flush()  # Flush per garantire che i dati siano inviati immediatamente
            print(f'Comando inviato: {command}')
        except serial.SerialException as e:
            print(f'Errore durante l\'invio del comando sulla porta {port_name_send}: {e}')

def receive_data(ser_receive):
    """
    Gestisce la ricezione dei dati attraverso la porta seriale specificata.
    """
    if ser_receive:
        try:
            while True:
                if ser_receive.in_waiting > 0:
                    data = ser_receive.readline().decode().strip()
                    print(f'Dati ricevuti da {port_name_receive}: LED{data[3]} {data[4]}')

                    if data.startswith("LED"):
                        led_number = int(data[3])
                        led_state = int(data[4])
                        update_circle_color(led_number, "ON" if led_state == 1 else "OFF")
        except serial.SerialException as e:
            print(f'Errore durante la ricezione dei dati sulla porta {port_name_receive}: {e}')

if __name__ == "__main__":
    ser_send, ser_receive = open_serial_ports()

    receive_thread = threading.Thread(target=receive_data, args=(ser_receive,))
    receive_thread.daemon = True
    receive_thread.start()

    app = MainWindow(lambda command: send_command(ser_send, command))
    app.mainloop()
