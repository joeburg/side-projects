# This short program creates a file with the random numbers used in the
# main molecular dynamics code.

import random
random.seed(1)

f = open("random.txt", "w")
for n in range(200):
  f.write("%.60e\n" % random.random())
f.close()
