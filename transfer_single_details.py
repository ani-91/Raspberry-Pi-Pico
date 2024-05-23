from machine import I2C, Pin
import utime 
import bluetooth
import time
from ble_simple_peripheral import BLESimplePeripheral



class AT24C64:
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
        for i in range(self.pages):
            self.write(i*32, buf)
            
    def check_eeprom_empty(self,start,end):
        size = end-start
        empty_buffer = b'\xFF' * size
        data = eeprom.read(0, size)

    
        if data == empty_buffer:
            return true
        else:
            return false

sda=machine.Pin(8)
scl=machine.Pin(9)            
i2c=machine.I2C(0,sda=sda, scl=scl, freq=400000)
i2caddr=80
eeprom = AT24C64(i2c,i2caddr)
            

ble = bluetooth.BLE()
sp = BLESimplePeripheral(ble)
global addr
memaddtag=0
addr=500

def on_rx(data):
    print("Data received: ", data)
    data_string = data.decode('utf-8')
    data_list = data_string.split(',')# Split the string by commas
    print(data_list)
    processed_list = [x if x != '' else '0' for x in data_list]#replacing empty values('') with 0
    print(processed_list)
    
    
    #storing patient details
    eeprom.write(0,int(data_list[0]).to_bytes(1, 'big'))#converting and storing bed number in a byte 
    eeprom.write(1,int(data_list[2]).to_bytes(2, 'big'))#converting and storing age in 2 bytes
    eeprom.write(3,int(float(data_list[3])*10).to_bytes(1,'big'))#converting and storing weight in 1 bytes(max input is 10 kg and float also possible, maximum float= 9.9kg so multiply by 10 i.e.,99 and store it as a byte, when displaying divide by 10)
    eeprom.write(4,data_list[5])#storing pincode as 6 characters
    eeprom.write(10,int(data_list[6]).to_bytes(1, 'big'))#storing incubation indication ( a number 1-30 so stored in byte)
    
    #storing system details
    if data_list[7] == 'true':#storing whether L1 is on or off
        eeprom.write(11,'1')
        eeprom.write(12,int(data_list[8]).to_bytes(1, 'big'))#storing L1 frequency max=120 so stored as a byte
        eeprom.write(13,int(data_list[9]).to_bytes(1, 'big'))#storing L1 duration max=40 so stored as a byte
    else:
        eeprom.write(11,'0')
        eeprom.write(12,'0')
        eeprom.write(13,'0')
    if data_list[10] == 'true':#storing whether L2 is on or off
        eeprom.write(14,'1')
        eeprom.write(15,int(data_list[11]).to_bytes(1, 'big'))#storing L2 frequency max=120 so stored as a byte
        eeprom.write(16,int(data_list[12]).to_bytes(1, 'big'))#storing L2 duration max=40 so stored as a byte
    else:
        eeprom.write(14,'0')
        eeprom.write(15,'0')
        eeprom.write(16,'0')
    if data_list[13] == 'true':#storing whether L3 is on or off
        eeprom.write(17,'1')
        eeprom.write(18,int(data_list[14]).to_bytes(1, 'big'))#storing L3 frequency max=120 so stored as a byte
        eeprom.write(19,int(data_list[15]).to_bytes(1, 'big'))#storing L3 duration max=40 so stored as a byte
    else:
        eeprom.write(17,'0')
        eeprom.write(18,'0')
        eeprom.write(19,'0')
    eeprom.write(20,processed_list[1])
    eeprom.write(20+len(processed_list[1]),processed_list[4])
   
    print('PATIENT DETAILS:')
    print('bed no = ',int.from_bytes(eeprom.read(0,1),'big'))
    print('name = ',eeprom.read(20,len(processed_list[1])).decode('utf-8'))
    print('age = ',int.from_bytes(eeprom.read(1,2),'big'))
    print('weight = ',(int.from_bytes(eeprom.read(3,1),'big'))/10)
    print('Date of arrival = ',eeprom.read(20+len(processed_list[1]),len(processed_list[4])).decode('utf-8'))
    print('pincode = ',str(eeprom.read(4,6),'utf-8'))
    print('incubation indication = ',int.from_bytes(eeprom.read(10,1),'big'))
    print('SYSTEM DETAILS:')
    if eeprom.read(11,1) == b'1':
        print('L1 was on with freq=',int.from_bytes(eeprom.read(12,1),'big'),'for duration=',int.from_bytes(eeprom.read(13,1),'big'))
    else:
        print('L1 was off')
    if eeprom.read(14,1) == b'1':
        print('L2 was on with freq=',int.from_bytes(eeprom.read(15,1),'big'),'for duration=',int.from_bytes(eeprom.read(16,1),'big'))
    else:
        print('L2 was off')
    if eeprom.read(17,1) == b'1':
        print('L3 was on with freq=',int.from_bytes(eeprom.read(18,1),'big'),'for duration=',int.from_bytes(eeprom.read(19,1),'big'))
    else:
        print('L3 was off')
  
    
while True:
    if sp.is_connected():# Check if a BLE connection is established
        sp.on_write(on_rx)# Set the callback function for data reception
    else:
        sp.advertise()
        time.sleep(1)