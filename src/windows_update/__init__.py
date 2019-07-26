#!/usr/bin/env python

from . import util, config, parser, scrape, fs, runner

def main():
  runner.Runner().run()
