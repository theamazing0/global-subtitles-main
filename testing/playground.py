# import sounddevice as sd
# import numpy

# fs = 48000

# sd.default.samplerate = fs
# sd.default.channels = 2

# duration = 10.5  # seconds
# myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=2)

# sd.wait()

# sd.play(myrecording, fs)

from scipy.io.wavfile import wavWrite
import sounddevice as REC

# Recording properties
SAMPLE_RATE = 44100
SECONDS = 10

# Channels
MONO    = 1
STEREO  = 2

# Command to get all devices listed: py -m sounddevice 
# Device you want to record
REC.default.device = 'VoiceMeeter VAIO3 Output (VB-Audio VoiceMeeter VAIO3), Windows DirectSound'

print(f'Recording for {SECONDS} seconds')

# Starts recording
recording = REC.rec( int(SECONDS * SAMPLE_RATE), samplerate = SAMPLE_RATE, channels = MONO)
REC.wait()  # Waits for recording to finish

# Writes recorded data in to the wave file
wavWrite('recording.wav', SAMPLE_RATE, recording)