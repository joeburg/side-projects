
import sys
#------------------------------------------------------------------------#


if len(sys.argv) < 2:
	print 'Usage:'
	print '  python %s <email file>' %sys.argv[0]
	exit()

email_file = sys.argv[1]
clean_file = 'clean_CL_emails.txt'


emails = set([])
f = open(email_file)
fc = open(clean_file,'w')
for line in f:
	fields = line.strip().split()
	email = fields[0]

	if email not in emails:
		emails.add(email)

		if len(fields) > 1:
			phone = fields[1]
			# fc.write('%s    %s\n' %(email,phone))
		else:
			fc.write('%s\n'%email)

f.close()
fc.close()
print 'Number of unique emails: %d' %len(emails)