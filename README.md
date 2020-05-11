# bikeproject
Reads speed and break info from BH stay-at-home bike

## requirements

`> sudo apt-get install libportaudio0 libportaudio2 libportaudiocpp0 portaudio19-dev`

`> sudo pip3 install pyaudio`

`> pip3 install mathplotlib`

## tools

* `print_sound_index`: you need to run this script to know the USB index in which the sound input is plugged. This sound index needs to be updated in the `record_sound` and `realtime_frequency` scripts.
* `record_sound`: modify the name of the file in the script and update the dev_index according to the previous script. It records a 10' wav file.
* `plot_wav_file`: as the name says.
* `analyse_wav_file_testdownsample` & `analyse_wav_file_testrpm` test the algorithms for downsampling and computing the rpm according to the peaks found. Some parameters would need to be adjusted to the signal (plot_wav_file helps) such as:
  * threshold (in volume): the threshold level for the peak to detect
  * distance (in samples): minimum distance between peaks to detect - required to speed up the algorithm - it is computed as samples_per_second*1/max_rpm*60seconds
  * downsample factor: from a 44.1kHz signal the samples per second are divided by this factor - make a few tests with the files above to make sure you keep the samples to analyse to a minimum without missing any peak in the signal.
  * start (in seconds): in case there is a delay from the start of the recording and the start of the signal to analyse.
  
### Helpers for passthrough test

* `real_bike.wav` is a recording of the bike sensor signal (for computing RPM)
* `real_bike_passthrough.wav` is a recording of the previous signal, once passed through the raspberry (play wav file, output to jack, and record it back from USB mic input)
* `passthrough_test.py` records input from USB mic
* `play_sound.py` plays a wav file and outputs it to the jack

The passthrough recording was done by connecting the jack audio output to the USB mic input, then starting the `passthrough_test.py` to start recording from USB mic input, and then running the `play_sound.py` script with the original `real_bike.wav` signal to play the sound in the jack output.
  
 ## RPM computation
 
 The `realtime_frequency` script takes an audio input (assumed to be composed of regular peaks) and computes their frequency in rpm in a 3s window.
 Settings such as `dev_index`, `distance`, `threshold` or `downsample factor` detailed in Tools apply here and they have to be adapted to the signal to measure.

## Webservice

Start `server.py` in a chosen port, for example: `> python3 server.py 8081` 
* *Start* starts measuring the RPMs
* *Stop* stops the measurement
