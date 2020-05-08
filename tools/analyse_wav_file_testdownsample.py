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

downsample_factor = 2
#test downsample
a = np.array(signal)
b = a[::downsample_factor]
print('length signal '+str(len(signal)))
print('length downsampled signal ' + str(len(b)))


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
    
threshold = 1500
min_distance = 50000
start = 100000
max_values1 = find_local_max(signal, min_distance, threshold, start)
print('max original size')
print(max_values1)


max_values2 = find_local_max(b, int(min_distance/downsample_factor), threshold, int(start/downsample_factor))
print('max donwsampled')
print(max_values2)

plt.figure(1)
plt.title("Signal wave ...")
plt.plot(signal)

plt.figure(2)
plt.title("Signal wave downsampled...")
plt.plot(b)

plt.show()