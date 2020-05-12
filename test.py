import unittest
from analysisTool import *


class TestCase(unittest.TestCase):

    def test_make_date(self):
        self.assertEqual(type(make_date("1234-01-02")), type(Date(1234, 1, 2)))
        self.assertEqual(make_date("1234-01-02").get_day(), Date(1234, 1, 2).get_day())
        self.assertEqual(make_date("1234-01-02").get_month(), Date(1234, 1, 2).get_month())
        self.assertEqual(make_date("1234-01-02").get_year(), Date(1234, 1, 2).get_year())

    def test_make_time(self):
        self.assertEqual(type(make_time('12:30:59,123')), type(Time(12, 30, 59, 123)))
        self.assertEqual(make_time('12:30:59,123').get_hr(), Time(12, 30, 59, 123).get_hr())
        self.assertEqual(make_time('12:30:59,123').get_mins(), Time(12, 30, 59, 123).get_mins())
        self.assertEqual(make_time('12:30:59,123').get_sec(), Time(12, 30, 59, 123).get_sec())
        self.assertEqual(make_time('12:30:59,123').get_ms(), Time(12, 30, 59, 123).get_ms())


if __name__ == '__main__':
    unittest.main()
