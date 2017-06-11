import cl
import glob
import scipy
import time
import wave
import yaml


#-----------------------------------------------------------------------------#

def Load_Voice_Files():
	AudioFiles = {}
	dir_name = '../data/Joes_voice_wav/'
	filenames = glob.glob('{}*.wav'.format(dir_name))

	for fname in filenames:
		AudioFiles[fname[len(dir_name):-4]] = fname

	return AudioFiles


def Load_Word_Pronounciations():
	fname = '../data/dictionary/dictionary.yml'
	with open(fname) as f:
		Pronounciation = yaml.load(f)
	return Pronounciation


def GetPhenomeFiles(words,AudioFiles,Pronounciation):
	''' gets the files associalted with the phenomes representing the words in the string given '''
	phenome_files = []

	for word in words:
		word = word.upper()

		# get the pronounciation 
		try:
			phenomes = Pronounciation[word]
		except:
			print 'Word not in dictionary.'
			break
 
		# get the audio files for eaeh phenome 
		for phenome in phenomes:
			try: 
				phenome_files.append(AudioFiles[phenome])
			except:
				print 'Phenome (%s) not in audio files.' % phenome

		# add a pause between words
		try:
			phenome_files.append(AudioFiles['PAUSE2'])
		except:
			print 'PAUSE2 file not recognized.'

	return phenome_files

def GetParams(phenome_files):
	''' returns the parameters of the audio file; adds up the total number of frames '''
	# get the parameters
	# params = (Nchannels, samplewidth, framerate, nframes, comptype, compname)
	Nframes = 0
	n = 0
	for fname in phenome_files:
		w = wave.open(fname, 'rb')
		Nframes += w.getnframes()

		if n == 0:
			params = list(w.getparams())
			n += 1

		w.close()

	# update the total number of frames and the speed up the frame rate
	params[2] = params[2]*1.05
	params[3] = Nframes

	return tuple(params)


def WriteAudioFile(params,phenome_files,ofile):
	# generate the output file
	wout = wave.open(ofile,'wb')
	wout.setparams(params)

	for fname in phenome_files:
		w = wave.open(fname, 'rb')
		wout.writeframes(w.readframes(w.getnframes()))
		w.close()

	wout.close()


def Generate_OutputFile(string,AudioFiles,Pronounciation,ofile):
	words = string.strip().split()

	''' think to optimize the list structure '''

	phenome_files = GetPhenomeFiles(words,AudioFiles,Pronounciation)

	params = GetParams(phenome_files)

	WriteAudioFile(params,phenome_files,ofile)


#-----------------------------------------------------------------------------#

AudioFiles = Load_Voice_Files()
Pronounciation = Load_Word_Pronounciations()

string = raw_input('Give a statement: ')
ofile = 'audio.wav'

t0 = time.time()
Generate_OutputFile(string,AudioFiles,Pronounciation,ofile)
print 'Time elapsed = %.2f seconds.' % (time.time() - t0)
