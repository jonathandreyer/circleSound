# -*- coding: utf-8 -*-
import logging
import atexit
import RPi.GPIO as GPIO


class A4988Driver:
    STEP = 18       # PWM0
    DIRECTION = 17
    MS1 = 15
    MS2 = 14
    MS3 = 4
    ENABLE = 27

    def __init__(self):
        self.logger = logging.getLogger('app.A4988Driver')
        self.logger.debug('init')

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        # Output
        GPIO.setup(self.DIRECTION, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.MS1, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.MS2, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.MS3, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.ENABLE, GPIO.OUT, initial=GPIO.HIGH)
        # PWM
        GPIO.setup(self.STEP, GPIO.OUT, initial=GPIO.LOW)
        self._pwm = GPIO.PWM(self.STEP, 0.1)

        atexit.register(self._exit)

        self._set_mode()
        self.set_direction(0)

    def set_speed(self, speed):
        self.logger.debug('set speed : ' + str(speed))
        self._pwm.ChangeFrequency(speed)

    def set_direction(self, dir):
        if dir:
            GPIO.output(self.DIRECTION, GPIO.HIGH)
        else:
            GPIO.output(self.DIRECTION, GPIO.LOW)

    def enable(self):
        self.logger.debug('enable')
        GPIO.output(self.ENABLE, GPIO.LOW)
        self._pwm.start(50)

    def disable(self):
        self.logger.debug('disable')
        GPIO.output(self.ENABLE, GPIO.HIGH)
        self._pwm.stop()

    def _set_mode(self):
        self.logger.debug('set to 8 microstep')
        GPIO.output(self.MS1, GPIO.HIGH)
        GPIO.output(self.MS2, GPIO.HIGH)
        GPIO.output(self.MS3, GPIO.HIGH)

    def _exit(self):
        self.logger.debug('exit')
        self.disable()
        self.set_speed(0.1)

        GPIO.cleanup(self.DIRECTION)
        GPIO.cleanup(self.MS1)
        GPIO.cleanup(self.MS2)
        GPIO.cleanup(self.MS3)
        GPIO.cleanup(self.ENABLE)
        #GPIO.cleanup(self.STEP)


if __name__ == "__main__":
    import time

    logger = logging.getLogger('app')

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')

    # Console output
    consolelog = logging.StreamHandler()
    consolelog.setFormatter(formatter)
    logger.addHandler(consolelog)
    logger.setLevel(logging.DEBUG)

    driv = A4988Driver()
    driv.enable()

    #driv.set_speed(750)
    #print('DC: 50')

    #time.sleep(14)

    driv.set_speed(1000)

    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print('interrupted!')

    driv.disable()

    print('end')
