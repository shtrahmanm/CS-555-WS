from gedcom_data import *
import unittest
import logging

class TestStringMethods(unittest.TestCase):

    #Runs script on Sprint 2 ged file so that info lists are populated.
    parseFile(Path('Sprint3.ged'))

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
        result = US16(Husband_ID[1], Children[1])
        self.assertEqual(result, None)
    def test_US16_3(self):
        result = US16(Husband_ID[2], Children[2])
        self.assertEqual(result, None)
    def test_US16_4(self):
        result = US16(Husband_ID[3], Children[3])
        self.assertEqual(result, None)
    def test_US16_5(self):
        result = US16(Husband_ID[5], Children[5])
        self.assertEqual(result, None)

    def test_US17_1(self):
        result = US17(Husband_ID[0], Wife_ID[0], 0)
        self.assertEqual(result, None)
    def test_US17_2(self):
        result = US17(Husband_ID[1], Wife_ID[1], 1)
        self.assertEqual(result, None)
    def test_US17_3(self):
        result = US17(Husband_ID[2], Wife_ID[2], 2)
        self.assertEqual(result, None)
    def test_US17_4(self):
        result = US17(Husband_ID[5], Wife_ID[5], 5)
        self.assertEqual(result, 'Error US17 Gardner Revko(@I13@) is married to his mother Elina Revko(@I12@).')
    def test_US17_5(self):
        result = US17(Husband_ID[3], Wife_ID[3], 3)
        self.assertEqual(result, None)


    #Tests for user story 18
    def test_US18_1(self):
        result = US18(Husband_ID[0], Wife_ID[0])
        self.assertEqual(result, False)
    def test_US18_2(self):
        result = US18(Husband_ID[1], Wife_ID[1])
        self.assertEqual(result, False)
    def test_US18_3(self):
        result = US18(Husband_ID[2], Wife_ID[2])
        self.assertEqual(result, False)
    def test_US18_4(self):
        result = US18(Husband_ID[4], Wife_ID[4])
        self.assertEqual(result, True)
    def test_US18_5(self):
        result = US18(Husband_ID[3], Wife_ID[3])
        self.assertEqual(result, False)
    
    #Tests for user story 21
    def test_US21_1(self):
        result = US21(Husband_ID[7], Wife_ID[7], 7)
        self.assertEqual(result, 'Error US21 Pamela Trisha(@I16@) is a male.')
    def test_US21_2(self):
        result = US21(Husband_ID[0], Wife_ID[0], 0)
        self.assertEqual(result, None)
    def test_US21_3(self):
        result = US21(Husband_ID[1], Wife_ID[1], 1)
        self.assertEqual(result, None)
    def test_US21_4(self):
        result = US21(Husband_ID[2], Wife_ID[2], 2)
        self.assertEqual(result, None)
    def test_US21_5(self):
        result = US21(Husband_ID[3], Wife_ID[3], 3)
        self.assertEqual(result, None)

    def test_US29_1(self):
        result = US29(0)
        self.assertEqual(result, False)
    def test_US29_2(self):
        result = US29(1)
        self.assertEqual(result, False)
    def test_US29_3(self):
        result = US29(2)
        self.assertEqual(result, True)
    def test_US29_4(self):
        result = US29(3)
        self.assertEqual(result, False)
    def test_US29_5(self):
        result = US29(4)
        self.assertEqual(result, False)

    def test_US30_1(self):
        result = US30(0)
        self.assertEqual(result, True)
    def test_US30_2(self):
        result = US30(1)
        self.assertEqual(result, True)
    def test_US30_3(self):
        result = US30(2)
        self.assertEqual(result, False)
    def test_US30_4(self):
        result = US30(3)
        self.assertEqual(result, False)
    def test_US30_5(self):
        result = US30(4)
        self.assertEqual(result, True)

    #Tests for user story 33
    def test_US33_1(self):
        result = US33(0)
        self.assertEqual(result, False)
    def test_US33_2(self):
        result = US33(1)
        self.assertEqual(result, False)
    def test_US33_3(self):
        result = US33(2)
        self.assertEqual(result, False)
    def test_US33_4(self):
        result = US33(3)
        self.assertEqual(result, False)
    def test_US33_5(self):
        result = US33(32)
        self.assertEqual(result, True)

    #Tests for user story 34
    def test_US34_1(self):
        result = US34(Husband_ID[1], Wife_ID[1], Date(Married[1]), 1)
        self.assertEqual(result, 'Error US34 Isabella Shtrahman(167) was more than double the age of Jacob Shtrahman(23) at the time of marriage.')
    def test_US34_2(self):
        result = US34(Husband_ID[4], Wife_ID[4], Date(Married[4]), 4)
        self.assertEqual(result, 'Error US34 Boris Kogan(94) was more than double the age of Janette Kogan(21) at the time of marriage.')
    def test_US34_3(self):
        result = US34(Husband_ID[6], Wife_ID[6], Date(Married[6]), 6)
        self.assertEqual(result, 'Error US34 Elina Revko(-3) was more than double the age of Igor Revko(-1) at the time of marriage.')
    def test_US34_4(self):
        result = US34(Husband_ID[0], Wife_ID[0], Date(Married[0]), 0)
        self.assertEqual(result, None)
    def test_US34_5(self):
        result = US34(Husband_ID[2], Wife_ID[2], Date(Married[2]), 2)
        self.assertEqual(result, None)

if __name__ == '__main__':
    unittest.main()