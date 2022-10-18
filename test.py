from gedcom_data import *
import unittest
import logging

class TestStringMethods(unittest.TestCase):

    #Runs script on Sprint 2 ged file so that info lists are populated.
    parseFile(Path('Sprint2-2.ged'))

    def test_US01_1(self):
        result = US01(Date("17 AUG 2022"))
        self.assertEqual(result, False)
    def test_US01_2(self):
        result = US01(Date("15 JUN 2022"))
        self.assertEqual(result, False)
    def test_US01_3(self):
        result = US01(Date("17 MAY 2022"))
        self.assertEqual(result, False)
    def test_US01_4(self):
        result = US01(Date("1 JAN 1973"))
        self.assertEqual(result, False)
    def test_US01_5(self):
        result = US01(Date("17 FEB 2002"))
        self.assertEqual(result, False)

    def test_US02_1(self):
        result = US02(Date("16 JUL 2022"), Date("17 AUG 2022"))
        self.assertEqual(result, True)
    def test_US02_2(self):
        result = US02(Date("16 SEP 2022"), Date("15 JUN 2022"))
        self.assertEqual(result, False)
    def test_US02_3(self):
        result = US02(Date("16 OCT 1968"), Date("17 MAY 2022"))
        self.assertEqual(result, True)
    def test_US02_4(self):
        result = US02(Date("16 NOV 2022"), Date("1 JAN 1973"))
        self.assertEqual(result, False)
    def test_US02_5(self):
        result = US02(Date("16 MAR 1901"), Date("17 FEB 2002"))
        self.assertEqual(result, True)

    #Tests for user story 5
    def test_US05_1(self):
        result = US05(Date("16 JUL 2022"), Date("17 AUG 2022"))
        self.assertEqual(result, True)
    def test_US05_2(self):
        result = US05(Date("16 SEP 2022"), Date("15 JUN 2022"))
        self.assertEqual(result, False)
    def test_US05_3(self):
        result = US05(Date("16 OCT 1968"), Date("17 MAY 2022"))
        self.assertEqual(result, True)
    def test_US05_4(self):
        result = US05(Date("16 NOV 2022"), Date("1 JAN 1973"))
        self.assertEqual(result, False)
    def test_US05_5(self):
        result = US05(Date("16 MAR 1901"), Date("17 FEB 2002"))
        self.assertEqual(result, True)
    
    #Tests for user story 6
    def test_US06_1(self):
        result = US06(Date("16 JUL 2022"), Date("17 AUG 2022"))
        self.assertEqual(result, True)
    def test_US06_2(self):
        result = US06(Date("16 SEP 2022"), Date("15 JUN 2022"))
        self.assertEqual(result, False)
    def test_US06_3(self):
        result = US06(Date("16 OCT 1968"), Date("17 MAY 2022"))
        self.assertEqual(result, True)
    def test_US06_4(self):
        result = US06(Date("16 NOV 2022"), Date("1 JAN 1973"))
        self.assertEqual(result, False)
    def test_US06_5(self):
        result = US06(Date("16 MAR 1901"), Date("17 FEB 2002"))
        self.assertEqual(result, True)

    def test_US07_1(self):
        result = US07(152)
        self.assertEqual(result, True)
    def test_US07_1(self):
        result = US07(30)
        self.assertEqual(result, False)
    def test_US07_1(self):
        result = US07(29)
        self.assertEqual(result, False)
    def test_US07_1(self):
        result = US07(160)
        self.assertEqual(result, True)
    def test_US07_1(self):
        result = US07(18)
        self.assertEqual(result, False)

    def test_US16_1(self):
        result = US16(Husband_ID[0], Children[0])
        self.assertEqual(result, 'Error US16 Edward Shtrahman(@I1@) does not have the same last name as his son, Matthew Shtra (@I3@).')
    def test_US16_2(self):
        result = US16('@I7@', '@I1@ @I11@')
        self.assertEqual(result, None)
    def test_US16_3(self):
        result = US16('@I5@', '@I2@')
        self.assertEqual(result, None)
    def test_US16_4(self):
        result = US16('@I9@', '@I10@ @I13@')
        self.assertEqual(result, None)
    def test_US16_5(self):
        result = US16('@I12@', 'N/A')
        self.assertEqual(result, None)

    def test_US17_1(self):
        result = US17('@I1@', '@I2@', 0)
        self.assertEqual(result, None)
    def test_US17_2(self):
        result = US17('@I7@', '@I8@', 1)
        self.assertEqual(result, None)
    def test_US17_3(self):
        result = US17('@I5@', '@I6@', 2)
        self.assertEqual(result, None)
    def test_US17_4(self):
        result = US17('@I16@', '@I11@', 5)
        self.assertEqual(result, 'Error US17 Gardner Revko(@I16@) is married to his mother Elina Revko(@I11@).')
    def test_US17_5(self):
        result = US17('@I14@', '@I15@', 7)
        self.assertEqual(result, None)


    #Tests for user story 18
    def test_US18_1(self):
        result = US18('@I14@', '@I15@')
        self.assertEqual(result, False)
    def test_US18_2(self):
        result = US18('@I1@', '@I2@')
        self.assertEqual(result, False)
    def test_US18_3(self):
        result = US18('@I5@', '@I6@')
        self.assertEqual(result, False)
    def test_US18_4(self):
        result = US18('@I10@', '@I13@')
        self.assertEqual(result, True)
    def test_US18_5(self):
        result = US18('@I12@', '@I11@')
        self.assertEqual(result, False)
    
    #Tests for user story 21
    def test_US21_1(self):
        result = US21('@I14@', '@I15@', 7)
        self.assertEqual(result, 'Error US21 Pamela Trisha(@I15@) is a male.')
    def test_US21_2(self):
        result = US21('@I1@', '@I2@', 0)
        self.assertEqual(result, None)
    def test_US21_3(self):
        result = US21('@I5@', '@I6@', 2)
        self.assertEqual(result, None)
    def test_US21_4(self):
        result = US21('@I10@', '@I13@', 4)
        self.assertEqual(result, None)
    def test_US21_5(self):
        result = US21('@I12@', '@I11@', 5)
        self.assertEqual(result, None)
if __name__ == '__main__':
    unittest.main()