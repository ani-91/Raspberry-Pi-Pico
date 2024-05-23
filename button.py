from machine import Pin
import time
button=Pin(15,Pin.IN)
led=Pin(16,Pin.OUT)
while True:
    state=button.value()
    print(state)
    if state==1:
        led.toggle
        
    

            
        
       
        


        
      
    
  
  