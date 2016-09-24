# Read in a WAV and find the freq's
import pyaudio
import wave
import numpy as np

from math import log2, pow

A4 = 440
C0 = A4*pow(2, -4.75)
name = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

#this takes in an int and makes string note value
def pitch(freq):
    # freq = int(freq)
    h = round(12*log2(freq/C0))
    octave = h // 12
    n = h % 12
    return name[n] + str(octave)


chunk = 2048

# open up a wave
file_name = input("What is the file name? ?!?!?!?!?cos0!!!!!!  ")
# wf = wave.open('sandstorm.wav', 'rb')
wf = wave.open(file_name, 'rb')


# sample width in bytes
swidth = wf.getsampwidth()

# get the sampling frequency
RATE = wf.getframerate()

# use a Blackman window
window = np.blackman(chunk)

# instantiate pyaudio
p = pyaudio.PyAudio()

# open stream
stream = p.open(format =
                p.get_format_from_width(wf.getsampwidth()),
                channels = wf.getnchannels(),
                rate = RATE,
                output = True)

# read some data
data = wf.readframes(chunk)


# play stream and find the frequency of each chunk
print("before loop")

# truncate the fucking data stream
if len(data) != chunk*swidth:
    data = data[:chunk*swidth-len(data)]

while len(data) == chunk*swidth: # THIS ONE S:LKFJSDFKSDFLKKJSD:FKLSJ :(

    print("loop start loop ")
    # write data out to the audio stream
    stream.write(data)
    # unpack the data and times by the hamming window
    # indata = np.array(wave.struct.unpack("%dh"%(len(data)/swidth),\
    #                                      data))*window

    indata = np.array(wave.struct.unpack("%dh"%(chunk),\
                                         data))*window


    # Take the fft and square each value
    fftData=abs(np.fft.rfft(indata))**2
    # find the maximum
    which = fftData[1:].argmax() + 1
    # use quadratic interpolation around the max
    if which != len(fftData)-1:
        y0,y1,y2 = np.log(fftData[which-1:which+2:])
        x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)


        # find the frequency and output it
        thefreq = ((which+x1)*RATE/chunk)
        print("The freq is %f Hz" % (thefreq))
        print("The note is %s" % pitch(thefreq))
    else:
        thefreq = (which*RATE/chunk)
        print("The freq is %s Hz." % (thefreq))
        print("The note is %s" % pitch(thefreq))

    # read some more data
    data = wf.readframes(chunk)
    while len(data) != chunk*swidth:
        data = data[:chunk*swidth-len(data)]

if data:
    stream.write(data)

# stop the stream
stream.close()
# close pyaudio
p.terminate()
