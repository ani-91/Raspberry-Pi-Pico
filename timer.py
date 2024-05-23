import machine
import time
import utime


class RTC:
    def __init__(self, sda_pin=14, scl_pin=15, port=1, speed=100000, address=0x68, register=0x00):
        self.rtc_address = address  
        self.rtc_register = register  
        sda = machine.Pin(sda_pin,machine.Pin.PULL_UP)  
        scl = machine.Pin(scl_pin,machine.Pin.PULL_UP)  
        self.i2c = machine.I2C(port, sda=sda, scl=scl, freq=speed)  

   
    def DS3231_SetTime(self, NowTime=b"\x00\x23\x12"):
        self.i2c.writeto_mem(self.rtc_address, self.rtc_register, NowTime)

    # DS3231 gives data in bcd format. This has to be converted to a binary format.
    def bcd2hex(self, value):
        return (value or 0) - 6 * ((value or 0) >> 4)
    

    # Read the Realtime from the DS3231 with errorhandling. Currently two output modes can be used.
    def DS3231_ReadTime(self, mode=0):
        try:
            buffer = self.i2c.readfrom_mem(self.rtc_address, self.rtc_register, 3)
            hour = self.bcd2hex(buffer[2]) 
            minute =self.bcd2hex(buffer[1])
            second =self.bcd2hex(buffer[0]) 
            if mode == 0:  
                return second, minute, hour
            if mode == 1:  
                time_string = f"{hour}:{minute}:{second}"
                return time_string
            

        except Exception as e:
            return (
                "Error: is the DS3231 not connected or some other problem (%s)" % e
            )  
        
rtc = RTC()
rtc.DS3231_SetTime(b'\x00\x00\x00')
microsec=0
millisec=0
sec=0
mint=0
  
while True:
    t = rtc.DS3231_ReadTime(1) 
    print(t)
    time.sleep(1)
    print(time.localtime())
    
    
    
    
    
    
    
    
'''    
    microsec+=1
    if microsec>1000:
        microsec=0
        millisec+=1
        if millisec>1000:
            millisec=0
            sec+=1
            if sec>60:
                sec=0
                mint+=1
    print('sec=',sec)
    utime.sleep(1000)
'''