import RPi.GPIO as GPIO
import time

servo = 18  # GPIO18 = physical pin 12

GPIO.setmode(GPIO.BCM)
GPIO.setup(servo, GPIO.OUT)

pwm = GPIO.PWM(servo, 50)
pwm.start(2.5)

def smooth_move(pwm, start, end, step=0.1, delay=0.02):
    dc = start
    while abs(dc - end) > 0.01:
        pwm.ChangeDutyCycle(dc)
        time.sleep(delay)
        dc += step if end > start else -step
    pwm.ChangeDutyCycle(end)
    time.sleep(0.5)

# Adjust these values for your specific servo's safe range
ZERO_DEG = 3.0
NINETY_DEG = 7.5
MAX_DEG = 12.5

try:
    print("0 deg")
    smooth_move(pwm, NINETY_DEG, ZERO_DEG)
    time.sleep(1)

    print("90 deg")
    smooth_move(pwm, ZERO_DEG, NINETY_DEG)
    time.sleep(1)

    print("180 deg")
    smooth_move(pwm, NINETY_DEG, MAX_DEG)
    time.sleep(1)

finally:
    
    pwm.stop()
    del pwm  # Explicitly delete the PWM object
    GPIO.cleanup()
