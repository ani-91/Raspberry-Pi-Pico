from machine import Pin,I2C
i2c=I2C(0,sda=Pin(12),scl=Pin(13),freq=400000)
print(i2c.scan())
x=1
print(type(x))
print(bytearray([0x0A]))