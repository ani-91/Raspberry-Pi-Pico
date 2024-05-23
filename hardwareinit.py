from machine import I2C, Pin
import utime
import time

class LCD():
    rs = Pin(5,Pin.OUT)
    e = Pin(6,Pin.OUT)
    d4 = Pin(10,Pin.OUT)
    d5 = Pin(11,Pin.OUT)
    d6 = Pin(12,Pin.OUT)
    d7 = Pin(13,Pin.OUT)

 
    def pulseE():
        e.value(1)
        utime.sleep_us(40)
        e.value(0)
        utime.sleep_us(40)
    def returnHome():
        rs.value(0)
        send2LCD8(0b00000010)
        rs.value(1)
        utime.sleep_ms(2000)
    def moveCursorRight():
        rs.value(0)
        send2LCD8(0b00010100)
        rs.value(1)
    def setCursor(line, pos):
        b = 0
        if line==1:
            b=0
        elif line==2:
            b=40
        elif line==3:
            b=20
        elif line==4:
            b=60
        returnHome()
        for i in range(0, b+pos):
            moveCursorRight()
    def send2LCD4(BinNum):
        d4.value((BinNum & 0b00000001) >>0)
        d5.value((BinNum & 0b00000010) >>1)
        d6.value((BinNum & 0b00000100) >>2)
        d7.value((BinNum & 0b00001000) >>3)
        pulseE()
    def send2LCD8(BinNum):
        d4.value((BinNum & 0b00010000) >>4)
        d5.value((BinNum & 0b00100000) >>5)
        d6.value((BinNum & 0b01000000) >>6)
        d7.value((BinNum & 0b10000000) >>7)
        pulseE()
        d4.value((BinNum & 0b00000001) >>0)
        d5.value((BinNum & 0b00000010) >>1)
        d6.value((BinNum & 0b00000100) >>2)
        d7.value((BinNum & 0b00001000) >>3)
        pulseE()
    def setUpLCD():
        rs.value(0)
        led.value(0)
        send2LCD4(0b0011)#8 bit
        send2LCD4(0b0011)#8 bit
        send2LCD4(0b0011)#8 bit
        send2LCD4(0b0010)#4 bit
        send2LCD8(0b00101000)#4 bit,2 lines?,5*8 bots
        send2LCD8(0b00001101)#lcd on, blink off, cursor off.
        send2LCD8(0b00000110)#increment cursor, no display shift
        send2LCD8(0b00000001)#clear screen
        utime.sleep_ms(2)#clear screen needs a long delay
    def sendcmd(binum):
        rs.value(0)
        send2LCD8(binum)
        rs.value(1)
    def displayString(row, col, input_string):
        setCursor(row,col)
        for x in input_string:
            send2LCD8(ord(x))
####
class AT24C64(object):
    def __init__(self, sda_pin=14, scl_pin=15, port=0, speed=100000, address=80, register=0x00 pages=256, bpp=32):
        self.i2c = machine.I2C(port, sda=sda_pin, scl=scl_pin, freq=speed) 
        self.i2c_addr = address 
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
            time.sleep_ms(5)
            memadd += partial
         # full page write
        for i in range(partial, len(buf), self.bpp):
            self.i2c.writeto_mem(self.i2c_addr, memadd+i-partial, buf[i:i+self.bpp], addrsize=16)
            time.sleep_ms(5)
            
    def wipe(self):
        buf = b'\xff' * 32
        for i in range(256):
            self.write(i*32, buf)
            
    def check_eeprom_empty(self,start,end):
        size = end-start
        empty_buffer = b'\xFF' * size
        data = eeprom.read(0, size)

    
        if data == empty_buffer:
            print("EEPROM is empty")
        else:
            print(data)

###
class RTC:
    w = ["FRI", "SAT", "SUN", "MON", "TUE", "WED", "THU"]
    def __init__(self, sda_pin=14, scl_pin=15, port=1, speed=100000, address=0x68, register=0x00):
        self.rtc_address = address  
        self.rtc_register = register  
        sda = machine.Pin(sda_pin,machine.Pin.PULL_UP)  
        scl = machine.Pin(scl_pin,machine.Pin.PULL_UP)  
        self.i2c = machine.I2C(port, sda=sda, scl=scl, freq=speed)  

   
    def DS3231_SetTime(self, NowTime=b"\x00\x23\x12\x28\x14\x07\x21"):
        self.i2c.writeto_mem(self.rtc_address, self.rtc_register, NowTime)

    # DS3231 gives data in bcd format. This has to be converted to a binary format.
    def bcd2hex(self, value):
        return (value or 0) - 6 * ((value or 0) >> 4)
    
    # Add a 0 in front of numbers smaller than 10
    def pre_zero(self, value):
        pre_zero = True  # Change to False if you don't want a "0" in front of numbers smaller than 10
        if pre_zero:
            if value < 10:
                value = f"0{value}"  # From now on the value is a string!
        return value

    # Read the Realtime from the DS3231 with errorhandling. Currently two output modes can be used.
    def DS3231_ReadTime(self, mode=0):
        try:
            buffer = self.i2c.readfrom_mem(self.rtc_address, self.rtc_register, 7)
            year = self.bcd2hex(buffer[6]) + 2000
            month = self.bcd2hex(buffer[5])  
            day = self.bcd2hex(buffer[4])  
            weekday = self.w[self.bcd2hex(buffer[3])]
            hour = self.pre_zero(self.bcd2hex(buffer[2])) 
            minute = self.pre_zero(self.bcd2hex(buffer[1]))  
            second = self.pre_zero(self.bcd2hex(buffer[0]))  
            if mode == 0:  
                return second, minute, hour, weekday, day, month, year
            if mode == 1:  
                time_string = f"{hour}:{minute}:{second}      {weekday} {day}.{month}.{year}"
                return time_string
            

        except Exception as e:
            return (
                "Error: is the DS3231 not connected or some other problem (%s)" % e
            )  
        
###
class ADC():
    def __init__(self, sda_pin=14, scl_pin=15, port=0, speed=100000, address=72, register=0x00):
        self.rtc_address = address  
        sda = machine.Pin(sda_pin,machine.Pin.PULL_UP)  
        scl = machine.Pin(scl_pin,machine.Pin.PULL_UP)  
        self.i2c = machine.I2C(port, sda=sda, scl=scl, freq=speed)
 
    def read_config():
        dev.writeto(address, bytearray([1]))
        result = dev.readfrom(address, 2)
        return result[0] << 8 | result[1]
 
    def read_value():
        dev.writeto(address, bytearray([0]))
        result = dev.readfrom(address, 2)
        config = read_config()
        config &= ~(7 << 12) & ~(7 << 9)
        config |= (4 << 12) | (0 << 9) | (1 << 15)
        config = [int(config >> i & 0xff) for i in (8, 0)]
        dev.writeto(address, bytearray([1] + config))
        return result[0] << 8 | result[1]
 
    def val_to_voltage(val, max_val=32767, voltage_ref=6.144):
        return val/ max_val * voltage_ref

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
    
lcd = LCD()
lcd.setUpLCD()
eeprom = AT24C64()
rtc = RTC()
adc = ADC()
ps = Pressure_Sensor()