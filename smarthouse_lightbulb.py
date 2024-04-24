import logging
import threading
import time
import requests

from messaging import ActuatorState
import common


class Actuator:

    def __init__(self, did):
        self.did = did
        self.state = ActuatorState('False')

    def simulator(self):

        logging.info(f"Actuator {self.did} starting")

        while True:

            logging.info(f"Actuator {self.did}: {self.state.state}")

            time.sleep(common.LIGHTBULB_SIMULATOR_SLEEP_TIME)

    def client(self):

        logging.info(f"Actuator Client {self.did} starting")

        url = f"http://127.0.0.1:8000/smarthouse/actuator/{self.did}/current" #url til skytjeneste
        while True:
            try:
                response = requests.get(url) #get request til sky
                response.raise_for_status()
                data = response.json()
                self.state = ActuatorState(data['state'])
                logging.info (f"Actuator {self.did} updated state to: {self.state}")
            except requests.RequestException as e: #skriver ut error melding om mislykket
                logging.error(f"Error updating actuator {self.did} state: {e}")
            time.sleep(common.LIGHTBULB_CLIENT_SLEEP_TIME)


        logging.info(f"Client {self.did} finishing")


    def run(self):

        simulator_thread = threading.Thread(target=self.simulator)
        client_thread = threading.Thread(target=self.client)

        simulator_thread.start()
        client_thread.start()

        simulator_thread.join()
        client_thread.join()



