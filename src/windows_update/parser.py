#!/usr/bin/env python

import xml.etree.ElementTree as ET

KEY_ENTRY = 'entry'
KEY_ID = 'id'

class XmlParser(object):

  def __init__(self, filename, namespace=''):
    self.filename = filename
    self.tree = tree = ET.parse(filename)
    self._root = tree.getroot()
    self.root = WrappedNode(namespace, self._root)
    self.namespace = namespace

class WrappedNode(object):
  def __init__(self, namespace, node):
    self.node = node
    self.namespace = namespace

  def __getattr__(self, key):
    return getattr(self.node, key)

  def key(self, key):
    ns = ''
    if self.namespace != "":
      ns = "{%s}" % self.namespace
    return ns + key

  def findall(self, key):
    return [WrappedNode(self.namespace, node) for node in self.node.findall(self.key(key))]

  def find(self, key):
    return WrappedNode(self.namespace, self.node.find(self.key(key)))
