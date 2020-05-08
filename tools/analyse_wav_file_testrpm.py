import matplotlib.pyplot as plt
import numpy as np
import wave
import sys

spf = wave.open(sys.argv[1], 'rb')

signal = spf.readframes(-1)
signal = np.fromstring(signal, "Int16")

if spf.getnchannels() == 2:
  print("Just mono files")
  sys.exit(0)



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

def compute_rpm(max_values):
  rpm_acc = 0
  intervals = 0
  print('compute rpm')
  for m in range(len(max_values)-1):
    print('computing peaks')
    distance = max_values[m+1][0] - max_values[m][0]
    print('distance ' + str(distance) + str(type(distance)))
    rpm_acc += int(60 * real_rate / distance)
    print('rpm_acc ' + str(rpm_acc) + str(type(rpm_acc)))
    intervals += 1   
  return int(rpm_acc/intervals)

samp_rate = 44100 # 44.1kHz sampling rate
downsample_factor = 4
real_rate = samp_rate/downsample_factor    
threshold = 1000
min_distance = int(real_rate * 60 / 120) # we'll limit max within 120 rpm
start = 0
#max_values1 = find_local_max(signal, min_distance, threshold, start)
#print('max original size')
#print(max_values1)

a = np.array(signal)
b = a[::downsample_factor]
print('length signal '+str(len(signal)))
print('length downsampled signal ' + str(len(b)))



max_values2 = find_local_max(b, int(min_distance), threshold)
print('max donwsampled')
print(max_values2)

rpm = compute_rpm(max_values2)
print('RPM '+str(rpm))





plt.figure(1)
plt.title("Signal wave ...")
plt.plot(signal)

plt.figure(2)
plt.title("Signal wave downsampled...")
plt.plot(b)

plt.show()