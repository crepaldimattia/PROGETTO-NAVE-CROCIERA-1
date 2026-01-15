
import random   # Generazione numeri casuali

#
# Funzioni
#
def leggi_temperatura(N):
    TEMP = round(random.uniform(10,40), N)
    return TEMP
# Simulazione sensore umidità, da 20 a 90 gradi
# cifre decimali pari a N
def leggi_umidita(N):
    UMID = round(random.uniform(20,90), N)
    return UMID
