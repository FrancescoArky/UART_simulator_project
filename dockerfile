# Usa l'immagine ufficiale di Python 3.11 come base
FROM python:3.11

# Imposta il working directory all'interno del container
WORKDIR /simulatore

# Copia i file requirements.txt e i file Python (main.py e gui.py) nella directory /app del container
COPY requirements.txt .
COPY main.py .
COPY gui.py .

# Installa le dipendenze specificate nel requirements.txt
RUN pip install -r requirements.txt

# Comando di default per eseguire il programma quando il container viene avviato
CMD ["python", "main.py"]
