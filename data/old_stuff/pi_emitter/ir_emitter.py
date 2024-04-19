#!/usr/bin/python

# -*- coding: utf-8 -*- 

#import RPi.GPIO as GPIO
#from time import sleep
import pigpio

def main(args):
    
#    duty_cycle = 0.0001
#    GPIO.setwarnings(False)
#    GPIO.setmode(GPIO.BCM)

    outpin_1 = 18
    outpin_2 = 13
    
#   GPIO.setup(outpin_1, GPIO.OUT)
#   GPIO.setup(outpin_2, GPIO.OUT)
#   pwm_1 = GPIO.PWM(outpin_1,38000)
#   pwm_2 = GPIO.PWM(outpin_2,38000)
     
    pwm_1 = pigpio.pi()
    pwm_2 = pigpio.pi()

#   pwm_2.start(duty_cycle)
#   pwm_1.start(duty_cycle)     
#   GPIO.output(outpin_1, 1)
#   GPIO.output(outpin_2, 1)
    
    pwm_1.hardware_PWM(outpin_1, 38000, 500000)
    pwm_2.hardware_PWM(outpin_2, 38000, 500000)	

#   pwm_1.stop()
#   pwm_2.stop()

    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))



