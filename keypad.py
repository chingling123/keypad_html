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

GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def gpio_callback(channel):
    global dropped
    global dropatempt
    dropped = True
    dropatempt = 0
    print "falling " + str(channel)


GPIO.add_event_detect(22, GPIO.FALLING, callback=gpio_callback, bouncetime=50)

dropped = False
dropatempt = 0

eel.init('web')

print len(mo.motors)

def check_motor():
    print(mo.motorCount)
    print("motor info " + str(mo.read_motor_info()))
    mo.start_motor()
    print("motor info " + str(mo.read_motor_info()))

    if mo.read_motor_info() == 0x01:
        mo.add_counter()
        if mo.motorCount < 5:
            check_motor()
        else:
            eel.python_alert("Motores Com Problema")
    else:
        start_motor()


def start_motor():
    global dropatempt
    print('out check motor')
    start_time = time.time()
    elapsed_time = 0

    while mo.read_motor_info() != 0X01:
        elapsed_time = time.time() - start_time
        if elapsed_time > 10:
            break
     
        print('reading... ' + str(mo.motorCount))
        mo.set_status_sensor()
        print(mo.get_actual_status())
        mo.set_status_reset()
        time.sleep(1)

    print('laps')
    mo.set_status_counter()
    print(mo.get_actual_status())

    time.sleep(0.5)
    if dropped == False and dropatempt < 1:
        dropatempt += 1
        check_motor()
    elif dropped == False and dropatempt == 1:
        mo.add_counter()
        dropatempt = 0
        check_motor()


@eel.expose
def check_cpf(cpf):
    try:
        global dropatempt
        global dropped
        print('check_cpf')
        test = cpfcnpj.validate(cpf)
        print(test)
        
        if test == True:
            dropatempt = 0
            dropped = False
            eel.python_errors(test)
            check_motor()
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
