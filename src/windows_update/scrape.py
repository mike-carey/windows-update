#!/usr/bin/env python3

import time

from . import util, parser

class KbidMixin(object):
  def get_version(self, node):
    raise Exception('Get version not implemented')

class KbidFinder(object):
  """Finds a KBID."""

  def __init__(self, xmlfile, rematcher, namespace=''):
    self.xmlfile = xmlfile
    self.parser = parser.XmlParser(xmlfile, namespace)
    self.rematcher = rematcher

  def find(self):
    util.log("{}", self.parser.root)
    items = self.parser.root.findall('entry')
    latest_version = None
    latest_kbid = None
    for item in items:
      text = item.find('title').text
      if self.rematcher.match(text):
        v = self.get_version(item)
        if latest_version is None or v > latest_version:
          util.log("{} is greater than {}", v, latest_version)
          latest_version = v
          latest_kbid = item.find('id').text.split(':')[-1:][0]

    if latest_kbid is None:
      raise Exception("KBID is null!")

    return latest_kbid

class UpdateKbidFinder(KbidFinder, KbidMixin):
  def get_version(self, node):
    return int(self.rematcher.group(1))

class ServiceStackKbidFinder(KbidFinder, KbidMixin):
  def get_version(self, node):
    return util.Time(node.find('updated').text)

class Scraper(object):
  """Scrapes the MS webpack for update urls."""

  def __init__(self, driver, os_name):
    self.driver = driver
    self.os_name = os_name

  def get_urls(self, url):
    self.driver.get(url)

    links_to_click = []
    for a in self.driver.find_elements_by_tag_name('a'):
      id = a.get_property("id")
      if id[-5:] == '_link' and a.text.find(self.os_name) != -1:
        links_to_click.append(id[0:-5])

    util.log("Found {} links to click", len(links_to_click))

    urls = []
    for link_to_click in links_to_click:
      util.log("Clicking the {} link", link_to_click)
      self.driver.find_element_by_id(link_to_click).click()
      util.log("Switching to the other window")
      self.driver.switch_to.window(self.driver.window_handles[1])
      time.sleep(2)
      for a in self.driver.find_elements_by_tag_name('a'):
        util.log("Found a new link")
        urls.append(a.get_property('href'))
      util.log("Closing the windows")
      self.driver.close()
      util.log("Switching to the other window")
      self.driver.switch_to.window(self.driver.window_handles[0])

    util.log("Found {} updates", len(urls))

    return urls
