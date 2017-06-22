# program to join two text documents for processing

f1 = open('DailyStar_articles_(2003_2007)_(2013_2015)_data.txt')
f2 = open('DailyStar_articles_2008_20012_data.txt')
fo = open('DailyStar_all_data.txt', 'w')
for line in f1:
	fo.write(line)

for line in f2:
	fo.write(line)

f1.close()
f2.close()
fo.close()