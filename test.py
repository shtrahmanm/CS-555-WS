from gedcom_data import *
import unittest
import logging

class TestStringMethods(unittest.TestCase):
    parseFile(Path('Sprint2.ged'))

    def test_US03_1(self):
        result = US03(Date("16 JUN 2022"), Date("17 AUG 2022"))
        self.assertEqual(result, False)
    def test_US03_2(self):
        result = US03(Date("16 SEP 2022"), Date("15 JUN 2022"))
        self.assertEqual(result, True)
    def test_US03_3(self):
        result = US03(Date("16 OCT 1968"), Date("17 MAY 2022"))
        self.assertEqual(result, False)
    def test_US03_4(self):
        result = US03(Date("16 NOV 2022"), Date("1 JAN 1973"))
        self.assertEqual(result, True)
    def test_US03_5(self):
        result = US03(Date("16 MAR 1901"), Date("17 FEB 2002"))
        self.assertEqual(result, False)

    def test_US04_1(self):
        result = US04(Date("16 JUN 2022"), Date("17 AUG 2022"))
        self.assertEqual(result, False)
    def test_US04_2(self):
        result = US04(Date("16 SEP 2022"), Date("15 JUN 2022"))
        self.assertEqual(result, True)
    def test_US04_3(self):
        result = US04(Date("16 OCT 1968"), Date("17 MAY 2022"))
        self.assertEqual(result, False)
    def test_US04_4(self):
        result = US04(Date("16 NOV 2022"), Date("1 JAN 1973"))
        self.assertEqual(result, True)
    def test_US04_5(self):
        result = US04(Date("16 MAR 1901"), Date("17 FEB 2002"))
        self.assertEqual(result, False)

    def test_US16_1(self):
        result = US16('@I1@', '@I3@ @14@')
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
        result = US17('@I1@', '@I2@')
        self.assertEqual(result, None)
    def test_US17_2(self):
        result = US17('@I7@', '@I8@')
        self.assertEqual(result, None)
    def test_US17_3(self):
        result = US17('@I5@', '@I6@')
        self.assertEqual(result, None)
    def test_US17_4(self):
        result = US17('@I16@', '@I11@')
        self.assertEqual(result, 'Error US17 The mother, Elina Revko(@I11@), is married to her child Gardner Revko(@I16@).')
    def test_US17_5(self):
        result = US17('@I14@', '@I15@')
        self.assertEqual(result, None)


if __name__ == '__main__':
    unittest.main()
