import atexit
import RPi.GPIO as GPIO
import argparse
import eel
import json
from pycpfcnpj import cpfcnpj
from hx711 import HX711

def cleanup():
    GPIO.cleanup()

atexit.register(cleanup)

hx = HX711(5,6)
hx.set_reading_format("LSB", "MSB")

parser = argparse.ArgumentParser(description='BizSys System', usage='%(progs)s [options]')
parser.add_argument('--startup', metavar='Startup Type', nargs='?', default='N', help='[N]ormal startup, [C]alibration Measure')

args = parser.parse_args()

eel.init('web')

@eel.expose
def check_cpf(cpf):
    try:
        print(cpfcnpj.validate(cpf))
        eel.python_errors(cpfcnpj.validate(cpf))
    except:
        eel.python_errors('Exception')

def tare():
    print("tare")
    hx.reset()
    hx.tare()

@eel.expose
def getWeight():
    weight = hx.get_weight(5)
    print(weight)
    eel.get_weight(str(weight).replace("[","").replace("]",""))

@eel.expose
def set_config_measuring():
    file = open("config.cfg","r")
    data = json.loads(file.read())
    print(data["measuring"])
    hx.set_reference_unit(data["measuring"])
    tare()

@eel.expose
def write_config_measuring(w):
    print(w)
    file = open("config.cfg","r")
    data = json.loads(file.read())
    data["measuring"] = w
    print(data)
    file.close()
    with open("config.cfg", "w") as outfile:
        json.dump(data, outfile)

set_config_measuring()

if args.startup == 'N':
    eel.start('keypad.html')
elif args.startup == 'C':
    eel.start('calibmeasure.html')
