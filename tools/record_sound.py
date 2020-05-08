import pyaudio
import wave

form_1 = pyaudio.paInt16 #16-bit resolution
chans = 1 # channels
samp_rate = 44100 # 44.1kHz sampling rate
chunk = 4096 # samples for buffer
record_secs = 10 # seconds to record
dev_index = 2 #device index from print sound index script
wav_output_filename = 'real_bike.wav'

audio = pyaudio.PyAudio() # create pyaudio instantiation

stream = audio.open(format = form_1, rate = samp_rate, channels = chans, input_device_index = dev_index, input = True, frames_per_buffer = chunk)

print("recording")
frames = []

for ii in range(0,int((samp_rate/chunk)*record_secs)):
  data = stream.read(chunk)
  frames.append(data)

print("finished recording")

stream.stop_stream()
stream.close()
audio.terminate()

wavefile = wave.open(wav_output_filename, 'wb')
wavefile.setnchannels(chans)
wavefile.setsampwidth(audio.get_sample_size(form_1))
wavefile.setframerate(samp_rate)
wavefile.writeframes(b''.join(frames))
wavefile.close()