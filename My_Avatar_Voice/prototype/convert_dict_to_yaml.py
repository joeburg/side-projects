
fname = '../data/cmu_files/cmudict_words.txt'
fin = open(fname,'r')
fout = open('dictionary.yml', 'w')

while True:
	fields = fin.readline().strip().split()
	if fields[0]:
		key = fields[0]
		phemones = fields[1:]

		fout.write('%s: [' % key)
		for i in range(len(phemones)):
			if i == 0:
				fout.write('%s' %phemones[i])
			else:
				fout.write(', %s' %phemones[i])
		fout.write(']\n')

	else:
		print 'All done!'
		break

fin.close()
fout.close()

