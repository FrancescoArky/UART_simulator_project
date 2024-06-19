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
        # Apertura della porta seriale per l'invio
        ser_send = serial.Serial(port_name_send, baud_rate, timeout=1) # Inizializzazione della porta seriale per invio dei dati
        print(f'Porta seriale {port_name_send} aperta per invio')
    except serial.SerialException as e:
        print(f'Errore durante l\'apertura della porta seriale {port_name_send}: {e}')
        exit(1)  # Esce dal programma con codice di errore 1 nel caso in cui la porta di invio dati COM1 non sia disponibile

    try:
        # Apertura della porta seriale per la ricezione
        ser_receive = serial.Serial(port_name_receive, baud_rate, timeout=1)
        print(f'Porta seriale {port_name_receive} aperta per ricezione')
    except serial.SerialException as e:
        print(f'Errore durante l\'apertura della porta seriale {port_name_receive}: {e}')
        if ser_send:
            ser_send.close()  # Chiude la porta seriale per l'invio se è stata aperta con successo in caso di malfunzionamento di quella di ricezione
        exit(1)  # Esce dal programma con codice di errore 1 nel caso in cui la porta di ricezione dati COM2 non sia disponibile

    return ser_send, ser_receive

def send_command(ser_send, command):
    """
    Invia un comando attraverso la porta seriale specificata, si verificherà un raise di serial.SerialException in caso di errore durante l'invio del comando.
    """
    if ser_send:
        try:
            # Invio del comando
            ser_send.write(command.encode())
        except serial.SerialException as e:
            print(f'Errore durante l\'invio del comando sulla porta {port_name_send}: {e}')

def receive_data(ser_receive):
    """
    Gestisce la ricezione dei dati attraverso la porta seriale specificata.
    """
    if ser_receive:
        try:
            # Loop per ricevere i dati
            while True:
                if ser_receive.in_waiting > 0:
                    data = ser_receive.readline().decode()
                    print(f'Dati ricevuti da {port_name_receive}: LED{data[3]} {data[4]}')

                    # Gestione del messaggio ricevuto
                    if data.startswith("LED"):
                        led_number = data[3]  # Numero del LED
                        led_state = data[4]   # Stato del LED
                        update_circle_color(int(led_number), "ON" if led_state == '1' else "OFF")
        except serial.SerialException as e:
            print(f'Errore durante la ricezione dei dati sulla porta {port_name_receive}: {e}')

if __name__ == "__main__":
    # Apertura delle porte seriali
    ser_send, ser_receive = open_serial_ports()

    # Avvio della comunicazione seriale in un thread separato per la ricezione dei dati
    receive_thread = threading.Thread(target=receive_data, args=(ser_receive,))
    receive_thread.daemon = True
    receive_thread.start()

    # Creazione e avvio della finestra principale
    app = MainWindow(lambda command: send_command(ser_send, command))
    app.mainloop()
