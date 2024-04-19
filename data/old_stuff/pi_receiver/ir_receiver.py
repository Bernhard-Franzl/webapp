#!/usr/bin/python3 -u

import RPi.GPIO as GPIO
from time import ctime
import time
import os
import csv


def setup_mode(inpin_1, inpin_2):

	GPIO.setup(inpin_1, GPIO.IN)
	GPIO.setup(inpin_2, GPIO.IN)
	
	terminate = False
	while not terminate:
		
		val_1 = GPIO.input(inpin_1)
		val_2 = GPIO.input(inpin_2)

		print(val_1, val_2)
		time.sleep(0.01)


def process_sensor_value(sensor_value, sampling_rate, one_counter, zero_counter, possible_event, event_confirmed, event_one_count):
	
	if sensor_value == 1:
		one_counter += 1 
		
		if one_counter > (sampling_rate//20):
			possible_event = True
		
	else:
		zero_counter += 1
		
		if zero_counter >= (sampling_rate//2):
			
			zero_counter = 0
			
			if possible_event == True:
				possible_event = False

				if one_counter > (sampling_rate//10):
					event_confirmed = True
					event_one_count = one_counter

				else:
					event_confirmed = False
			
			one_counter = 0
					

			
	return one_counter, zero_counter, possible_event, event_confirmed, event_one_count

#def get_timestamp(time_client):
#	try:
#		response = time_client.request('pool.ntp.org')
#		timestamp = time.ctime(response.tx_time)
#	except:
#		timestamp = time.asctime(time.localtime())	
#	return timestamp
def reset_counters(counters):
	for i in range(len(counters)):
		counters[i] = 0
	return counters	
		
				
def detect_mode(inpin_1, inpin_2, outpin_1, outpin_2, sampling_rate, sys_args):
	
	print("detect mode")	
	sys.stdout.flush()

	# setup pins 
	GPIO.setup(inpin_1, GPIO.IN)
	GPIO.setup(inpin_2, GPIO.IN)
	
	GPIO.setup(outpin_1, GPIO.OUT)
	GPIO.setup(outpin_2, GPIO.OUT)

	# initialize some boolean variables
	possible_event_1, possible_event_2 = False, False
	event_confirmed_1, event_confirmed_2 = False, False
	discard_next = False
	
	# initiialize lots of counters
	event_one_counter_1, event_one_counter_2 = 0, 0
	one_counter_1, one_counter_2 = 0, 0
	zero_counter_1, zero_counter_2 = 0, 0
	entering_counter, leaving_counter = 0, 0
	in_counter, out_counter = 0, 0
	only_one, nothing_counter  = 0, 0
	
	while True:
		
		start = time.time()
		
		# read sensor values -> 1 means no connection, i.e. light interrupted
		val_1 = GPIO.input(inpin_1)
		val_2 = GPIO.input(inpin_2)
		
		GPIO.output(outpin_1, val_1)
		GPIO.output(outpin_2, val_2)
		
		# use sensor values to detect events, i.e. when a person interupts the lightgate
		one_counter_1, zero_counter_1, possible_event_1, event_confirmed_1, event_one_counter_1 = process_sensor_value(
			sensor_value = val_1,  
			sampling_rate = sampling_rate,
			one_counter = one_counter_1, 
			zero_counter = zero_counter_1, 
			possible_event = possible_event_1, 
			event_confirmed = event_confirmed_1,
			event_one_count = event_one_counter_1
		)

		one_counter_2, zero_counter_2, possible_event_2, event_confirmed_2, event_one_counter_2 = process_sensor_value(
			sensor_value = val_2,  
			sampling_rate = sampling_rate,
			one_counter = one_counter_2, 
			zero_counter = zero_counter_2, 
			possible_event = possible_event_2, 
			event_confirmed = event_confirmed_2,
			event_one_count = event_one_counter_2
		)
	
		#counter for walking direction
		if possible_event_1 and (not possible_event_2) and not (event_confirmed_1 or event_confirmed_2):
			in_counter += 1
			
		if possible_event_2 and not possible_event_1 and not (event_confirmed_1 or event_confirmed_2):
			out_counter += 1
		
		# some sanity checks to prevent bugs
		if (one_counter_1 >= sampling_rate*10) or (one_counter_2 >= sampling_rate*10):
			print(f"Too many ones at receiver. Please check system in {sys_args.roomname} at door {sys_args.doornumber}!")
			discard_next = True
			one_counter_1, one_counter_2, event_one_counter_1, event_one_counter_2 = 0, 0, 0, 0 
		
		# use event detection and walking direction to count leaving and entering people
		if event_confirmed_1 and event_confirmed_2:
			
			if discard_next:
				discard_next = False
				event_confirmed_1, event_confirmed_2 = False, False
				event_one_counter_1, event_one_counter_2, in_counter, out_counter, only_one, nothing_counter = 0, 0, 0, 0, 0, 0		
				
			else:
				timestamp = time.asctime(time.localtime())
				
				entering = (in_counter >= out_counter)
				if entering:
					message = "person is ENTERING"					
					entering_counter += 1
					
				else:
					message = "person is LEAVING"
					leaving_counter += 1
					
				print(message,"\n", timestamp)
				print()
				sys.stdout.flush()

				
				# write stats of the detected event to a file
				with open(f"data_{sys_args.roomname}/door{sys_args.doornumber}.csv", "a", newline="") as file:
					writer = csv.writer(file)
					writer.writerow([entering, timestamp, entering_counter, leaving_counter, in_counter, out_counter, event_one_counter_1, event_one_counter_2])

				event_confirmed_1, event_confirmed_2 = False, False
				event_one_counter_1, event_one_counter_2, in_counter, out_counter, only_one, nothing_counter = 0, 0, 0, 0, 0, 0  
			
		elif event_confirmed_1 and not event_confirmed_2:
			only_one += 1 
			if only_one >= sampling_rate:			
				event_confirmed_1 = False
				event_one_counter_1, event_one_counter_2, in_counter, out_counter, only_one, nothing_counter = 0, 0, 0, 0, 0, 0	
		
		elif event_confirmed_2 and not event_confirmed_1:
			only_one += 1 
			if only_one >= sampling_rate:			
				event_confirmed_2 = False
				event_one_counter_1, event_one_counter_2, in_counter, out_counter, only_one, nothing_counter = 0, 0, 0, 0, 0, 0	
				
		else:
			if not (possible_event_2 or possible_event_1):
				nothing_counter += 1
				
				if nothing_counter > sampling_rate:
					discard_next = False
					event_one_counter_1, event_one_counter_2, in_counter, out_counter, only_one, nothing_counter = 0, 0, 0, 0, 0, 0	
			
		sleep_time = 1/sampling_rate - time.time() + start
		
		if sleep_time > 0:
			time.sleep(sleep_time)
		else:
			continue


def main(args):
	
	inpin_1 = 25
	inpin_2 = 18
	
	sampling_rate = 100
	
	outpin_1 = 12
	outpin_2 = 23
	
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)
	
	# check if we are in setup mode or not
	if args.setup:
		setup_mode(inpin_1, inpin_2)
		
	else:	
		# check if data directory exists, if not create it
		if not os.path.isdir(f"data_{args.roomname}"):
			os.makedirs(f"data_{args.roomname}")
		
		# create a format.csv if not yet created
		if not os.path.isfile(f"data_{args.roomname}/format.csv"):
			with open(f"data_{args.roomname}/format.csv", "w", newline="") as file:
					writer = csv.writer(file)
					writer.writerow(["Entering", "Time", "People_IN", "People_OUT", "IN_Support_Count", "OUT_Support_Count", "One_Count_1", "One_Count_2"])
		

		# write special line in data csv-file to indicate new session
		with open(f"data_{args.roomname}/door{args.doornumber}.csv", "a", newline="") as file:
			writer = csv.writer(file)
			writer.writerow([2, time.asctime(time.localtime()), 0, 0, 0, 0, 0, 0])

		detect_mode(inpin_1, inpin_2, outpin_1, outpin_2, sampling_rate, args)
	
	return 0
			


if __name__ == "__main__":
	import sys
	import argparse
	
	parser =  argparse.ArgumentParser()
	parser.add_argument("-s", "--setup", action="store_true")
	parser.add_argument("-r", "--roomname", action="store", type=str , required=True)
	parser.add_argument("-d", "--doornumber", action="store", type=int , required=True, choices=range(1,10))
	args = parser.parse_args()
	
	sys.exit(main(args))
