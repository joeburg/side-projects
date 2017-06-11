import cl
import glob
import scipy
import wave




fname1 = '../data/Joes_voice_wav/M.wav'
fname2 = '../data/Joes_voice_wav/AA1.wav'
fname3 = '../data/Joes_voice_wav/N.wav'
ofile = 'test.wav'


files = [fname1, fname2, fname3]

# get the parameters
# params = (Nchannels, samplewidth, framerate, nframes, comptype, compname)
Nframes = 0
n = 0
for fname in files:
	w = wave.open(fname, 'rb')
	Nframes += w.getnframes()

	if n == 0:
		params = list(w.getparams())
		n += 1

	w.close()

# update the total number of frames and the speed up the frame rate
params[2] = params[2]*1
params[3] = Nframes
params = tuple(params)

# generate the output file
wout = wave.open(ofile,'wb')
wout.setparams(params)
for fname in files:
	w = wave.open(fname, 'rb')
	wout.writeframes(w.readframes(w.getnframes()))
	w.close()

wout.close()

# print Nframes

# f = wave.open(fname,'r')
# f.readframes(f.getnframes())
# f.close()