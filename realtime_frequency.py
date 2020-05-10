import matplotlib.pyplot as plt
import numpy as np
import wave
import sys
import pyaudio
import queue

form_1 = pyaudio.paInt16 #16-bit resolution
chans = 1 # channels
samp_rate = 44100 # 44.1kHz sampling rate
chunk = 4096 # samples for buffer
record_secs = 3
downsample_factor = 24 # 8
real_rate = samp_rate/downsample_factor
dev_index = 2 #device index from print sound index script
# values to adjust for the signal to be processed quickly
#threshold = 1000 # this is for audio tests with my phone
threshold = 10000 # bike
min_distance = int(real_rate * 60 / 120) # we'll limit max within 120 rpm
start = 0

length_analysis = int(record_secs * samp_rate)
signal = b''

global int_queue

# find local max which are separated by a minimum distance
# optionally local max values need to be larger than a threshold
def find_local_max(s, min_distance = 0, threshold = 0, start = 0):
  p =start
  max_array = []
  while p < len(s):
    if s[p] > threshold:
      if s[p] > s[p-1] and s[p] >= s[p+1]:
        max_array.append([p,s[p]])
        p += min_distance
        print('max found!' + str(p))
    p += 1
  return max_array
    
def callback(in_data, frame_count, time_info, status):
  # print('lengthdata ' + str(len(in_data)))
  # it receives two chunks, we need to concatenate several to do the analysis
  prepareInput(in_data)
  return (None, pyaudio.paContinue)

def prepareInput(in_data):
  global signal
  a = signal + in_data 
  signal = a
  b = np.fromstring(a, "Int16")
  #print('length b ' + str(len(b)))
  # check that we already have the required size
  if(len(b) > length_analysis):
    processSignal(b)
    signal = b''

def compute_rpm(max_values):
  rpm_acc = 0
  intervals = 0
  print('compute rpm')
  for m in range(len(max_values)-1):
    print('computing peaks')
    distance = max_values[m+1][0] - max_values[m][0]
    #print('distance ' + str(distance) + str(type(distance)))
    rpm_acc += int(60 * real_rate / distance)
    #print('rpm_acc ' + str(rpm_acc) + str(type(rpm_acc)))
    intervals += 1   
  if intervals > 0:
    rpm = int(rpm_acc/intervals)
  else:
    rpm = 0
  global int_queue
  int_queue.put(rpm)
  return rpm  

#def serveRpm():
  #print('Returning rpm ' + str(rpm))
  #return rpm

def processSignal(trololo):
  #global rpm
  print('length trololo ' + str(len(trololo)))
  # downsample
  a = np.array(trololo)
  b = a[::downsample_factor]
  max_values = find_local_max(b, int(min_distance), threshold)
  print('max donwsampled')
  print(max_values)
  rpm = compute_rpm(max_values)
  print('RPM '+str(rpm))
  return
  


def main(stop = None, ext_queue = None):
  audio = pyaudio.PyAudio() # create pyaudio instantiation
  stream = audio.open(format = form_1, rate = samp_rate, channels = chans, input_device_index = dev_index, input = True, frames_per_buffer = chunk, stream_callback = callback)
  global int_queue
  if ext_queue:
    int_queue = ext_queue
    print("Using external queue")
  else:
    int_queue = queue.Queue()
    print("Using internal queue")
  print("recording")
  try: 
    while True:
      if stop:
        if stop():
          break
  except KeyboardInterrupt:
    pass
  print("finished recording")
  stream.stop_stream()
  stream.close()
  audio.terminate()
  return

if __name__ == "__main__":
  main()
  

