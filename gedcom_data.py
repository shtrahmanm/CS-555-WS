import sys
from pathlib import Path
valid_tags={"INDI", "NAME", "SEX", "BIRT", "DEAT", "FAMC", "FAMS", "FAM", "MARR", "HUSB", "WIFE", "CHIL",
 "DIV", "DATE", "HEAD", "TRLR", "NOTE"}
if (len(sys.argv)!=2 ):
    sys.exit("Usage: gedcom_data.py <filename>")
my_file = Path(sys.argv[1])
if not (my_file.is_file()):
    sys.exit("File does not exist")
file1 = open(sys.argv[1], 'r')
Lines = file1.readlines() 
file1 = open("Output.txt","w")
for line in Lines:
    words = line.strip().split()
    level = words[0]
    tag = words[1]
    #check for validity
    valid ='N'
    length = len(level)+len(tag)+2
    if(tag in valid_tags):
        valid = 'Y'
    
    if((valid=='N' and len(words)>2) and words[2] in valid_tags):
        id=words[1]
        valid = 'Y'
        tag=words[2]
        file1.write("--> {}\n".format(line.strip()))
        file1.write("<-- {}|{}|{}|{}\n".format(level, tag, valid, id))
    else:
        file1.write("--> {}\n".format(line.strip()))
        file1.write("<-- {}|{}|{}|{}\n".format(level, tag, valid, line.strip()[length:]))
file1.close()