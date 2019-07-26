#!/usr/bin/env python

import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from . import config, fs, scrape, util

class Runner(object):

  @property
  def chrome_options(self):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    return chrome_options

  def __init__(self):
    self.cache = fs.Cache(config.cache_path)
    self.driver = webdriver.Chrome(executable_path = config.driver_path, chrome_options=self.chrome_options)
    self.downloader = fs.Downloader(config.downloads_directory)
    self.scraper = scrape.Scraper(self.driver, os_name=config.os_name)

  def run(self):
    if not os.path.exists(config.driver_path):
      self.downloader.download_file(config.chromedriver_url % '75.0.3770.140', config.executable_path)

    xmlfile = self.downloader.download_file(config.atom_feed, 'atom-feed.xml', skip_cache=(not config.development))

    up_kbid = scrape.UpdateKbidFinder(xmlfile, config.update_rematcher, namespace=config.xml_namespace).find()
    util.log("Update KBID is {}", up_kbid)
    ss_kbid = scrape.ServiceStackKbidFinder(xmlfile, config.service_stack_rematcher, namespace=config.xml_namespace).find()
    util.log("Service Stack KBID is {}", ss_kbid)

    urls = []
    urls.append(*self.scraper.get_urls(config.catalog_url_template % up_kbid))
    urls.append(*self.scraper.get_urls(config.catalog_url_template % ss_kbid))

    for file in self.downloader.download_files(*urls):
      print(file)
