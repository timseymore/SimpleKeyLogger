# -*- coding: utf-8 -*-
"""
Analysis Tool

Created on Sun Oct 13 13:04:20 2019

@author: Tim Seymore
"""


class Date:
    """
    A date in a log file entry with a year, month, and day
    """
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
        return (self._year > d.get_year()) or (self._year == d.get_year() and self._month > d.get_month()) or\
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
    """
    A time in a log file entry with hours, minutes, seconds, and milliseconds
    """
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
        return self.__le__(other) or self.__eq__(other)


class Entry:
    """
    An entry in a key log file with a date, time, and key press
    """
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


class AnalysisTool:
    """
    tool used to analyze a key log file
    """

    def __init__(self):
        """
        EFFECTS: creates new AnalysisTool instance
        """
        with open("path.txt", 'r') as f:
            log_path = f.read()
        self.log_path = log_path[2:-1]
        self.entries = []

    def main(self):
        """
        EFFECTS: runs the analysis tool ui
        """
        running = True
        print("Simple Key Logger - Analysis Tool")
        print("=================================\n")
        self.build_entry_list()
        while running:
            print("               Options")
            print("====================================\n")
            print("To view complete log file type 'l'")
            print("For keystrokes only view type 'k'")
            print("To view the dates saved in log file type 'd'")
            print("To search entry list type 's'")
            print("To build new entry list type 'b'")
            print("To check file path type 'p'")
            print("To quit type 'q'")
            option = input()
            print()
            if option == 'q':
                running = False
            elif option == 'p':
                print(self.log_path + "\n")
            elif option == 'l':
                self.view_log()
            elif option == 'k':
                self.print_keys()
            elif option == 'd':
                self.print_dates()
            elif option == 's':
                self.search_entries()
            elif option == 'b':
                self.build_entry_list()
            print()
        print("exiting program...")

    def build_entry_list(self):
        """
        MODIFIES: self
        EFFECTS: builds new list of entries from log file,
                prints error message if no entries added
        """
        print("Building new entry list...\n")
        print(str(len(self.entries)) + " entries removed")
        self.entries = []
        try:
            with open(self.log_path, 'r') as f:
                for line in f:
                    self.entries.append(make_entry(line))
        except FileNotFoundError:
            print(FileNotFoundError)
        if len(self.entries) == 0:
            print("Error: no entries added to list")
            print("Verify correct file path and log file for contents")
        else:
            print(str(len(self.entries)) + " entries added")

    def view_log(self):
        """
        REQUIRES: log file exists
        EFFECTS: prints full log file
        """
        with open(self.log_path, 'r') as f:
            print("Printing full log...\n")
            print(f.read())

    def search_entries(self):
        """
        EFFECTS: displays the search options menu and handles choice
        """
        print("       Search Options")
        print("===============================")
        print("To search by pattern type 'p'")
        print("To search by dates type 'd'")
        choice = input()
        if choice == 'p':
            self.search_by_pattern()
        elif choice == 'd':
            self.search_by_date()

    def search_by_pattern(self):
        """
        EFFECTS: takes user input and searches entry list for given pattern
                 prints log entry for each complete pattern found and total number of times found
        """
        index = 0
        times_found = 0
        print("Pattern to search for:")
        pattern = input()
        if len(pattern) != 0:
            for entry in self.entries:
                if entry.get_key()[1] == pattern[0]:
                    if check_for_pattern(pattern[1:], self.entries[(index+1):]):
                        times_found += 1
                        print("Pattern found on " + str(entry.get_date()) + " at " + str(entry.get_time()) + '\n')
                        for e in self.entries[index:index+len(pattern)]:
                            print(e)
                index += 1
            if times_found == 0:
                print("Pattern not found\n")
            else:
                print("Pattern was found a total of " + str(times_found) + " times")

    def search_by_date(self):
        """
        EFFECTS: prints each log entry found in given date and time range in chronological order
        """
        print("Dates in entry list:")
        self.print_dates()
        print()
        # Get user input for start date/time
        print("Type the date to start: (yyyy-mm-dd)")
        start_date_str = input()
        start_date = make_date(start_date_str)
        if not is_in(start_date, self.get_dates()):
            print("ERROR: start date not in entry list")
            return
        print("Type time to start: (hh:mm:ss,mms)")
        # start_time_str = input()
        start_time = make_time(input())  
        # Get user input for stop date/time      
        print("Type the date to stop: (yyyy-mm-dd)")
        stop_date_str = input()
        stop_date = make_date(stop_date_str)
        if not is_in(stop_date, self.get_dates()):
            print("ERROR: stop date not in entry list")
            return
        if stop_date < start_date:
            print("ERROR: stop date falls before start date")
            return
        print("Type time to stop: (hh:mm:ss,mms)")
        stop_time_str = input()
        stop_time = make_time(stop_time_str)
        if stop_date == start_date and stop_time < start_time:
            print("ERROR: stop time falls before start time")
            return
        print()
        # Print selected entries 
        for entry in self.entries:
            if stop_date >= entry.get_date() >= start_date and stop_time >= entry.get_time() >= start_time:
                print(entry)

    def print_keys(self):
        """
        EFFECTS: prints key press from each entry in entries list on a separate line
        """
        for entry in self.entries:
            print(entry.get_key())

    def get_dates(self) -> list:
        """
        EFFECTS: returns list of dates in which there are entries in the list
        """
        dates = []
        for entry in self.entries:
            if not is_in(entry.get_date(), dates):
                dates.append(entry.get_date())
        return dates

    def print_dates(self):
        """
        EFFECTS: prints each date that there are entries for on a separate line
        """
        for date in self.get_dates():
            print(date)


# Helper Functions

def make_date(d_str: str) -> Date:
    """
    REQUIRES: d_str is in format 'yyyy-mm-dd'
    EFFECTS: returns new Date instance from given date string
    """
    year = int(d_str[:4])
    month = int(d_str[5:7])
    day = int(d_str[8:])
    return Date(year, month, day)


def make_time(t_str: str) -> Time:
    """
    REQUIRES: t_str is in format 'hh:mm:ss,mms'
    EFFECTS: returns Time instance from given t_str
    """
    hr = int(t_str[:2])
    mins = int(t_str[3:5])
    sec = int(t_str[6:8])
    ms = int(t_str[9:])
    return Time(hr, mins, sec, ms)


def make_entry(line: str) -> Entry:
    """
    REQUIRES: line in file exists and is in format 'yyyy-mm-dd hh:mm:ss,mms: key'
    EFFECTS: returns new Entry instance from given line in log file
    """
    date = make_date(line[:10])
    time = make_time(line[11:23])
    key = line[25:]
    return Entry(date, time, key)


def is_in(el, lst: list) -> bool:
    """
    EFFECTS: returns True if an equal element is in list, False otherwise
    """
    for entry in lst:
        if entry == el:
            return True
    return False


def is_special(key: str) -> bool:
    """
    EFFECTS: returns true if key is a special key: space, esc, ect..
    """
    return key[0] == 'K'


def is_digit(key: str) -> bool:
    """
    EFFECTS: returns true if key is digit 0-9, false otherwise
    """
    digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    return is_in(key, digits)


def is_symbol(key: str) -> bool:
    """
    EFFECTS: returns true if key is symbol: . , / ect, false otherwise
    """
    symbols = [',', '.', '/', "'", ';', '`', '[', ']', '\\', '*', '-', '+', '=']
    return is_in(key, symbols)


def is_char(key: str) -> bool:
    """
    EFFECTS: returns true if key is an alphabetic character, false otherwise
    """
    return not (is_digit(key) or is_special(key) or is_symbol(key))


def check_for_pattern(pattern: str, entries: list):
    """
    EFFECTS: checks each char in pattern against each entry in entries
             returns true if complete pattern is found starting at beginning of entries list
    """
    index = 0
    for char in pattern:
        if char != entries[index].get_key()[1]:
            return False
        index += 1
    return True


if __name__ == "__main__":
    AnalysisTool().main()
