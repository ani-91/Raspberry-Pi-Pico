from machine import Pin,I2C
import time

class PS:
    def __init__(self, sda_pin=0, scl_pin=1, port=0, speed=100000, address=0x6D):
        self.address = address 
        sda = Pin(sda_pin)  
        scl = Pin(scl_pin)  
        self.i2c = machine.I2C(port, sda=sda, scl=scl, freq=speed)
        
    def read(self, memadd, nbytes):
        return self.i2c.readfrom_mem(self.address, memadd, nbytes)
    
    def write(self, memadd, buf):
        return self.i2c.writeto_mem(self.address, memadd, bytearray([buf]))
ps=PS()

ps.write(0x30,0x1B)
command=ps.read(0x30,1)

while (command & 0x08) == 1:
    command
    
pressure_H=int(ps.read(0x06,1))
pressure_C=int(ps.read(0x07,1))
pressure_L=int(ps.read(0x08,1))

pressure_adc=pressure_H*65536+pressure_C*258+pressure_L

if (pressure_adc>8388608):
    pressure=(pressure_adc-16777216)/k
else:
    pressure=pressure_adc/k
    
print('adc value=',pressure_adc,'pressure=',pressure)


