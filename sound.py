import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)
while True:
    select = int(input("Please select the type of output <1-3>, 0:exit -> "))
    if select == 0:
        GPIO.output(7, 0)
        break

    if select == 1:
        for i in range(1000):
            for j in range(250):
                GPIO.output(7,1)
            for j in range(250):
                GPIO.output(7,0)
    if select == 2:
        for i in range(1000):
            for j in range(250):
                    GPIO.output(7,1)
            for j in range(1000):
                    GPIO.output(7,0)
    if select == 3:
        for i in range(1000):
            for j in range(1000):
                GPIO.output(7,1)
            for j in range(250):
                GPIO.output(7,0)

