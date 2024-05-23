from machine import Pin
import utime
 
rs = Pin(5,Pin.OUT)
e = Pin(6,Pin.OUT)
d4 = Pin(10,Pin.OUT)
d5 = Pin(11,Pin.OUT)
d6 = Pin(12,Pin.OUT)
d7 = Pin(13,Pin.OUT)
UP = Pin(28,Pin.IN)
DOWN = Pin(27,Pin.IN)
SELECT = Pin(16,Pin.IN)
led=Pin(20,Pin.OUT)
 
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
setUpLCD()

uparrow= bytearray([0b00000100,0b00001110,0b0011111,0b00000100,0b00000100,0b00000100,0b00000100,0b00000000])
downarrow= bytearray([0b00000100,0b00000100,0b00000100,0b00000100,0b00011111,0b00001110,0b00000100,0b00000000])

def uparrow_display(line,pos):
    sendcmd(0b01000000)
    for i in range(8):
        send2LCD8(uparrow[i])
    sendcmd(0b00000010)
    sendcmd(0b10000000)
    setCursor(line,pos)
    send2LCD8(00000000)
utime.sleep_ms(2000)   
    

def downarrow_display(line,pos):
    sendcmd(0b01001000)
    for i in range(8):
        send2LCD8(downarrow[i])
    sendcmd(0b00000010)
    sendcmd(0b10000000)
    setCursor(line,pos)
    send2LCD8(0b00000001)
utime.sleep_ms(2000) 


setUpLCD()
rs.value(1)
displayString(1,0,'select led color')
displayString(2,0,'to display')
#uparrow_display(2,6)
utime.sleep_ms(3000)
#downarrow_display(2,7)
#displayString(2,9,'to chng')




count=0
def UP_INT(UP):
    UP.irq(handler=None)
    start=utime.ticks_ms()
    if utime.ticks_diff(utime.ticks_ms,start)>500:
        global count
        count-=1
        if count==1:
            displayString(1,0,'1.Black')
        elif count==2:
            setUpLCD()
            displayString(1,0,'2.Blue')
        elif count==3:
            setUpLCD()
            displayString(1,0,'3.Red')
        elif count==4:
            setUpLCD()
            displayString(1,0,'4.Orange')
    UP.irq(handler=UP_INT)
    
UP.irq(trigger=Pin.IRQ_RISING, handler=UP_INT)


count=0
def DOWN_INT(DOWN):
    DOWN.irq(handler=None)
    start=utime.ticks_ms()
    if utime.ticks_diff(utime.ticks_ms,start)>500:
        global count
        count+=1
        if count==1:
            setUpLCD()
            displayString(1,0,'1.Black')
        elif count==2:
            setUpLCD()
            displayString(1,0,'2.Blue')
        elif count==3:
            setUpLCD()
            displayString(1,0,'3.Red')
        elif count==4:
            setUpLCD()
            displayString(1,0,'4.Orange')
        
    
    DOWN.irq(handler=DOWN_INT)   
            
DOWN.irq(trigger=Pin.IRQ_RISING, handler=DOWN_INT)


def SELECT_INT(SELECT):
    SELECT.irq(handler=None)
    start=utime.ticks_ms()
    if utime.ticks_diff(utime.ticks_ms,start)>500:
        if count==3:
            led.value(1)
            utime.sleep_ms(1000)
            led.value(0)
    SELECT.irq(handler=SELECT_INT)
    
SELECT.irq(trigger=Pin.IRQ_RISING, handler=SELECT_INT)
