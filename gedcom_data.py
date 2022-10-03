from ast import Div
from asyncio.unix_events import BaseChildWatcher
from asyncore import write
from distutils.debug import DEBUG
import sys
from pathlib import Path
from telnetlib import SE
import datetime
from prettytable import PrettyTable

#Define Tables in Output.txt
Individuals = PrettyTable()
Families = PrettyTable()
#Dictionary for gedcom tags
valid_tags = {
  "INDI", "NAME", "SEX", "BIRT", "DEAT", "FAMC", "FAMS", "FAM", "MARR", "HUSB",
  "WIFE", "CHIL", "DIV", "DATE", "HEAD", "TRLR", "NOTE"
}
#Dictionary for converting gedcom months to ints
months = {
  "JAN": 1,
  "FEB": 2,
  "MAR": 3,
  "APR": 4,
  "MAY": 5,
  "JUN": 6,
  "JUL": 7,
  "AUG": 8,
  "SEP": 9,
  "OCT": 10,
  "NOV": 11,
  "DEC": 12
}

#Function to convert gedcom date into useable format
#date = "day month(first 3 letters of month) year" -> return list of ints [day, month, year]
class Date:
   def __init__(self, date):
    list = date.split()
    self.day = int(list[0])
    self.year = months[list[1]]
    self.month = int(list[2])

#Check command line arguments
if (len(sys.argv) != 2):
  sys.exit("Usage: gedcom_data.py <filename>")
#Check if file exists
my_file = Path(sys.argv[1])
if not (my_file.is_file()):
  sys.exit("File does not exist")
#Open file and begin reading line by line, also opens output file to write into
file1 = open(sys.argv[1], 'r')
Lines = file1.readlines()
file1 = open("Output.txt", "w")

#lists of individual data
idi = []
Name = []
Gender = []
Birthday = []
Age = []
Alive = []
Death = []
Child = []
Spouse = []

#lists of family data
idf = []
Married = []
Divorced = []
Husband_ID = []
Husband_Name = []
Wife_ID = []
Wife_Name = []
Children = []

#Temp variable to tell if DATE tag is for birth, death date, marriage, etc...
birth = 0
death = 0
marry = 0
divorce = 0

#Begin iterating line by line
for line in Lines:
  words = line.strip().split()
  level = words[0]
  tag = words[1]
  #check for validity
  valid = 'N'
  length = len(level) + len(tag) + 2
  if (tag in valid_tags):
    valid = 'Y'
  if ((valid == 'N' and len(words) > 2) and words[2] in valid_tags):
    id = words[1]
    valid = 'Y'
    tag = words[2]
  #Only valid tags are relevant to table
  if valid=='Y':  
  #Check for individual table info
    if (tag == "INDI"):
        idi.append(id)
        Alive.append("True")
        Death.append("N/A")
        Child.append("N/A")
        Spouse.append("N/A")
    if (tag == "NAME" and level == "1"):
        Name.append(line.strip()[length:])
    if (tag == "SEX"):
        Gender.append(line.strip()[length:])
    if (tag == "BIRT"):
        birth = 1
    if (tag == "DATE"):
        if (birth):
            Birthday.append(line.strip()[length:])
            date = Birthday[len(Birthday) - 1].split()
            day = int(date[0])
            month = months[date[1]]
            year = int(date[2])
            today = datetime.datetime.now()
            Age.append(today.year - year - ((today.month, today.day) < (month, day)))
            birth = 0
        if (death):
            Death[len(Alive) - 1] = line.strip()[length:]
            death = 0
    if (tag == "DEAT"):
        Alive[len(Alive) - 1] = "False"
        death = 1
    if (tag == "FAMC"):
        Child[len(Child) - 1] = line.strip()[length:]
    if (tag == "FAMS"):
        Spouse[len(Spouse) - 1] = line.strip()[length:]
    #Check for Family table info
    if (tag == "FAM"):
        idf.append(id)
        Married.append("N/A")
        Divorced.append("N/A")
        Husband_ID.append("N/A")
        Husband_Name.append("N/A")
        Wife_ID.append("N/A")
        Wife_Name.append("N/A")
        Children.append("N/A")
    if (marry):
        Married[len(Married) - 1] = line.strip()[length:]
        marry = 0
    if (tag == "MARR"):
        marry = 1
    if (divorce):
        Divorced[len(Divorced) - 1] = line.strip()[length:]
        divorce = 0
    if (tag == "DIV"):
        divorce = 1
    if (tag == "HUSB"):
        Husband_ID[len(Husband_ID) - 1] = line.strip()[length:]
        Husband_Name[len(Husband_Name) - 1] = Name[idi.index(
        Husband_ID[len(Husband_ID) - 1])]
    if (tag == "WIFE"):
        Wife_ID[len(Wife_ID) - 1] = line.strip()[length:]
        Wife_Name[len(Wife_Name) - 1] = Name[idi.index(Wife_ID[len(Wife_ID) - 1])]
    if (tag == "CHIL"):
        if (Children[len(Children) - 1] == "N/A"):
            Children[len(Children) - 1] = line.strip()[length:]
        else:
            Children[len(Children) - 1] += " {}".format(line.strip()[length:])

#Check if marriage before death
MarrbeforeBirth = []
MarryAfterDeath = []
DivorcedAfterDeath = []
for i in range(len(idf)):
  #date of marriage converted to usable format
  marrydate = Date(Married[i])
  #Husband birthday converted
  birthdate = Date(Birthday[idi.index(Husband_ID[i])])
  if (marrydate.year - birthdate.year - ((marrydate.month, marrydate.day) < (birthdate.month, birthdate.day))) < 0:
    MarrbeforeBirth.append(Husband_ID[i])
  #Wife birthday converted
  birthdate = Date(Birthday[idi.index(Wife_ID[i])])
  if (marrydate.year - birthdate.year - ((marrydate.month, marrydate.day) < (birthdate.month, birthdate.day))) < 0:
    MarrbeforeBirth.append(Wife_ID[i])
  #Check if died
  if (Alive[idi.index(Husband_ID[i])] == "False"):
    deathdate = Date(Death[idi.index(Husband_ID[i])])
    if (Divorced[i] != "N/A"):
      divorcedate = Date(Divorced[i])
      if (deathdate.year - divorcedate.year - ((deathdate.month, deathdate.day) <( divorcedate.month, divorcedate.day))) < 0:
        DivorcedAfterDeath.append(Husband_ID[i])
    if (deathdate.year - marrydate.year - ((deathdate.month, deathdate.day) < (marrydate.month, marrydate.day))) < 0:
      MarryAfterDeath.append(Husband_ID[i])
  if (Alive[idi.index(Wife_ID[i])] == "False"):
    deathdate = Date(Death[idi.index(Wife_ID[i])])
    if (Divorced[i] != "N/A"):
      divorcedate = Date(Divorced[i])
      if (deathdate.year - divorcedate.year - ((deathdate.month, deathdate.day) <( divorcedate.month, divorcedate.day))) < 0:
        DivorcedAfterDeath.append(Wife_ID[i])
    if (deathdate.year - marrydate.year - ((deathdate.month, deathdate.day) < (marrydate.month, marrydate.day))) < 0:
      MarryAfterDeath.append(Wife_ID[i])

#Adding to Individuals Table
Individuals.add_column("ID", idi)
Individuals.add_column("Name", Name)
Individuals.add_column("Gender", Gender)
Individuals.add_column("Birthday", Birthday)
Individuals.add_column("Age", Age)
Individuals.add_column("Alive", Alive)
Individuals.add_column("Death", Death)
Individuals.add_column("Child", Child)
Individuals.add_column("Spouse", Spouse)

#Adding to Families Table
Families.add_column("ID", idf)
Families.add_column("Married", Married)
Families.add_column("Divorced", Divorced)
Families.add_column("Husband ID", Husband_ID)
Families.add_column("Husband Name", Husband_Name)
Families.add_column("Wife ID", Wife_ID)
Families.add_column("Wife Name", Wife_Name)
Families.add_column("Children", Children)

#Write tables to Output.txt
file1.write("Individuals\n")
file1.write("{}\n".format(Individuals))
file1.write("Families\n")
file1.write("{}".format(Families))
#list = convertDate(Birthday[1])
#file1.write("\n{}".format(list))
file1.close()
