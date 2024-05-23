import machine
import utime

# Configure PWM with a frequency of 50Hz (standard for most servos)
servo = machine.PWM(machine.Pin(4))
servo.freq(50)

# Function to set the angle of the servo motor
def set_servo_angle(angle):
    # Map the input angle range (-90 to 90) to the pulse width range (0.5 to 2.4 milliseconds)
    pulse_width = int(500 + ((angle + 90) * 190)/18)
    print(pulse_width)
    servo.duty_ns(pulse_width * 1000)
   
set_servo_angle(90)
