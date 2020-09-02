# temperature & humidity sensor + website

This is one of my small school projects at campus-bb Berlin, Stadtmitte.
It runs a python program to read from the sensor and dumps it to `data.json`.
Additionally, there is a web server written in Go that reads the `data.json` and displays
it on a simple website using Go's template package.

# Documentation

## Setup

![setup](setup.jpg)

### Requirements

- Raspberry Pi 3
- 3 Pin cables
- KY-015 Kombi-Sensor Temperatur+Feuchtigkeit (from the Sensorkit by Joy-It)
- Go language installed
- Python 3 installed

## Installation

**Assuming you are doing the installing on your Pi Model 3.**
See the above picture for how you can connect the sensor pins with the Pi's pins,
so you don't need to change the GPIO pin in the `sensor.py` code.


```shell script
sudo apt install git
git clone https://github.com/robinbraemer/school-sensor-web.git
cd school-sensor-web
```

Before you can run the sensor.py you need to install Adafruit (the python library used for this sensor).
```shell script
git clone https://adafruit/Adafruit_Python_DHT.git
cd Adafruit_Python_DHT
sudo python setup.py install
```

Go back to the project directory with `cd ..`.

In order to communicate with the Pi's I2C-Bus we need to activate I2C.
```shell script
sudo nano /boot/config.txt
```
Add the following line:
`dtparam=i2c_arm=on`

Save & close nano editor with 'CTRL+X -> Y -> Return'.

Then install the additional libraries.
```shell script
sudo apt install python-smbus i2c-tools -y
```

## Let's run it!

After you did the [installation](#installation) we can run `sensor.py` and `web.go`.

Being in root directory of this project, run the sensor.
```shell script
sudo python sensor.py
```

We can additionally run the Go web server with:
```shell script
go run web.go
```

The website is reachable from http://localhost:8080.
You can the available flags with `go run web.go -h`.

For example we can serve the website on the default http port 80 with:
```shell script
sudo go run web.go -p 80
``` 
but we need run it with sudo since this is a lower port requiring more permissions.

# More

Please refer to the `web.go` and `sensor.go` for the implementation and read the code comments.