#!/usr/bin/python

#
# !!! PLEASE READ !!!
#
# This code sample is retrieved from the pdf documentation Sensorkit 40x by Joy-It
# and modified in the button while loop to dump the sensor data to the data.json file.
#
# !!! PLEASE READ !!!
#

import Adafruit_DHT
# coding=utf-8
# Benoetigte Module werden importiert und eingerichtet
import RPi.GPIO as GPIO
import time

# Die Pause von zwei Sekunden zwischen den Messungen wird hier eingestellt
sleeptime = 2
# Sensor should be set to Adafruit_DHT.DHT11,
# Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
DHTSensor = Adafruit_DHT.DHT11
# Hier kann der Pin deklariert werden, an dem das Sensormodul angeschlossen ist
# Hier kann der Pin deklariert werden, an dem das Sensormodul angeschlossen ist
GPIO_Pin = 23
print('KY-015 Sensortest - Temperatur und Luftfeuchtigkeit')

import json

# dump writes sensor data to the file so web.go can read it.
def dump(data):
    with open('data.json', 'w') as outfile:
        json.dump(data, outfile)

try:
    while (1):
        # Messung wird gestartet und das Ergebnis in die entsprechenden Variablen geschrieben
        Luftfeuchte, Temperatur = Adafruit_DHT.read_retry(DHTSensor, GPIO_Pin)
        print("-----------------------------------------------------------------")
        if Luftfeuchte is not None and Temperatur is not None:
            temp = '{0:0.1f}°C'.format(Temperatur)
            hum = Luftfeuchte  # '{1:0.1f}%'.format(Luftfeuchte)

            # Das gemessene Ergebnis wird in der Konsole ausgegeben
            print('Temperatur = ' + temp + ' | rel. Luftfeuchtigkeit = ' + str(hum))
            data = {
                'Temperatur': temp,
                'Luftfeuchtigkeit': hum
            }
            dump(data)
        # Da der Raspberry Pi aufgrund des Linux-Betriebsystems für Echtzeitanwendungen benachteiligt ist,
        # kann es sein, dass aufgrund von Timing Problemen die Kommunikation scheitern kann.
        # In dem Falle wird eine Fehlermeldung ausgegeben - ein Ergebnis sollte beim nächsten Versuch vorliegen
        else:
            print('Fehler beim Auslesen - Bitte warten auf nächsten Versuch!')
            print("-----------------------------------------------------------------")
            print("")
            time.sleep(sleeptime)
# Aufraeumarbeiten nachdem das Programm beendet wurde
except KeyboardInterrupt:
    GPIO.cleanup()
