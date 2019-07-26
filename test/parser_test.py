#!/usr/bin/env python

from windows_update import parser

import os
import tempfile
import unittest

xml_feed = '''<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
<entry>
  <title>How to create and manage the Central Store for Group Policy Administrative Templates in Windows</title>
  <id>urn:docid:3087759</id>
  <updated>2019-07-18T06:59:18Z</updated>
  <content type="text">This article describes how to create a Central Store on a domain controller to store and replicate registry-based policies for Windows operating systems in a domain.</content>
  <link href="https://support.microsoft.com/help/3087759" />
</entry>
<entry>
  <title>Servicing stack update for Windows 10, Version 1507</title>
  <id>urn:docid:4509090</id>
  <updated>2019-07-09T17:04:33Z</updated>
  <content type="text">Learn more about update KB4509090, including improvements and fixes, any known issues, and how to get the update.</content>
  <link href="https://support.microsoft.com/help/4509090" />
</entry>
</feed>
'''

class ParseTest(unittest.TestCase):

  def setUp(self):
    t = tempfile.mkstemp()
    with open(t[1], 'w') as f:
      f.write(xml_feed)
    self.tempfile = t[1]

  def teardown(self):
    os.remove(self.tempfile)

  def test_get_entries(self):
    p = parser.XmlParser(self.tempfile, namespace="http://www.w3.org/2005/Atom")
    es = p.root.findall("entry")

    assert len(es) == 2

if __name__ == '__main__':
  unittest.main()
