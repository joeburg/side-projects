#Purpose: given a movie, find another movie that is most similar to it
#Joe Burg

import sys
import time
import math
import collections

############################################################################
#Program inputs

if len(sys.argv) < 3:
    print 'Usage:'
    print '  %s <MovieLens file> <similarities file> [user thresh (default = 5)]'\
          % sys.argv[0]
    exit()
elif len(sys.argv) ==  3:
    inputfile = sys.argv[1]
    outputfile = sys.argv[2]
    threshold = 5
else:
    inputfile = sys.argv[1]
    outputfile = sys.argv[2]
    threshold = int(sys.argv[3])

t0 = time.time()

print 'Input MovieLens file: %s' % inputfile
print 'Output file for similarity data: %s' % outputfile
print 'Minimum number of common users: %s' % threshold

############################################################################
#program functions

def avg_rating(user):
    tot = 0 
    for movie in user:
        tot += user[movie]
    return tot/float(len(user))

def compute_similarity(movie1,movie2,common_users,users,user_avg):
    numerator = 0
    denominatorA = 0
    denominatorB = 0
    for user in common_users:
        #for each user in common between the 2 movies, compute the
        #similarity coeff
        a = (users[user][movie1] - user_avg[user])
        b = (users[user][movie2] - user_avg[user])
        numerator += a*b
        denominatorA += a**2
        denominatorB += b**2

    #to ensure no division by 0, set S to 0 if either denominator
    #component is 0 (numerator should be 0 in these cases)
    if denominatorA == 0 or denominatorB == 0:
        return 0
    else:
        return numerator / math.sqrt(denominatorA * denominatorB)

def find_max_S(S_scores):
    #initialize the max S coeff
    S_max = S_scores[0][1]
    S_max_index = 0
    for i in range(len(S_scores)):
        #if a coeff is larger then make it the new max S coeff
        if S_scores[i][1] > S_max:
            S_max = S_scores[i][1]
            S_max_index = i
    return S_scores[S_max_index]
        
############################################################################
#main program

#create data structures
#movies = {movieID: set([userID])}
#users = {userID : {movieID : rating}}
#user_avg = {userID: avg_rating}
                   
file_in = open(inputfile)
users = {}
movies = {}
N_lines = 0
for line in file_in:
    N_lines += 1
    line = line.strip().split()
    
    #change str to ints so dictionaries can be sorted and so
    #ratings can be used to calculate similarity coefficients
    line = map(int,line)

    #create movies data structure
    if not movies.has_key(line[1]):
        movies[line[1]] = set([])
        movies[line[1]].add(line[0])
    else:
        movies[line[1]].add(line[0])

    #create users data structure 
    if not users.has_key(line[0]):
        users[line[0]] = {}
        users[line[0]][line[1]] = line[2]
    else:
        users[line[0]][line[1]] = line[2]
file_in.close()

N_users = len(users)
N_movies = len(movies)

#sort movie IDs so they can be written out in increasing order
movies = collections.OrderedDict(sorted(movies.items()))

#find average rating for each user and put in user_avg dictionary
user_avg = {}
for user in users:
    user_avg[user] = avg_rating(users[user])

#compute similarities for each movie and write out the most similar
file_out = open(outputfile, 'w')
for movie1 in movies:
    S_scores = []
    for movie2 in movies:
        #don't compare the same movie
        if movie1 != movie2:
            #take intersection of users who rated each movie and
            #ensure it's larger than the threshold before computing
            #the similarity coefficent 
            common_users = movies[movie1] & movies[movie2]
            if len(common_users) > threshold:
                S = compute_similarity(movie1,movie2,common_users,users,user_avg)
                S_scores.append([movie2,S,len(common_users)])

    #find the largest similarity coeff given each coeff in the S_scores list            
    if len(S_scores) > 0:
        S_max = find_max_S(S_scores)
        file_out.write('%s (%s,%.2f,%s)\n' \
                       %(movie1,S_max[0],S_max[1],S_max[2]))
    else:
        file_out.write('%s\n' % movie1)

file_out.close()

print '\nRead %s lines with a total of %s movies and %s users' \
      % (N_lines,N_movies,N_users)

t1 = time.time()
print '\nComputed similarities in %.3f seconds' % (t1-t0)
