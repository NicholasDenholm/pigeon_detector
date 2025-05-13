from gpiozero import AngularServo
import time

myGPIO = 18
servo_delay = 0.001
my_correction = 0.0
maxPW = (2.5+my_correction)/1000
minPW = (0.5-my_correction)/1000
servo = AngularServo(myGPIO, initial_angle=0, min_angle=0, max_angle=180, min_pulse_width=minPW, max_pulse_width=maxPW)

def loop(start_angle:int, end_angle:int, step:int, rotations:int):
    count = 0
    while count < rotations:
        for angle in range(start_angle, end_angle + 1, step): # specify your angle
            servo.angle = angle
            time.sleep(servo_delay)
        time.sleep(0.5)

        for angle in range(end_angle, start_angle - 1, -step): # specify your angle to rotate back to
            servo.angle = angle
            time.sleep(servo_delay)
        time.sleep(0.5)
        count = count + 1

if __name__ == "__main__":

    print("Rotating servo ...")
    try:
        # Define your variables here
        start_angle = 0
        end_angle = 180
        step = 1
        rotations = 2
        # Call the function
        loop(start_angle, end_angle, step, rotations)
        print("Completed ", rotations, "rotations.")
    except KeyboardInterrupt:
        print("Ending program.")



