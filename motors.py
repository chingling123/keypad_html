from smbus2 import SMBus

class Motors:
    
    def __init__(self, motorsList):
        self.motors = motorsList
        self.motorCount = 0
        self.bus = SMBus(1)
        
    def start_motor(self):
        if self.motorCount < self.motors.count:
           self.bus.write_byte(self.motors[self.motorCount], 0x01)
            
    def add_counter(self):
        if self.motorCount < len(self.motors)-1:
            self.motorCount += 1
        else:
            self.motorCount = 0

    def read_motor_info(self):
        b = self.bus.read_byte(self.motors[self.motorCount])
        return b

    def set_status_counter(self):
        self.bus.write_byte(self.motors[self.motorCount], 0x02)

    def set_status_sensor(self):
        self.bus.write_byte(self.motors[self.motorCount], 0x03)

    def set_status_reset(self):
        self.bus.write_byte(self.motors[self.motorCount], 0x09)    

    def get_actual_status(self):
        b = self.bus.read_byte(self.motors[self.motorCount])
        return b
    