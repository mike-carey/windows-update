#!/usr/bin/env python

import os

from . import util

def env(key, default=None, _assert=False, _type=str):
  KEY = key.upper()
  v = os.getenv(KEY)
  if v is None:
    if _assert == True:
      raise Exception('Missing required environment variable: {}'.format(KEY))
    return default

  return _type(v)

chromedriver_url = env('chromedriver_url', 'https://chromedriver.storage.googleapis.com/index.html?path=%s/')

atom_feed = env('atom_feed', 'https://support.microsoft.com/app/content/api/content/feeds/sap/en-us/6ae59d69-36fc-8e4d-23dd-631d98bf74a9/atom')
catalog_url_template = env('catalog_url_template', 'http://www.catalog.update.microsoft.com/Search.aspx?q=KB%s')
download_url = env('download_url', 'http://www.catalog.update.microsoft.com/DownloadDialog.aspx')
build_regex = env('build_regex', '.*OS Build %s.(\d+).*')
service_stack_regex = env('service_stack_regex', 'Servicing stack update.*%s.*')
build = env('build', '17763')
os_name = env('os_name', 'Windows Server 2019')
xml_namespace = env('xml_namespace', 'http://www.w3.org/2005/Atom')

cache_directory = env('cache_directory', 'cache')
downloads_directory = env('downloads_directory', 'downloads')
driver_directory = env('driver_directory', 'driver')

selenium_driver = 'chromedriver'
cache_file = 'windows-update.json'

# Generated configs
cache_path = os.path.join(cache_directory, cache_file)
driver_path = env('driver_path', os.path.join(driver_directory, selenium_driver))
update_rematcher = util.REMatcher(build_regex % build)
service_stack_rematcher = util.REMatcher(service_stack_regex % os_name)

development = env('development', False, _type=bool)
