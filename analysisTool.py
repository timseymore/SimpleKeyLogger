# -*- coding: utf-8 -*-
"""
Keylogger Analysis Tool


=============================================================================
MIT License

Copyright (c) 2019 Tim Seymore

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


class Date:
    def __init__(self, year: int, month: int, day: int):
        self._year = year
        self._month = month
        self._day = day

    def get_year(self) -> int:
        return self._year

    def get_month(self) -> int:
        return self._month

    def get_day(self) -> int:
        return self._day

    def __eq__(self, d):
        return self._year == d.get_year() and self._month == d.get_month() and self._day == d.get_day()

    def __gt__(self, d):
        return (self._year > d.get_year()) or (self._year == d.get_year() and self._month > d.get_month()) or \
               (self._year == d.get_year() and self._month == d.get_month() and self._day > d.get_day())

    def __ge__(self, d):
        return self.__gt__(d) or self.__eq__(d)

    def __lt__(self, d):
        return not self.__ge__(d)

    def __le__(self, d):
        return self.__lt__(d) or self.__eq__(d)

    def __str__(self):
        return str(self._month) + "/" + str(self._day) + "/" + str(self._year)


class Time:
    def __init__(self, hr: int, mins: int, sec: int, ms: int):
        self._hr = hr
        self._mins = mins
        self._sec = sec
        self._ms = ms

    def get_hr(self) -> int:
        return self._hr

    def get_mins(self) -> int:
        return self._mins

    def get_sec(self) -> int:
        return self._sec

    def get_ms(self) -> int:
        return self._ms

    def __str__(self):
        hr = str(self._hr)
        mins = str(self._mins)
        sec = str(self._sec)
        ms = str(self._ms)
        if self._hr < 10:
            hr = '0' + hr
        if self._mins < 10:
            mins = '0' + mins
        if self._sec < 10:
            sec = '0' + sec
        if self._ms < 100:
            if self._ms < 10:
                ms = '00' + ms
            else:
                ms = '0' + ms
        return hr + ":" + mins + ":" + sec + "." + ms

    def __eq__(self, other):
        return self._hr == other.get_hr() and self._mins == other.get_mins() and self._sec == other.get_sec() and \
               self._ms == other.get_ms()

    def __gt__(self, other):
        return self._hr > other.get_hr() or (self._hr == other.get_hr() and self._mins > other.get_mins()) or \
               (self._hr == other.get_hr() and self._mins == other.get_mins() and self._sec > other.get_sec()) or \
               (self._hr == other.get_hr() and self._mins == other.get_mins() and self._sec == other.get_sec() and
                self._ms > other.get_ms())

    def __ge__(self, other):
        return self.__eq__(other) or self.__gt__(other)

    def __lt__(self, other):
        return not self.__ge__(other)

    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)


class Entry:
    def __init__(self, date: Date, time: Time, key: str):
        self._date = date
        self._time = time
        self._key = key

    def get_date(self) -> Date:
        return self._date

    def get_time(self) -> Time:
        return self._time

    def get_key(self) -> str:
        return self._key

    def __str__(self) -> str:
        return str(self._date) + " " + str(self._time) + ": " + self._key


class Error:
    def __init__(self, message="GenericError"):
        self.message = message
        print("ERROR: " + message)


class AnalysisTool:
    def __init__(self):
        with open("path.txt", 'r') as f:
            log_path = f.read()
        self.log_path = log_path[2:-1]
        self.entries = []
        self.is_running = False

    def main(self):
        self.print_main_title()
        self.build_entry_list()
        self.run()

    @staticmethod
    def print_main_title():
        print("\nSimple Key Logger - Analysis Tool")
        print("=================================\n")

    @staticmethod
    def print_main_options():
        print("\n               Options")
        print("====================================\n")
        print("To view complete log file type 'log'")
        print("For keystrokes only view type 'keys'")
        print("To view the dates saved in log file type 'dates'")
        print("To search entry list type 'search'")
        print("To build new entry list type 'build'")
        print("To check file path type 'path'")
        print("To quit type 'quit'")

    def build_entry_list(self):
        print("Building new entry list...\n")
        print(str(len(self.entries)), "old entries removed")
        self.entries = []
        try:
            with open(self.log_path, 'r') as f:
                for line in f:
                    self.entries.append(make_entry(line))
        except FileNotFoundError:
            Error("FileNotFound")
        if len(self.entries) == 0:
            Error("NoEntriesFound")
        else:
            print(str(len(self.entries)), "new entries added")

    def run(self):
        self.is_running = True
        while self.is_running:
            self.print_main_options()
            self.get_and_handle_input()

    def get_and_handle_input(self):
        _option = get_input().casefold
        if _option == 'quit':
            self.is_running = False
        elif _option == 'path':
            print(self.log_path + "\n")
        elif _option == 'log':
            self.print_full_log()
        elif _option == 'keys':
            self.print_keys()
        elif _option == 'dates':
            self.print_dates()
        elif _option == 'search':
            self.search_entries()
        elif _option == 'build':
            self.build_entry_list()

    def search_entries(self):
        print("       Search Options")
        print("===============================")
        print("To search by pattern type 'p'")
        print("To search by dates type 'd'")
        print("To search dates by time of day type 't'")
        _option = get_input().casefold
        if _option == 'p':
            self.search_by_pattern()
        elif _option == 'd':
            self.search_by_date()
        elif _option == 't':
            self.search_dates_by_time_range()

    def search_by_pattern(self):
        index = 0
        times_found = 0
        print("Pattern to search for:")
        pattern = get_input()
        if len(pattern) != 0:
            for entry in self.entries:
                if is_char(entry.get_key()) and entry.get_key()[1] == pattern[0]:
                    if check_for_pattern(pattern[1:], self.entries[(index + 1):]):
                        times_found += 1
                        print("Pattern found on " + str(entry.get_date()) + " at " + str(entry.get_time()) + '\n')
                        for e in self.entries[index:index + len(pattern)]:
                            print(e)
                index += 1
            if times_found == 0:
                print("Pattern not found\n")
            else:
                print("Pattern was found a total of " + str(times_found) + " times")

    def search_by_date(self):
        print("Dates in entry list:")
        self.print_dates()
        print()
        print("Type the date to start: (yyyy-mm-dd)")
        start_date_str = get_input()
        start_date = make_date(start_date_str)
        if not is_in(start_date, self.get_dates()):
            Error("start date not in entry list")
            return
        print("Type the date to stop: (yyyy-mm-dd)")
        stop_date_str = get_input()
        stop_date = make_date(stop_date_str)
        if not is_in(stop_date, self.get_dates()):
            Error("stop date not in entry list")
            return
        if stop_date < start_date:
            Error("stop date falls before start date")
            return
        print()
        for entry in self.entries:
            if stop_date >= entry.get_date() >= start_date:
                print(entry)

    def search_dates_by_time_range(self):
        print("Dates in entry list:")
        self.print_dates()
        print()
        print("Type the date to start: (yyyy-mm-dd)")
        start_date = make_date(get_input())
        if not is_in(start_date, self.get_dates()):
            Error("start date not in entry list")
            return
        print("Type the date to stop: (yyyy-mm-dd)")
        stop_date = make_date(get_input())
        if not is_in(stop_date, self.get_dates()):
            Error("stop date not in entry list")
            return
        if stop_date < start_date:
            Error("stop date falls before start date")
            return
        print("Type time to start: (hh:mm:ss,mms)")
        start_time = make_time(get_input())
        print("Type time to stop: (hh:mm:ss,mms)")
        stop_time = make_time(get_input())
        if stop_date == start_date and stop_time < start_time:
            Error("stop time falls before start time")
            return
        print()
        for entry in self.entries:
            if stop_date >= entry.get_date() >= start_date and stop_time >= entry.get_time() >= start_time:
                print(entry)

    def get_dates(self) -> list:
        dates = []
        for entry in self.entries:
            if not is_in(entry.get_date(), dates):
                dates.append(entry.get_date())
        return dates

    def print_keys(self):
        for entry in self.entries:
            print(entry.get_key())

    def print_dates(self):
        for date in self.get_dates():
            print(date)

    def print_full_log(self):
        try:
            with open(self.log_path, 'r') as f:
                print("Printing full log...\n")
                print(f.read())
        except FileNotFoundError:
            Error("FileNotFound")


# Helper Functions

def get_input() -> str:
    print()
    string = input('>>> ')
    print()
    return string


def make_date(d_str: str) -> Date:
    """ Returns new Date instance from given date string

    REQUIRES: d_str is in format 'yyyy-mm-dd'
    """
    year = int(d_str[:4])
    month = int(d_str[5:7])
    day = int(d_str[8:])
    return Date(year, month, day)


def make_time(t_str: str) -> Time:
    """ Returns Time instance from given t_str.

    REQUIRES: t_str is in format 'hh:mm:ss,mms'
    """
    hr = int(t_str[:2])
    mins = int(t_str[3:5])
    sec = int(t_str[6:8])
    ms = int(t_str[9:])
    return Time(hr, mins, sec, ms)


def make_entry(line: str) -> Entry:
    """ Returns new Entry instance from given line in log file.

    REQUIRES: line in file exists and is in format 'yyyy-mm-dd hh:mm:ss,mms: key'
    """
    date = make_date(line[:10])
    time = make_time(line[11:23])
    key = line[25:]
    return Entry(date, time, key)


def is_in(el, lst: list) -> bool:
    return lst.__contains__(el)


def is_char(key: str) -> bool:
    return not (is_number(key) or is_symbol(key) or key[0] == 'K')


def is_number(key: str) -> bool:
    return is_in(key, ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])


def is_symbol(key: str) -> bool:
    return is_in(key, [',', '.', '/', "'", ';', '`', '[', ']', '\\', '-', '=', '*', '+'])


def check_for_pattern(pattern: str, entries: list) -> bool:
    if len(entries) > 0:
        return check_pattern_match(pattern, entries)
    return False


def check_pattern_match(_pattern, _entries):
    index = 0
    for char in _pattern:
        if fail_pattern_match(char, _entries[index].get_key()):
            return False
        index += 1
    return True


def fail_pattern_match(_char, _key):
    return _char != _key[1] or not is_char(_key)


if __name__ == "__main__":
    AnalysisTool().main()
