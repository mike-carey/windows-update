#!/usr/bin/env python

from windows_update import config

import os
import unittest
from unittest import mock

env_var = '_test_foo'
ENV_VAR = env_var.upper()

class ConfigTest(unittest.TestCase):

  @mock.patch.dict(os.environ, {})
  def test_should_default(self):
    v = config.env(env_var, default='default')
    assert v == 'default'

  @mock.patch.dict(os.environ, {})
  def test_should_not_default(self):
    with self.assertRaises(Exception):
      config.env(env_var, _assert=True)

  @mock.patch.dict(os.environ, {ENV_VAR: 'env_var'})
  def test_should_pull_from_env(self):
    v = config.env(env_var)
    assert v == 'env_var'

  @mock.patch.dict(os.environ, {ENV_VAR: '1'})
  def test_should_pull_from_env_and_transform(self):
    v = config.env(env_var, _type=int)
    assert v == 1
    assert isinstance(v, int)

if __name__ == '__main__':
  unittest.main()
