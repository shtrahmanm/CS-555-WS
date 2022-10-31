from logging import RootLogger
import sys
from pathlib import Path
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
    self.month = months[list[1]]
    self.year = int(list[2])

def US01(date):
    today = datetime.datetime.now()
    if (today.year - date.year - ((today.month, today.day) <  (date.month, date.day))) < 0:
      return True
    else:
      return False

def US02(birthdate,marrydate):
    if (birthdate.year - marrydate.year -
        ((birthdate.month, birthdate.day) <
         (marrydate.month, marrydate.day))) < 0:
         return True
    else:
        return False

def US03(birthdate, deathdate):
  if ((deathdate.year - birthdate.year) - ((deathdate.month, deathdate.day) < (birthdate.month, birthdate.day))) < 0:
    return True
  else:
    return False

def US04(marrydate, divorcedate):
  if ((divorcedate.year - marrydate.year) - ((divorcedate.month, divorcedate.day) < (marrydate.month, marrydate.day))) < 0:
    return True
  else:
    return False
#returns true if there is a marriage after death 
def US05(deathdate,marrydate):
    if (deathdate.year - marrydate.year -
        ((deathdate.month, deathdate.day) <
         (marrydate.month, marrydate.day))) < 0:
         return True
    else:
        return False
#return true if there is a divorce after death
def US06(deathdate,divorcedate):
    if (deathdate.year - divorcedate.year -
                ((deathdate.month, deathdate.day) <
                (divorcedate.month, divorcedate.day))) < 0:
         return True
    else:
        return False

def US07(age):
  if (age > 150):
    return True
  else:
    return False

#Return true if family contains greater than 15 siblings
def US15(siblings):
  if (len(siblings) > 14):
    return True
  else:
    return False

def US16(husband_id, children_id):
  if(children_id == 'N/A'):
    return None
  hus_split = Name[idi.index(husband_id)].split()
  child_ids = children_id.split()
  for i in range (0, len(child_ids)-1):
    child_names = Name[idi.index(child_ids[i])].split()
    if(Gender[idi.index(child_ids[i])] == 'M'  and child_names[1] != hus_split[1]):
      return "Error US16 " + Name[idi.index(husband_id)] + "(" + idi[idi.index(husband_id)] + ") does not have the same last name as his son, " + Name[idi.index(
                child_ids[i])] + " (" + child_ids[i] + ")."
  return None

#Check if married to descendant
def US17(husband_id, wife_id, i):
  if(Child[idi.index(husband_id)] != 'N/A'):
    Hmom = Wife_ID[idf.index(Child[idi.index(husband_id)])]
    if(Hmom == wife_id):
      return "Error US17 "+ Husband_Name[i] + "(" + husband_id + ") is married to his mother "\
      + Wife_Name[i] + "(" + wife_id + ")."
  elif(Child[idi.index(wife_id)] != 'N/A'):
    Wdad = Husband_ID[idf.index(Child[idi.index(wife_id)])]
    if (Wdad == husband_id):
      return "Error US17 "+  Wife_Name[i] + "(" + wife_id + ") is married to her father "\
      + Husband_Name[i] + "(" + husband_id + ")."
  else:
    return None
#check if husband and wife are siblings (returns true if one parent is shared between spouses)
def US18(husband_id, wife_id):
  if(Child[idi.index(husband_id)] == 'N/A' or Child[idi.index(wife_id)] == 'N/A'):
    return False
  Hdad = Husband_ID[idf.index(Child[idi.index(husband_id)])]
  Hmom = Wife_ID[idf.index(Child[idi.index(husband_id)])]
  Wdad = Husband_ID[idf.index(Child[idi.index(wife_id)])]
  Wmom = Wife_ID[idf.index(Child[idi.index(wife_id)])]
  if (Hdad == Wdad):
    return True
  elif(Hmom == Wmom):
    return True
  else:
    return False
#Correct Gender for role
def US21(husband_id, wife_id, i):
  Hgender = Gender[idi.index(husband_id)]=='F'
  Wgender = Gender[idi.index(wife_id)]=='M'
  if(Hgender=='F' and Wgender == 'M'):
    return "Error US21 "+ Husband_Name[i] + "(" + husband_id + ") is a female and "\
      + Wife_Name[i] + "(" + wife_id + ") is a male."
  elif(Hgender=='F'):
    return "Error US21 "+ Husband_Name[i] + "(" + husband_id + ") is a female."
  elif(Gender[idi.index(wife_id)]=='M'):
    return "Error US21 "+ Wife_Name[i] + "(" + wife_id + ") is a male."

#List deceased
def US29(i):
  if(Alive[i] == 'False'):
    return True
  else:
    return False

#List living married

def US30(i):
  if(Alive[i] == 'True' and Spouse[i] != 'N/A'):
    return True
  else:
    return False



#List orphans
def US33(i):
  if(Age[i]>18):
    return False
  if(Child[i]== 'N/A'):
    return False
  family_id = idf.index(Child[i])
  mother = idi.index(Wife_ID[family_id])
  father = idi.index(Husband_ID[family_id])
  if((Death[mother]!='N/A' and Death[father]!='N/A')):
    return True
  return False
#List large marriage age gap
def US34(husband_id, wife_id,marriage_date, i):
  husb_birth = Date(Birthday[idi.index(husband_id)])
  wife_birth = Date(Birthday[idi.index(wife_id)])
  Hmarr_age = marriage_date.year - husb_birth.year - ((marriage_date.month, marriage_date.day) < (husb_birth.month, husb_birth.day))
  Wmarr_age = marriage_date.year - wife_birth.year - ((marriage_date.month, marriage_date.day) < (wife_birth.month, wife_birth.day))
  if(Hmarr_age/Wmarr_age>2):
    return "Error US34 "+ Husband_Name[i] + "(" + str(Hmarr_age) + ") was more than double the age of " + Wife_Name[i] + "(" +\
      str(Wmarr_age) + ") at the time of marriage."
  elif(Wmarr_age/Hmarr_age>2):
    return "Error US34 "+ Wife_Name[i] + "(" + str(Wmarr_age) + ") was more than double the age of " + Husband_Name[i] + "(" +\
      str(Hmarr_age) + ") at the time of marriage."
  return None

#lists of individual data
idi = []
Name = []
Gender = []
Birthday = []
Deathday = []
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


#list of user stores
lst_US03 = []


#Begin iterating line by line
def parseFile(File):
  #Temp variable to tell if DATE tag is for birth, death date, marriage, etc...
  birth = 0
  death = 0
  marry = 0
  divorce = 0
  if not (File.is_file()):
    sys.exit("File does not exist")
  file1 = open(File, 'r')
  Lines = file1.readlines()
  file1.close()
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
    if valid == 'Y':
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
          Age.append(today.year - year -
                     ((today.month, today.day) < (month, day)))
          birth = 0
        if (death):
          Death[len(Alive) - 1] = line.strip()[length:]
          death = 0
          Deathday.append(line.strip()[length:])
          birthdate = Date(Birthday[len(Birthday) - 1])
          deathdate = Date(Deathday[len(Deathday) - 1])
          if (US03(birthdate, deathdate)):
            Age[len(Alive) - 1] = deathdate.year - year - (
              (deathdate.month, deathdate.day) < (month, day))
            lst_US03.append("Error US03: Birthdate of " + Name[len(Alive) - 1] +
                        "(" + idi[len(Alive) - 1] +
                        ") occurs after his/her death.")
          else:
            Age[len(Alive) - 1] = deathdate.year - year - (
              (deathdate.month, deathdate.day) < (month, day))
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
        Wife_Name[len(Wife_Name) - 1] = Name[idi.index(Wife_ID[len(Wife_ID) -
                                                               1])]
      if (tag == "CHIL"):
        if (Children[len(Children) - 1] == "N/A"):
          Children[len(Children) - 1] = line.strip()[length:]
        else:
          Children[len(Children) - 1] += " {}".format(line.strip()[length:])

def main():
    #Check command line arguments
    if (len(sys.argv) != 2):
        sys.exit("Usage: gedcom_data.py <filename>")
    parseFile(Path(sys.argv[1]))

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

    #Check if marriage before death
    MarrbeforeBirth = []
    MarryAfterDeath = []
    DivorcedAfterDeath = []
    MarriageAfterDivorce = []
    DateAfterToday = []
    MarriedDescendant = []
    Siblings = []
    WrongGender = []
    OlderThan150 = []
    TooManySiblings = []
    MalesName = []
    Orphan = []
    AgeGap = []
    Deceased = []
    AliveAndMarried = []
    today = datetime.datetime.now()

    for i in range(len(idi)):
        birthdate = Date(Birthday[i])

        if (US01(birthdate)):
            DateAfterToday.append('Error US01 Birth Date ' + Birthday[i] + ' happens after today')

        if (Death[i] != 'N/A'):
            deathdate = Date(Death[i])
            if (US01(deathdate)):
                DateAfterToday.append('Error US01 Death Date ' + Death[i] + ' happens after today')

        if(US07(Age[i])):
          OlderThan150.append('Error US07 Age of ' + Name[i] + ' is greater than 150')
        if(US33(i)):
          Orphan.append('US33: ' + Name[i] + '(' + idi[i] + ') is an orphaned child.')

        if(US29(i)):
          Deceased.append('US29: ' + Name[i] + ' is deceased.')

        if(US30(i)):
          AliveAndMarried.append('US30: ' + Name[i] + ' is alive and married.')


    for i in range(len(idf)):
        #date of marriage converted to usable format
        marrydate = Date(Married[i])
        if (today.year - marrydate.year - ((today.month, today.day) <  (marrydate.month, marrydate.day))) < 0:
            DateAfterToday.append('Error US01 Marriage Date ' + Married[i] + ' happens after today')
        #Husband birthday converted
        Hbirthdate = Date(Birthday[idi.index(Husband_ID[i])])
        if (marrydate.year - Hbirthdate.year -
            ((marrydate.month, marrydate.day) <
            (Hbirthdate.month, Hbirthdate.day))) < 0:
            MarrbeforeBirth.append("Error US02 Marriage " + Married[i] + " of " +
                                Husband_ID[i] + " and " + Wife_ID[i] +
                                " occurs before Husband's birth " +
                                Birthday[idi.index(Husband_ID[i])] + ".")
        #Wife birthday converted
        Wbirthdate = Date(Birthday[idi.index(Wife_ID[i])])
        if (marrydate.year - Wbirthdate.year -
            ((marrydate.month, marrydate.day) <
            (Wbirthdate.month, Wbirthdate.day))) < 0:
            MarrbeforeBirth.append("Error US02 Marriage " + Married[i] + " of " +
                                Husband_ID[i] + " and " + Wife_ID[i] +
                                " occurs before Wife's birth " +
                                Birthday[idi.index(Wife_ID[i])] + ".")
        #Check if died
        if (Alive[idi.index(Husband_ID[i])] == "False"):
            Hdeathdate = Date(Death[idi.index(Husband_ID[i])])
            if (Divorced[i] != "N/A"):
                divorcedate = Date(Divorced[i])
                if US06(Hdeathdate, divorcedate):
                    DivorcedAfterDeath.append("Error US06 Divorce " + Divorced[i] +
                                        " of " + Husband_ID[i] + " and " +
                                        Wife_ID[i] + " occurs after wife's death " +
                                        Death[idi.index(Husband_ID[i])] + ".")
            if US05(Hdeathdate,marrydate):
                MarryAfterDeath.append("Error US05 Marriage " + Married[i] + " of " +
                                    Husband_ID[i] + " and " + Wife_ID[i] +
                                    " occurs after wife's death " +
                                    Death[idi.index(Husband_ID[i])] + ".")
        if (Alive[idi.index(Wife_ID[i])] == "False"):
            Wdeathdate = Date(Death[idi.index(Wife_ID[i])])
            if (Divorced[i] != "N/A"):
                divorcedate = Date(Divorced[i])
                if US06(Wdeathdate,divorcedate):
                    DivorcedAfterDeath.append("Error US06 Divorce " + Divorced[i] +
                                        " of " + Husband_ID[i] + " and " +
                                        Wife_ID[i] + " occurs after wife's death " +
                                        Death[idi.index(Wife_ID[i])] + ".")
            if US05(Wdeathdate, marrydate):
                MarryAfterDeath.append("Error US05 Marriage " + Married[i] + " of " +
                                    Husband_ID[i] + " and " + Wife_ID[i] +
                                    " occurs after wife's death " +
                                    Death[idi.index(Wife_ID[i])] + ".")
        if (Divorced[i] != "N/A"):
            divorcedate = Date(Divorced[i])
            if (today.year - divorcedate.year -
                ((today.month, today.day) < (divorcedate.month, divorcedate.day))) < 0:
                DateAfterToday.append('Error US01 Divorce Date ' + Divorced[i] + ' Occurs after today')

            if (US04(marrydate, divorcedate)):
                MarriageAfterDivorce.append("Error US04 Marriage " + Married[i] +
                                        " of " + Husband_Name[i] + "(" + Husband_ID[i] + ") and " + Wife_Name[i] + "(" +
                                        Wife_ID[i] + ") occurs after their divorce " +
                                        Divorced[i] + ".")

        maleNames = US16(Husband_ID[i], Children[i])
        if(maleNames != None):
          MalesName.append(maleNames)

        if(US15(Children[i])):
          TooManySiblings.append('Error US15 ' + Husband_ID[i] + ' and ' + Wife_ID[i] + ' have too many children.')

        #Married to descendant
        descends = US17(Husband_ID[i], Wife_ID[i], i)
        if(descends!=None):
          MarriedDescendant.append(descends)
        #Siblings should not marry
        if(US18(Husband_ID[i], Wife_ID[i])):
          Siblings.append("Error US18 "+ Husband_Name[i] + "(" + Husband_ID[i] + ") and " + Wife_Name[i] + "(" +
                                        Wife_ID[i] + ") are siblings.")
        #Correct gender for role
        gendererror = US21(Husband_ID[i], Wife_ID[i], i)
        if(gendererror!=None):
          WrongGender.append(gendererror)
        #Check marriage age difference
        double_age = US34(Husband_ID[i], Wife_ID[i], marrydate, i)
        if(double_age!=None):
          AgeGap.append(double_age)
        
        #Write tables to Output.txt
        file1 = open("Output.txt", "w")
        file1.write("Individuals\n")
        file1.write("{}\n".format(Individuals))
        file1.write("Families\n")
        file1.write("{}".format(Families))
        #US01
        file1.write("\n{}".format(DateAfterToday))
        #US02
        file1.write("\n{}".format(MarrbeforeBirth))
        #US03
        file1.write("\n{}".format(lst_US03))
        #US04
        file1.write("\n{}".format(MarriageAfterDivorce))
        #US05
        file1.write("\n{}".format(MarryAfterDeath))
        #US06
        file1.write("\n{}".format(DivorcedAfterDeath))
        #US07
        file1.write("\n{}".format(OlderThan150))
        #US15
        file1.write("\n{}".format(TooManySiblings))
        #US16
        file1.write("\n{}".format(MalesName))
        #US17
        file1.write("\n{}".format(MarriedDescendant))
        #US18
        file1.write("\n{}".format(Siblings))
        #US21
        file1.write("\n{}".format(WrongGender))
        #US29
        file1.write("\n{}".format(Deceased))
        #US30
        file1.write("\n{}".format(AliveAndMarried))
        #US33
        file1.write("\n{}".format(Orphan))
        #US34
        file1.write("\n{}".format(AgeGap))

if __name__=="__main__":
    main()