from django.http import HttpResponse

# freq stuff
import pyaudio
import wave
import numpy as np

from math import log2, pow

# file stuff
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

# from mysite.models import Document
# from mysite.forms import DocumentForm



def hello(request):
    return HttpResponse("Hello world")


def freq(request):

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

    if data:
        stream.write(data)

    # stop the stream
    stream.close()
    # close pyaudio
    p.terminate()

    return HttpResponse("freq - WEb aPP")

#
# def list(request):
#     # Handle file upload
#     if request.method == 'POST':
#         form = DocumentForm(request.POST, request.FILES)
#         if form.is_valid():
#             newdoc = Document(docfile=request.FILES['docfile'])
#             newdoc.save()
#
#             # Redirect to the document list after POST
#             return HttpResponseRedirect(reverse('list'))
#     else:
#         form = DocumentForm()  # A empty, unbound form
#
#     # Load documents for the list page
#     documents = Document.objects.all()
#
#     # Render list page with the documents and the form
#     return render(
#         request,
#         'list.html',
#         {'documents': documents, 'form': form}
#     )
