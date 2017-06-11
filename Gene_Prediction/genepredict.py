#Purpose: determine the long ORFs in Saccharomyces cerevisia
#Joe Burg

import sys
import numpy as np
import time

############################################################################
#Program inputs

if len(sys.argv) < 3:
    print 'Usage:'
    print '  %s <input file> <output file> [min ORF length (default = 100)]'\
          % sys.argv[0]
    exit()
elif len(sys.argv) ==  3:
    inputfile = sys.argv[1]
    outputfile = sys.argv[2]
    cutoff = 100
else:
    inputfile = sys.argv[1]
    outputfile = sys.argv[2]
    cutoff = int(sys.argv[3])

start_time = time.time()

start_codon = 'ATG'
end_codon = ['TGA','TAA','TAG']

print "Input sequence file: %s" % inputfile
print "Output file for ORF data: %s" % outputfile
print "Minimum length for ORF: %s" % cutoff
print "Start codon: %s" % start_codon
print "Stop codon(s):"

for i in range(len(end_codon)):
    print "  %s" % end_codon[i]

############################################################################
#program functions

def find_start(sequence,start_codon,start_index,mod):
    start = start_index
    while True:
        #find the first start index
        start = sequence.find(start_codon,start)
        if start == -1:
            return start
        #if the start index has the same mod as the reading frame
        #then return the index; if not, continue search at next index
        elif start % 3 == mod:
            return start
        else:
            #there wont be another start codon in the next 2 indicies
            #so start at the third
            start += 3

def find_stop(sequence,end_codon,start_index,mod):
    for codon in end_codon:
        while True:
            #start searching for end codon after the start index
            #same logic applies for end codon acceptance as in find_start()
            #with the exception that there are 3 possible end codons
            end = sequence.find(codon,start_index+1)
            if end == -1:
                break
            elif end % 3 == mod:
                return end
            else:
                #start+1 is built into the find() method above so only
                #increase by 2                
                start_index = end + 2              

    return end

def find_ORFs(sequence,start_codon,end_codon):
    ORFs = []
    #loop over the 3 reading frame and search for the start and stop
    #codons using their respective functions (codons will be in the
    #correct reading frame / mod from functions)
    for i in range(3):
        start = i
        while True:
            start = find_start(sequence,start_codon,start,i)
            if start == -1:
                break
            else:
                end = find_stop(sequence,end_codon,start+1,i)
                if end == -1:
                    break
                else:
                    #indicies offset by 1 (plus 2 more for end codon)
                    end += 3
                    start += 1
                    L_ORF = (end - start + 1)/3
                    ORFs.append([i+1,start,end,L_ORF])
                    #begin new search for ORF after end codon -1 to
                    #translate back to 0->N-1 indicies
                    start = end - 1
    return ORFs

def process_seq(N_seq,sequence,start_codon,end_codon,N_ORFs_tot):
    filename_out.write('>Sequence %s\n' % N_seq)
    print '\nSequence %s:' % N_seq
    print '  %s base pairs' % len(sequence)

    #find the ORFs using the find_ORFs() function
    ORFs = find_ORFs(sequence,start_codon,end_codon)

    #print statistics to screen and write ORF data to output file 
    ORF_list = []
    N_ORFs = 0
    for ORF in ORFs:
        #only accept ORFs with lengths larger than the cutoff
        if len(ORF) > 0 and ORF[3] >= cutoff:
            N_ORFs += 1
            N_ORFs_tot += 1
            ORF_list.append(ORF[3])
            filename_out.write('%s %s %s %s\n' %(ORF[0],ORF[1],\
                                                 ORF[2],ORF[3]))
            
    if len(ORF_list)>0:    
        min_ORF = min(ORF_list)
        avg_ORF = np.mean(ORF_list)
        max_ORF = max(ORF_list)
    else:
        [min_ORF,avg_ORF,max_ORF] = [0,0.0,0]
                    
    print '  %s ORF(s)' % N_ORFs
    print '  min/max/avg ORF length: %s/%s/%s codon(s)' \
          %(min_ORF,avg_ORF,max_ORF)

    return N_ORFs_tot

############################################################################
#main program

filename_in = open(inputfile)
filename_out = open(outputfile, 'w')
filename_out.write('>ORF data for file %s\n' % inputfile)

N_seq = 0
N_ORFs_tot = 0
sequence = ''
for line in filename_in:
    line = line.strip()
    
    #new sequences are indicated by '>'
    if line[0] == '>':
        #first new sequence indicator does not have any sequence
        #associated with it so don't process it
        if len(sequence) > 0:
            N_seq += 1
            N_ORFs_tot = process_seq(N_seq,sequence,start_codon,\
                                  end_codon,N_ORFs_tot)

            #reset sequence
            sequence = ''
    else:
        #build the sequence as a single string
        sequence += line           

filename_in.close()

#Process the last sequence (due to no end '>')
N_seq += 1
N_ORFs_tot = process_seq(N_seq,sequence,start_codon,end_codon,N_ORFs_tot)
filename_out.close()

time_elapsed = time.time() - start_time
print '\nProcessed %s sequence(s) and found %s ORF(s)' %(N_seq, N_ORFs_tot)
print 'Elapsed time %s seconds' % time_elapsed
