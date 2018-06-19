import atexit
import RPi.GPIO as GPIO
import argparse
import eel
import json
import time
from motors import Motors
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

mo = Motors([0x11,0x12,0x13,0x14,0x15])

eel.init('web')

def start_motor():
    mo.start_motor()

    start_time = time.time()
    elapsed_time = 0

    while mo.read_motor_info() != 0X01:
        elapsed_time = time.time() - start_time
        if elapsed_time > 10:
            break
     
        print 'reading... ' + str(mo.motorCount)
        mo.set_status_sensor()
        print  mo.get_actual_status()
        mo.set_status_reset()
        time.sleep(1)

    print 'laps'
    mo.set_status_counter()
    print mo.get_actual_status()


@eel.expose
def check_cpf(cpf):
    try:
        test = cpfcnpj.validate(cpf)
        print(test)
        eel.python_errors(test)
        if test == True:
            start_motor()
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
