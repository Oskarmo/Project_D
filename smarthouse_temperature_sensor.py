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
        while True:
            payload = {'value': self.measurement.get_temperature(),'unit': '°C',
                       'timestamp': self.measurement.timestamp}
            try:
                response = requests.post(url, json=payload) #post request til sky
                response.raise_for_status()
                logging.info(f"Successfully sent temperature {self.measurement.get_temperature()}°C for sensor {self.did}")
            except requests.RequestException as e: #skriver ut error melding om mislykket
                logging.error(f"Error sending data for sensor {self.did}: {e}")
            time.sleep(common.TEMPERATURE_SENSOR_CLIENT_SLEEP_TIME) #Legger inn intervall tiden fra common


    def run(self):

        simulator_thread = threading.Thread(target=self.simulator)
        client_thread = threading.Thread(target=self.client)

        simulator_thread.start()
        client_thread.start()

        simulator_thread.join()
        client_thread.join()


