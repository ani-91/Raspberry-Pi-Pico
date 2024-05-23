import machine
import time

class Pressure_Sensor:
    def __init__(self, sda_pin=12, scl_pin=13, port=0, speed=100000, address=0x6D):
        self.address = address
        self.sda_pin = machine.Pin(sda_pin)
        self.scl_pin = machine.Pin(scl_pin)
        self.i2c = machine.I2C(port, sda=self.sda_pin, scl=self.scl_pin, freq=speed)
        print(self.i2c.scan())
        
    def read(self, memadd, nbytes):
        return self.i2c.readfrom_mem(self.address, memadd, nbytes)
        
    def write(self, memadd, buf):
        data = buf.to_bytes(1, 'big')
        return self.i2c.writeto_mem(self.address, memadd, data)
    
    
ps = Pressure_Sensor()
pressure_adcf = 0
while True:
    i=0
    for i in range(0,6):
        ps.write(0x30, 0x0A)
        command = ps.read(0x30, 1)
        while (command[0] & 0b00001000) != 0:
            command = ps.read(0x30, 1)
        pressure_H = int.from_bytes(ps.read(0x06, 1), 'big')
        pressure_C = int.from_bytes(ps.read(0x07, 1), 'big')
        pressure_L = int.from_bytes(ps.read(0x08, 1), 'big')
        pressure_adc = pressure_H * 65536 + pressure_C * 256 + pressure_L
        pressure_adcf += pressure_adc
    pressure_adcf=pressure_adcf/6.0
    k = 32
    if pressure_adcf > 8388608:
        pressure = (pressure_adcf - 16777216) / k
    else:
        pressure = pressure_adcf / k
    
    print('adc value =', pressure_adcf, 'pressure = ', pressure)
    pressure_adcf = 0
    
    temp_h = int.from_bytes(ps.read(0x09, 1), 'big')
    temp_l = int.from_bytes(ps.read(0x0A, 1), 'big')
    temp_adc = temp_h * 256 + temp_l
    print('temp=',temp_adc/256.0)
    time.sleep_ms(300)
#pressure = (pressure_adc - 16777216)*(100/8388608)
#pressure = pressure_adc*(300/8388607)