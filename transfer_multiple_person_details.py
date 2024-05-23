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

def on_rx(data):
    print("Data received: ", data)
    data_string = data.decode('utf-8')
    data_list = data_string.split(',')# Split the string by commas
    print(data_list)
    processed_list = [x if x != '' else '0' for x in data_list]#replacing empty values('') with 0
    processed_list.pop()
    print(processed_list)
    
    
    data = eeprom.read(0, 256)
    last_star_addr = data.rfind(b'*')# Find the position of the last '*' in the data string
    nda = last_star_addr + 1#new data address
    print('nda = ',nda)
    
    #storing patient details
    eeprom.write(0+nda,int(data_list[0]).to_bytes(1, 'big'))#converting and storing bed number in a byte 
    eeprom.write(1+nda,int(data_list[2]).to_bytes(2, 'big'))#converting and storing age in 2 bytes
    eeprom.write(3+nda,int(float(data_list[3])*10).to_bytes(1,'big'))#converting and storing weight in 1 bytes(max input is 10 kg and float also possible, maximum float= 9.9kg so multiply by 10 i.e.,99 and store it as a byte, when displaying divide by 10)
    eeprom.write(4+nda,data_list[5])#storing pincode as 6 characters
    eeprom.write(10+nda,int(data_list[6]).to_bytes(1, 'big'))#storing incubation indication ( a number 1-30 so stored in byte)
    
    #storing system details
    if data_list[7] == 'true':#storing whether L1 is on or off
        eeprom.write(11+nda,'1')
        eeprom.write(12+nda,int(data_list[8]).to_bytes(1, 'big'))#storing L1 frequency max=120 so stored as a byte
        eeprom.write(13+nda,int(data_list[9]).to_bytes(1, 'big'))#storing L1 duration max=40 so stored as a byte
    else:
        eeprom.write(11+nda,'0')
        eeprom.write(12+nda,'0')
        eeprom.write(13+nda,'0')
    if data_list[10] == 'true':#storing whether L2 is on or off
        eeprom.write(14+nda,'1')
        eeprom.write(15+nda,int(data_list[11]).to_bytes(1, 'big'))#storing L2 frequency max=120 so stored as a byte
        eeprom.write(16+nda,int(data_list[12]).to_bytes(1, 'big'))#storing L2 duration max=40 so stored as a byte
    else:
        eeprom.write(14+nda,'0')
        eeprom.write(15+nda,'0')
        eeprom.write(16+nda,'0')
    if data_list[13] == 'true':#storing whether L3 is on or off
        eeprom.write(17+nda,'1')
        eeprom.write(18+nda,int(data_list[14]).to_bytes(1, 'big'))#storing L3 frequency max=120 so stored as a byte
        eeprom.write(19+nda,int(data_list[15]).to_bytes(1, 'big'))#storing L3 duration max=40 so stored as a byte
    else:
        eeprom.write(17+nda,'0')
        eeprom.write(18+nda,'0')
        eeprom.write(19+nda,'0')
    eeprom.write(20+nda,processed_list[1])#storing name
    eeprom.write(20+len(processed_list[1])+nda,processed_list[4])#storing date
    eeprom.write(20+len(processed_list[1])+len(processed_list[4])+nda,'*')
    print(20+len(processed_list[1])+len(processed_list[4]))
    print(eeprom.read(20+len(processed_list[1])+len(processed_list[4]),1))
    
def printdetails(add):
    namecount=0
    datecount=1
    print('PATIENT DETAILS:')
    print('bed no = ',int.from_bytes(eeprom.read((0+add),1),'big'))
    for i in range (0,30):
        if eeprom.read(20+i+add,1).isdigit():
            break
        else:
            namecount+=1
    print('name = ',eeprom.read(20+add,namecount).decode('utf-8'))
    print('age = ',int.from_bytes(eeprom.read((1+add),2),'big'))
    print('weight = ',(int.from_bytes(eeprom.read(3+add,1),'big'))/10)
    for j in range(0,10):
        if eeprom.read(20+namecount+j,1) == b'*':
            break
        else:
            datecount +=1
    print('Date of arrival = ',eeprom.read(20+namecount+add,datecount-1).decode('utf-8'))
    print('pincode = ',eeprom.read(4+add,6).decode('utf-8'))
    print('incubation indication = ',int.from_bytes(eeprom.read(10+add,1),'big'))
    print('SYSTEM DETAILS:')
    if eeprom.read(11+add,1) == b'1':
        print('L1 = on with freq=',int.from_bytes(eeprom.read(12+add,1),'big'),'for duration=',int.from_bytes(eeprom.read(13+add,1),'big'))
    else:
        print('L1 = off')
    if eeprom.read(14+add,1) == b'1':
        print('L2 = on with freq=',int.from_bytes(eeprom.read(15+add,1),'big'),'for duration=',int.from_bytes(eeprom.read(16+add,1),'big'))
    else:
        print('L2 = off')
    if eeprom.read(17+add,1) == b'1':
        print('L3 = on with freq=',int.from_bytes(eeprom.read(18+add,1),'big'),'for duration=',int.from_bytes(eeprom.read(19+add,1),'big'))
    else:
        print('L3 = off')
    
print('old or new user?')
ip=input()
if ip == 'new':   
    while True:
        if sp.is_connected():# Check if a BLE connection is established
            sp.on_write(on_rx)# Set the callback function for data reception
        else:
            sp.advertise()
            time.sleep(1)
count = 0
count1 = 0
if ip == 'old':
    for i in range(0,1000):
        if eeprom.read(i,1) == b'*':
            count += 1
    if count == 0:
        print('Machine not used yet. No previous details available')
    else:
        print(count,'patients details available. Select a number from 1 to ', count)

    no = int(input())-1
    print(no)
    if no == 0:
        printdetails(0)
    else: 
        for i in range (0,200):
            if eeprom.read(i,1) == b'*':
                count1 += 1
                if count1 == no:
                    add = i+1
                    print(add)
                    printdetails(add)
    