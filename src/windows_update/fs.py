#!/usr/bin/env python

import os
import json
import hashlib

import py_essentials.hashing as hashing

try:
  import urllib.request as urllib2
except ImportError:
  import urllib2

from . import util

class Cache(object):
  def __init__(self, file, checksum_algorithm='sha256'):
    util.mkdir_p(os.path.dirname(file))
    self.file = file
    self.checksum_algorithm = checksum_algorithm
    self.c = {}
    if os.path.exists(file):
      util.log("Loading cache from {}", file)
      try:
        with open(file, 'r') as f:
          self.c = json.load(f)
      except json.decoder.JSONDecodeError:
        util.log("Error decoding json from cache file, ignoring and moving on")

  def __del__(self):
    util.log("Saving off cache to {}", self.file)
    self.write()

  def key(self, filename):
      return os.path.basename(filename)

  def put(self, filename):
    self.c[self.key(filename)] = self.hash(filename)

  def get(self, key):
    if key in self.c:
      return self.c[key]

    raise Exception("Unknown attribute {}".format(key))

  def has(self, key):
    return key in self.c

  def hash(self, filename):
    return hashing.fileChecksum(filename, self.checksum_algorithm)

  def check(self, filename):
    key = self.key(filename)
    return os.path.exists(filename) and self.has(key) and self.hash(filename) == self.get(key)

  def write(self):
    tmp_file = '{}.tmp'.format(self.file)
    with open(tmp_file, 'w') as f:
      json.dump(self.c, f, indent=2)

    os.rename(tmp_file, self.file)

class Downloader(object):

  def __init__(self, directory, cache=None):
    self.directory = directory
    util.mkdir_p(directory)
    self.cache = cache

  def download_files(self, *urls):
    filepaths = []
    for url in urls:
      filepaths.append(self.download_file(url))
    return filepaths

  def download_file(self, url, filename=None, skip_cache=False):
    if filename is None:
      filename = os.path.basename(url)

    if os.path.isabs(filename):
      filepath = filename
    else:
      filepath = os.path.join(self.directory, filename)

    if self.cache is not None and self.cache.check(filepath):
      util.log("{} is already present and matches hash in cache", self.cache.key(filepath))
      return filepath

    util.log("Downloading {} to {}", url, filepath)
    filedata = urllib2.urlopen(url)
    datatowrite = filedata.read()

    with open(filepath, 'wb') as f:
      f.write(datatowrite)

    if skip_cache:
      util.log("Skipping writing {} to cache".format(filepath))
    elif self.cache is None:
      util.log("Cannot write to cache as it is None")
    else:
      self.cache.put(filepath)

    return filepath
