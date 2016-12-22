import RPi.GPIO as GPIO
import time
import subprocess


def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(21, GPIO.IN)
#        is_pressed = GPIO.input(21) 
    out = subprocess.Popen(['omxplayer', 'example.mp3'])

if __name__ == '__main__':
    main()
