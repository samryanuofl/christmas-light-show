import RPi.GPIO as GPIO
import subprocess
import csv
import time
import atexit
import sys


CsvToGpio = {0: 20, 1: 6, 2: 26, 3: 22, 4: 13, 5: 21, 6: 19, 7: 16, 8: 6, 9: 13}


def cleanup():
    print('Cleaning up before exit')
    GPIO.cleanup()


class TimeSlot:
    def __init__(self, time_start_ms, time_end_ms, led_states):
        self.time_start_ms = time_start_ms
        self.time_end_ms = time_end_ms
        self.led_states = led_states

    def __repr__(self):
        return 'Start:' + str(self.time_start_ms) + ' End:' + str(self.time_end_ms) + ' States:' + str(self.led_states)


def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    for key, value in CsvToGpio.iteritems():
        print('Setting pin ' + str(value))
        GPIO.setup(value, GPIO.OUT)


def set_gpio(led_states):
    for idx, led in enumerate(led_states):
        GPIO.output(CsvToGpio[idx], led)


def get_current_timeslot(current_time, timeslots):
    for t in timeslots:
        if (current_time >= t.time_start_ms) and (current_time < t.time_end_ms):
            return t
    return None


def run_lightshow(audio_file, timeslots):
    audio_proc = subprocess.Popen(['omxplayer', 'carol.mp3', '> /dev/null'], stdout=subprocess.PIPE)
    start_time = time.time()
    while True:
        current_time = (time.time() - start_time) * 1000
        current_timeslot = get_current_timeslot(current_time, timeslots)
        if current_timeslot:
            set_gpio(current_timeslot.led_states)
        else:
            print current_time
            sys.exit(-1)


def get_timeslots_from_rows(rows):
    timeslots = []
    for idx, row in enumerate(rows):
        state_strings = row[1:]
        states = []
        for s in state_strings:
            states.append(bool(int(s)))
        if idx == (len(rows) - 1):
            timeslots.append(TimeSlot(int(row[0]), 1000000000, states))
        else:
            next_row = rows[idx + 1]
            time_end = int(next_row[0])
            timeslots.append(TimeSlot(int(row[0]), time_end, states))
    return timeslots


def main():
    atexit.register(cleanup)
    setup_gpio()
    rows = []
    with open('control.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=",", quotechar="|")
        for row in reader:
            rows.append(row)
    timeslots = get_timeslots_from_rows(rows)
    print(timeslots)
    run_lightshow('example.mp3', timeslots)


if __name__ == '__main__':
    main()
