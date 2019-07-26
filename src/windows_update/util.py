#!/usr/bin/env python

import re
import datetime
import errno
import os
import sys

def log(message, *args, **kwargs):
  sys.stderr.write(message.format(*args) + "\n")

# if sys.version_info[0] < 3:
#   def log(message, *args, **kwargs):
#     message.replace('{}', '%s')
#     print >> sys.stderr, message % args, **kwargs
# else:
#   def log(message, *args, **kwargs):
#     print(message.format(*args), file=sys.stderr, **kwargs)

def mkdir_p(path):
  try:
    os.makedirs(path)
  except OSError as exc:
    if exc.errno == errno.EEXIST and os.path.isdir(path):
      pass
    else:
      raise

class Time(object):

  UTC_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

  def __init__(self, t):
    self.t = t

  def compare_to(self, u):
    if isinstance(u, Time):
      u = u.t
    t = datetime.datetime.strptime(self.t, Time.UTC_FORMAT)
    u = datetime.datetime.strptime(u, Time.UTC_FORMAT)

    return (t - u) / datetime.timedelta(seconds=1)

  @classmethod
  def compare(t, u):
    return Time(t).compare_to(u)

  def __eq__(self, o):
    assert isinstance(o, Time)
    return self.compare_to(o) == 0

  def __ne__(self, o):
    assert isinstance(o, Time)
    return self.compare_to(o) != 0

  def __gt__(self, o):
    assert isinstance(o, Time)
    return self.compare_to(o) > 0

  def __lt__(self, o):
    assert isinstance(o, Time)
    return self.compare_to(o) < 0

  def __ge__(self, o):
    assert isinstance(o, Time)
    return self.compare_to(o) >= 0

  def __le__(self, o):
    assert isinstance(o, Time)
    return self.compare_to(o) <= 0

  def __str__(self):
    return self.t

class REMatcher(object):
  def __init__(self, regexp):
    self.regexp = regexp

  def match(self, matchstring):
    self.rematch = re.match(self.regexp, matchstring)
    return bool(self.rematch)

  def group(self, i):
    return self.rematch.group(i)
