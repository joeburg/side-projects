import glob
import os

def audio_convert(aifc_file, wav_file):
	os.system("afconvert -f 'WAVE' -c 2 -d I16@44100 {} {}".format(aifc_file, wav_file))


# grab all the .aifc files
dir_name_in = '../data/Joes_voice_aifc/'
dir_name_out = '../data/Joes_voice_wav/'

files = glob.glob('{}*.aifc'.format(dir_name_in))

# convert each .afic file to .wav file
for fin in files:
	fout = '{}{}.wav'.format(dir_name_out,fin[len(dir_name_in):-5])
	audio_convert(fin, fout)
