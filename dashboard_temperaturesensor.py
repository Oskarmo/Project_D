import tkinter as tk
from tkinter import ttk

import logging
import requests

from messaging import SensorMeasurement
import common


def refresh_btn_cmd(temp_widget, did):

    logging.info("Temperature refresh")

    # TODO: START
    # send request to cloud service to obtain current temperature

    #definerer URL til skytjeneste
    url = f"http://127.0.0.1:8000/smarthouse/sensor/{did}/current"

    #Sender GET request til skytjeneste
    try:
        response = requests.get(url)
        response.raise_for_status()
        current_temperature = response.json()['value']  # Får den faktiske temperaturen fra skytjenesten
        logging.info(f"Temperature fetched successfully: {current_temperature}")
    except requests.RequestException as e:
        logging.error(f"Failed to fetch temperature: {str(e)}")
        current_temperature = "Error"

        # Oppdater tekstfeltet i brukergrensesnittet med den hentede temperaturen
    temp_widget['state'] = 'normal'  # Tillater endring av tekst
    temp_widget.delete(1.0, 'end')  # Fjerner eksisterende tekst
    temp_widget.insert(1.0, current_temperature)  # Setter inn den nye temperaturen
    temp_widget['state'] = 'disabled'  # Gjør tekstfeltet skrivebeskyttet igjen


def init_temperature_sensor(container, did):

    ts_lf = ttk.LabelFrame(container, text=f'Temperature sensor [{did}]')

    ts_lf.grid(column=0, row=1, padx=20, pady=20, sticky=tk.W)

    temp = tk.Text(ts_lf, height=1, width=10)
    temp.insert(1.0, 'None')
    temp['state'] = 'disabled'

    temp.grid(column=0, row=0, padx=20, pady=20)

    refresh_button = ttk.Button(ts_lf, text='Refresh',
                                command=lambda: refresh_btn_cmd(temp, did))

    refresh_button.grid(column=1, row=0, padx=20, pady=20)
