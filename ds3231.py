import machine
import time
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
        
rtc = RTC()
rtc.DS3231_SetTime(b'\x00\x14\x18\x28\x23\x06\x23')
while True:
    t = rtc.DS3231_ReadTime(1) 
    print(t)
    time.sleep(1)
    

