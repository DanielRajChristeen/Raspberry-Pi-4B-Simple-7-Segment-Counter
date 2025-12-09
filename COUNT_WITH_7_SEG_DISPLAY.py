import RPi.GPIO as GPIO
import time

# ------------------------------------------
# BUTTONS
# ------------------------------------------
INC_BUT = 17
DEC_BUT = 18

# ------------------------------------------
# 7-SEGMENT PINS (AVOID 17,18)
# ------------------------------------------
SEGMENTS = {
    'A': 2,
    'B': 3,
    'C': 4,
    'D': 14,
    'E': 15,
    'F': 23,
    'G': 24
}

DIGIT_MAP = {
    0: ['A','B','C','D','E','F'],
    1: ['B','C'],
    2: ['A','B','G','E','D'],
    3: ['A','B','C','D','G'],
    4: ['F','G','B','C'],
    5: ['A','F','G','C','D'],
    6: ['A','F','E','D','C','G'],
    7: ['A','B','C'],
    8: ['A','B','C','D','E','F','G'],
    9: ['A','B','C','D','F','G']
}

# ------------------------------------------
# SETUP
# ------------------------------------------
GPIO.setmode(GPIO.BCM)

# Buttons
GPIO.setup(INC_BUT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(DEC_BUT, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Segments
for pin in SEGMENTS.values():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

# ------------------------------------------
# FUNCTIONS
# ------------------------------------------
def clear_display():
    for pin in SEGMENTS.values():
        GPIO.output(pin, GPIO.LOW)

def display_digit(number):
    clear_display()

    if number not in DIGIT_MAP:
        return

    for seg in DIGIT_MAP[number]:
        GPIO.output(SEGMENTS[seg], GPIO.HIGH)

# ------------------------------------------
# VARIABLES
# ------------------------------------------
count = 0
pre_inc = GPIO.HIGH
pre_dec = GPIO.HIGH
pre_count = -1   # force print + display first time

# ------------------------------------------
# MAIN LOOP
# ------------------------------------------
try:
    while True:

        inc = GPIO.input(INC_BUT)
        dec = GPIO.input(DEC_BUT)

        # rising → falling edge detect
        if (inc == GPIO.LOW) and (pre_inc == GPIO.HIGH):
            count += 1

        elif (dec == GPIO.LOW) and (pre_dec == GPIO.HIGH):
            count -= 1

        if count < 0:
            count = 0
        if count > 9:
            count = 9   # 7-seg displays only 0–9

        # update display only on change
        if count != pre_count:
            print(count)
            display_digit(count)
            pre_count = count

        pre_inc = inc
        pre_dec = dec

        time.sleep(0.02)  # debounce

except KeyboardInterrupt:
    clear_display()
    GPIO.cleanup()
