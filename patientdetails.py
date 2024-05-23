from machine import I2C, Pin
import utime

button=Pin(27,Pin.IN)
led=Pin(20,Pin.OUT)

def setup():
    size = 50
    empty_buffer = b'\xFF' * size
    data = eeprom.read(0, size)
    if data == empty_buffer:
        print("EEPROM is empty")
    else:
        print('age=',int.from_bytes(eeprom.read(5,2),'big'))
        print('name=',eeprom.read(20,30).rstrip(b'\xff').decode('utf-8'))
        print('weight=',(int.from_bytes(eeprom.read(0,2),'big'))/100)
        print('old user or new?=')

class AT24C64(object):
    def __init__(self, i2c, i2c_addr, pages=256, bpp=32):
        self.i2c = i2c
        self.i2c_addr = i2c_addr
        self.pages = pages
        self.bpp = bpp # bytes per page

    def capacity(self):
        return self.pages * self.bpp #capacity in bytes

    def read(self, memadd, nbytes):
        return self.i2c.readfrom_mem(self.i2c_addr, memadd, nbytes, addrsize=16)

    def write(self, memadd, buf):
        offset = memadd % self.bpp
        partial=0
         # partial page write
        if offset > 0:
            partial = self.bpp - offset
            self.i2c.writeto_mem(self.i2c_addr, memadd, buf[0:partial], addrsize=16)
            utime.sleep_ms(5)
            memadd += partial
         # full page write
        for i in range(partial, len(buf), self.bpp):
            self.i2c.writeto_mem(self.i2c_addr, memadd+i-partial, buf[i:i+self.bpp], addrsize=16)
            utime.sleep_ms(5)
            
    def wipe(self):
        buf = b'\xff' * 32
        for i in range(256):
            self.write(i*32, buf)
            
    
            
            
sda=machine.Pin(8)
scl=machine.Pin(9)            
i2c=machine.I2C(0,sda=sda, scl=scl, freq=400000)
i2caddr=80
eeprom = AT24C64(i2c,i2caddr)
setup()
led_state=led.value()
count=0

def INT_LED(button):
    
    start=utime.ticks_ms()
    if utime.ticks_diff(utime.ticks_ms,start)>1000:
        global count
        count=count+1
        led.toggle()
        led_state=led.value()
        eeprom.write(0,str(led_state))
        eeprom.write(1,str(count))
    
button.irq(trigger=button.IRQ_RISING, handler=INT_LED)

#eeprom.wipe()
o_n=input()
if o_n == 'old':
    print('...')
if o_n == 'new':
    eeprom.wipe()
    name= input("enter name: ")
    eeprom.write(20,name)
    age = int(input("Enter age in days: ")).to_bytes(2, 'big')
    eeprom.write(5,age)
    weight=int(float(input("enter weight:"))*100).to_bytes(2,'big')
    eeprom.write(0,weight)
    

