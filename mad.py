from machine import Pin,UART #importing PIN and PWM
import utime #importing time


#Defining UART channel and Baud Rate
uart = UART(0,9600)


LED = Pin(20, Pin.OUT)



while True:
    data=uart.read() #Getting data
    data=str(data) #Converting bytes to str type
    print(data)
    print("1")
        
    if(data == 'yes'):
        print("working")
           
    elif('LED_OFF' in data):
        print("working")
    utime.sleep(1)   
        