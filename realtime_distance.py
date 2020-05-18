import RPi.GPIO as GPIO
import time
import queue

# GPIO pin connected to the trigger for the sensor (HC-SR04)
TRIG = 23
# GPIO connected to ECHO (output of the sensor)
ECHO = 24
# List to store values and compute the mean
raw_values = []
#size of values over which to compute the range
MEAN_RANGE = 10 

# Set up the pin numbering scheme BCM (Broadcom SOC channel), pin numbers
# GPIO (General-Purpose Input/Output)
GPIO.setmode(GPIO.BCM)
# Set up TRIG as an output channel 
GPIO.setup(TRIG, GPIO.OUT)
# Set up ECHO as an input channel
GPIO.setup(ECHO, GPIO.IN)
# Variable to store the distance measures in a queue to be consumed by a webservice
global int_queue_dist

def measure_distance():
  global int_queue_dist
  global raw_values
  # Shut down the activator pin and stabilise for some seconds
  GPIO.output(TRIG, GPIO.LOW)
  print("DIST: waiting for the sensor to stabilise")
  time.sleep(2)

  # Turn on the activator pin for 10 microseconds and shut it down
  GPIO.output(TRIG, GPIO.HIGH)
  time.sleep(0.00001)
  GPIO.output(TRIG, GPIO.LOW)

  # The sensor sends 8 ultrasonic pulses at 40kHz and puts the ECHO output to HIGH.
  # This is the moment to start measuring the time.
  print("DIST: starting echo")
  while True:
    pulse_start = time.time()
    if GPIO.input(ECHO) == GPIO.HIGH:
      break

  # The ECHO output will be in HIGH until echo is received. 
  # Once that happens ECHO will switch to LOW and we have to stop the time measure. 
  while True:
    pulse_end = time.time()
    if GPIO.input(ECHO) == GPIO.LOW:
      break

  # Time measure in seconds.
  duration = pulse_end - pulse_start

  # Measure the distance using the sound speed
  # Also take into account that the measure includes the sound rountrip
  distance = (34300 * duration) / 2

  # Print result of single measure.
  print ("Distance - %.2f cm" % distance)

  # Add measure to list
  raw_values.append(distance)

  if len(raw_values)==MEAN_RANGE:
    acc_distance = sum(raw_values)/len(raw_values)
    print("DIST: Mean distance - "+ str(acc_distance))
    int_queue_dist.put(acc_distance)
    raw_values = []
  else:
    pass




def main(stop = None, ext_queue = None):
  global int_queue_dist
  if ext_queue:
    int_queue_dist = ext_queue
    print("DIST: Using external queue")
  else:
    int_queue_dist = queue.Queue()
    print("DIST: Using internal queue")
  print("DIST: Start measuring distance")
  try: 
    while True:
      measure_distance()
      if stop:
        if stop():
          break
  except KeyboardInterrupt:
    pass
  print("DIST: finished distance measuring")
  # Restart all GPIO channels.
  GPIO.cleanup()
  return

if __name__ == "__main__":
  main()
  
