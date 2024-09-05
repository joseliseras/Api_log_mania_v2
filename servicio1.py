#Servicio1
import requests
import time
import datetime 
import random

URL = 'http://localhost:5001/logs'
TOKEN = 'Bearer token_servicio1'

def generar_log():
    niveles = ['INFO', 'ERROR', 'DEBUG']
    log = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        'service_name' : 'Servicio1',
        'log_level' : random.choice(niveles),
        'message' : 'Este es un log del Servicio 1'
    }
    return log

def enviar_log():
    while True:
        log = generar_log()
        response = requests.post(URL, json=log, headers={'Authorization' : TOKEN})
        print(f'Enviado log: {log}, Respuesta: {response.status_code}')
        time.sleep(5)

if __name__ == '__main__':
    enviar_log()
    