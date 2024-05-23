import machine
import utime

 
rs = machine.Pin(5,machine.Pin.OUT)
e = machine.Pin(6,machine.Pin.OUT)
d4 = machine.Pin(10,machine.Pin.OUT)
d5 = machine.Pin(11,machine.Pin.OUT)
d6 = machine.Pin(12,machine.Pin.OUT)
d7 = machine.Pin(13,machine.Pin.OUT)
 
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
    send2LCD4(0b0011)#8 bit
    send2LCD4(0b0011)#8 bit
    send2LCD4(0b0011)#8 bit
    send2LCD4(0b0010)#4 bit
    send2LCD8(0b00101000)#4 bit,2 lines?,5*8 bots
    send2LCD8(0b00001100)#lcd on, blink off, cursor off.
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
        utime.sleep_ms(100)

setUpLCD()

benz = bytearray([0b00001110, 0b00010101, 0b00010101, 0b00010101, 0b00011011, 0b00010001, 0b00001110, 0b00000000])


sendcmd(0b01000000)
for i in range(8):
    send2LCD8(benz[i])
sendcmd(0b00000010)
sendcmd(0b10000000)
send2LCD8(0)
