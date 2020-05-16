import unittest
from analysisTool import *

TEST_DATE1 = Date(1234, 1, 2)
TEST_TIME1 = Time(12, 30, 59, 123)
TEST_ENTRY1 = Entry(TEST_DATE1, TEST_TIME1, "'a'")


class TestHelperFunctions(unittest.TestCase):

    def test_make_date(self):
        call = make_date("1234-01-02")
        self.assertEqual(type(call), type(TEST_DATE1))
        self.assertEqual(call.get_day(), TEST_DATE1.get_day())
        self.assertEqual(call.get_month(), TEST_DATE1.get_month())
        self.assertEqual(call.get_year(), TEST_DATE1.get_year())

    def test_make_time(self):
        call = make_time('12:30:59,123')
        self.assertEqual(type(call), type(TEST_TIME1))
        self.assertEqual(call.get_hr(), TEST_TIME1.get_hr())
        self.assertEqual(call.get_mins(), TEST_TIME1.get_mins())
        self.assertEqual(call.get_sec(), TEST_TIME1.get_sec())
        self.assertEqual(call.get_ms(), TEST_TIME1.get_ms())

    def test_make_entry(self):
        call = make_entry("1234-01-02 12:30:59.123: 'a'")
        self.assertEqual(type(call), type(TEST_ENTRY1))
        self.assertEqual(call.get_date(), TEST_ENTRY1.get_date())
        self.assertEqual(call.get_key(), TEST_ENTRY1.get_key())
        self.assertEqual(call.get_time(), TEST_ENTRY1.get_time())

    def test_is_in(self):
        lst1 = [0, 1, 2, 3, 4]
        lst2 = ['a', 'b', 'c', 'd']
        self.assertTrue(is_in(0, lst1))
        self.assertTrue(is_in(4, lst1))
        self.assertTrue(is_in(2, lst1))
        self.assertFalse(is_in(-1, lst1))
        self.assertFalse(is_in(5, lst1))
        self.assertFalse(is_in(11, lst1))
        self.assertFalse(is_in(12, lst1))
        self.assertTrue(is_in('a', lst2))
        self.assertTrue(is_in('d', lst2))
        self.assertTrue(is_in('c', lst2))
        self.assertFalse(is_in('x', lst2))
        self.assertFalse(is_in('aa', lst2))
        self.assertFalse(is_in('ab', lst2))
        self.assertFalse(is_in('a ', lst2))
        self.assertFalse(is_in(' a', lst2))

    def test_is_char(self):
        self.assertTrue(is_char('a'))
        self.assertTrue(is_char(TEST_ENTRY1.get_key()))
        self.assertFalse((is_char('$')))
        self.assertFalse(is_char('Key.space'))
        self.assertFalse(is_char('1'))

    def test_check_for_pattern(self):
        self.assertTrue(check_for_pattern("a", [TEST_ENTRY1]))


if __name__ == '__main__':
    unittest.main()
