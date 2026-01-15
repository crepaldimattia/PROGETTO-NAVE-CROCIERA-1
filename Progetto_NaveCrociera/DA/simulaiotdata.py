import json
import time
import random
import os

# Importo le funzioni che simulano il sensore
from misurazione import leggi_temperatura, leggi_umidita


# ===== LETTURA PARAMETRI DAL FILE =====
with open("configurazione/parametri.conf", "r") as file:
    parametri = json.load(file)

TEMPO = parametri["TEMPO_RILEVAZIONE"]
DECIMALI = parametri["N_DECIMALI"]
CABINE = parametri["N_CABINE"]
PONTI = parametri["N_PONTI"]


# ===== PREPARAZIONE FILE DI OUTPUT =====
# Creo la cartella se non esiste
os.makedirs("dati", exist_ok=True)

# Apro il file in append per non perdere i dati precedenti
file_dati = open("dati/iotdata.dbt", "a")


# ===== VARIABILI PER STATISTICHE =====
numero_rilevazioni = 0
somma_temperatura = 0
somma_umidita = 0

print("Simulazione avviata (CTRL+C per terminare)")


# ===== CICLO PRINCIPALE =====
try:
    while True:
        numero_rilevazioni += 1

        # Scelgo cabina e ponte casuali
        cabina = random.randint(1, CABINE)
        ponte = random.randint(1, PONTI)

        # Lettura dei dati dal sensore simulato
        temperatura = leggi_temperatura(DECIMALI)
        umidita = leggi_umidita(DECIMALI)

        # Timestamp corrente
        tempo_corrente = time.time()

        # Creazione del dato IoT
        dato = {
            "cabina": cabina,
            "ponte": ponte,
            "rilevazione": numero_rilevazioni,
            "dataeora": tempo_corrente,
            "temperatura": temperatura,
            "umidita": umidita
        }

        # Stampa a video per debug
        print(json.dumps(dato, indent=4))

        # Salvataggio su file
        file_dati.write(json.dumps(dato) + "\n")

        # Aggiorno le somme per le medie
        somma_temperatura += temperatura
        somma_umidita += umidita

        # Attesa prima della prossima rilevazione
        time.sleep(TEMPO)


# ===== GESTIONE CTRL+C =====
except KeyboardInterrupt:
    print("\nSimulazione terminata")

    media_temp = round(somma_temperatura / numero_rilevazioni, DECIMALI)
    media_umid = round(somma_umidita / numero_rilevazioni, DECIMALI)

    print("Rilevazioni totali:", numero_rilevazioni)
    print("Temperatura media:", media_temp, "°C")
    print("Umidità media:", media_umid, "%")

    file_dati.close()
