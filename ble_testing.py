from machine import Pin 
import bluetooth
import time
from ble_simple_peripheral import BLESimplePeripheral

# Create a Bluetooth Low Energy (BLE) object
ble = bluetooth.BLE()

# Create an instance of the BLESimplePeripheral class with the BLE object
sp = BLESimplePeripheral(ble)

# Define a callback function to handle received data
def on_rx(data):
    print("Data received: ", data)  # Print the received data

    # Convert bytes to a string
    data_string = data.decode('utf-8')

    # Split the string by commas
    data_list = data_string.split(',')
    print(data_list)
    print(type(data_list[0]))

# Start an infinite loop

time.sleep(1)

while True:
    if sp.is_connected():# Check if a BLE connection is established
        sp.on_write(on_rx)# Set the callback function for data reception
    else:
        sp.advertise()
        time.sleep(1)
        
    