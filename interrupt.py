from machine import Pin
import time

led = Pin(18,Pin.OUT)  
led.value(0)
Switch = Pin(15,Pin.IN,Pin.PULL_DOWN)
last_time=0

def Switch_INT(Switch):         
    global Switch_State
   
    Switch.irq(handler=None) 
    
    
    if (Switch.value() == 1) and (Switch_State == 0) :  
        Switch_State = 1
        led.on()    
        print('ON')
        
        
            
    if (Switch.value() == 0) and (Switch_State == 1) : 
        Switch_State = 0     
        led.value(0)    
        print('OFF')
        

    Switch.irq(handler=Switch_INT)
    
Switch.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=Switch_INT)

while True:
    Switch_State = Switch.value()
    print("Switch State=", Switch_State)
    print('hi')
    time.sleep(1)
    

















