#!/usr/bin/env python

from windows_update import util

import unittest

LARGER_TIME = "2019-07-01T02:35:06Z"
SMALLER_TIME = "2019-07-01T01:35:06Z"

class TimeTest(unittest.TestCase):
  def test_time_compare_to(self):
    assert util.Time(LARGER_TIME).compare_to(util.Time(SMALLER_TIME)) > 0
    assert util.Time(SMALLER_TIME).compare_to(util.Time(LARGER_TIME)) < 0
    assert util.Time(SMALLER_TIME).compare_to(util.Time(SMALLER_TIME)) == 0

  def test_magic_methods(self):
    assert util.Time(LARGER_TIME) > util.Time(SMALLER_TIME)
    assert util.Time(LARGER_TIME) >= util.Time(SMALLER_TIME)
    assert util.Time(LARGER_TIME) >= util.Time(LARGER_TIME)
    assert util.Time(SMALLER_TIME) != util.Time(LARGER_TIME)
    assert util.Time(LARGER_TIME) == util.Time(LARGER_TIME)
    assert util.Time(SMALLER_TIME) <= util.Time(LARGER_TIME)
    assert util.Time(SMALLER_TIME) <= util.Time(SMALLER_TIME)
    assert util.Time(SMALLER_TIME) < util.Time(LARGER_TIME)


class REMatcherTest(unittest.TestCase):
  def test_should_find_group(self):
    regex = "- (.*) -"
    m = util.REMatcher(regex)
    is_match = m.match("- hello world -")
    assert is_match == True
    g = m.group(1)
    assert g == "hello world"

if __name__ == '__main__':
  unittest.main()
