MID = 1500000
MIN = 1000000
MAX = 2000000

pwm = PWM(Pin(0))
pwm.freq(50)
i=0
pwm.duty_ns(MAX)
def opn():
    pwm.duty_ns(MID)
    
def close():
    for i in range(15,25,1):
        result = (float(i/10)) * 10 ** 6
        pwm.duty_ns(int(result))