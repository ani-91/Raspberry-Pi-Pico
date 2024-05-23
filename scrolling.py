import machine
import utime

 
rs = machine.Pin(5,machine.Pin.OUT)
e = machine.Pin(6,machine.Pin.OUT)
d4 = machine.Pin(10,machine.Pin.OUT)
d5 = machine.Pin(11,machine.Pin.OUT)
d6 = machine.Pin(12,machine.Pin.OUT)
d7 = machine.Pin(13,machine.Pin.OUT)
up = machine.Pin(28,machine.Pin.IN)
down = machine.Pin(27,machine.Pin.IN)
up.irq(trigger=Pin.IRQ_RISING, handler=scroll_up)
down.irq(trigger=Pin.IRQ_RISING, handler=scroll_down)

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

def split_string(l, s):
    n = len(s) // l
    parts = []
    temp = 0
    for i in range(0, n + 1):
        split = s[temp : l + temp]
        temp += l
        parts.append(split)   
    return parts

def scroll_display(input_string):
    parts = split_string(16, input_string)
    for i in range(0, (len(input_string) // 16) + 1):
        if i != 0 and (i % 2) == 0:
            utime.sleep(2)
            sendcmd(0b00000001)
            displayString((i % 2) + 1, 0, parts[i])
            
            
        else:
            displayString((i % 2) + 1, 0, parts[i])

def scroll_button(input_string, count):
    parts = split_string(16, input_string)
    displayString(parts[count % 16])
    
def scroll_up():
    

setUpLCD()

input_string="this text is too long to display on screen."



scroll_display(input_string)
'''
if i>:
    sendcmd(0b00011000)
    send2LCD8(ord(input_string[i]))
 '''   

