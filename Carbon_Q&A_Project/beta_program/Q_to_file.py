#Purpose: turn question into .txt file for archive and parsing 
#Joe Burg

def Q_to_file(question,Qnumber):

    Qfile = Qnumber+'.txt'
    
    dataFile = open(Qfile, 'w')
    dataFile.write(question)
    dataFile.close() 

    return Qfile
        
