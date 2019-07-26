#!/usr/bin/env python

from windows_update import fs

import os
import sys
import json
import tempfile
import unittest
from unittest import mock

class CacheTest(unittest.TestCase):
  def setUp(self):
    t = tempfile.mkstemp()
    self.tempfile = t[1]

    self.tempfile_to_hash = tempfile.mkstemp()[1]

  def teardown(self):
    os.remove(self.tempfile)

  def test_cache_is_loaded(self):
    data = {"foo": "bar"}
    with open(self.tempfile, 'w') as f:
      json.dump(data, f)
    cache = fs.Cache(self.tempfile)
    assert len(cache.c) != 0
    assert cache.c["foo"] == "bar"

  def test_cache_has_and_get(self):
    data = {"foo": "bar"}
    with open(self.tempfile, 'w') as f:
      json.dump(data, f)
    cache = fs.Cache(self.tempfile)
    assert cache.has('foo') == True
    assert cache.get('foo') == 'bar'

  def test_cache_check(self):
    with open(self.tempfile_to_hash, 'w') as f:
      f.write("---")
      f.write("foo: bar")
    cache = fs.Cache(self.tempfile)
    cache.put(self.tempfile_to_hash)
    h = cache.check(self.tempfile_to_hash)
    assert h == True

if __name__ == '__main__':
  unittest.main()
