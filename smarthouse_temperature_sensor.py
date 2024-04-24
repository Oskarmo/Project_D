import logging
import threading
import time
import math
import requests

from messaging import SensorMeasurement
import common


class Sensor:

    def __init__(self, did):
        self.did = did
        self.measurement = SensorMeasurement('0.0')

    def simulator(self):

        logging.info(f"Sensor {self.did} starting")

        while True:

            temp = round(math.sin(time.time() / 10) * common.TEMP_RANGE, 1)

            logging.info(f"Sensor {self.did}: {temp}")
            self.measurement.set_temperature(str(temp))

            time.sleep(common.TEMPERATURE_SENSOR_SIMULATOR_SLEEP_TIME)

    def client(self):

        logging.info(f"Sensor Client {self.did} starting")
        url = f"{common.BASE_URL}sensor/{self.did}/current"
        #sender kontinuelrig temperatur data
        while True:
            #Forbereder data med current temp, unit og tidsstempel
            payload = {'value': self.measurement.get_temperature(),'unit': '°C',
                       'timestamp': self.measurement.timestamp}
            #forsøke å sende data til server
            try:
                response = requests.post(url, json=payload) #post request til sky
                response.raise_for_status() #Error hvis noe galt med HTTP
                logging.info(f"Successfully sent temperature {self.measurement.get_temperature()}°C for sensor {self.did}")
            except requests.RequestException as e: #skriver ut error melding om mislykket
                logging.error(f"Error sending data for sensor {self.did}: {e}")
            time.sleep(common.TEMPERATURE_SENSOR_CLIENT_SLEEP_TIME) #Legger inn intervall tiden fra common


    def run(self):
        #Egen thread for simulator og client
        simulator_thread = threading.Thread(target=self.simulator)
        client_thread = threading.Thread(target=self.client)
        #Starter begge threads
        simulator_thread.start()
        client_thread.start()
        #Lar begge threads fullføre, før prosess fortsetter
        simulator_thread.join()
        client_thread.join()


