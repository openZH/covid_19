#!/usr/bin/env python3

# Various small utilities used by scrapers.

import subprocess
import re

def download(url):
  """curl like"""
  return subprocess.run(["./download.sh", url], capture_output=True).stdout.decode('utf-8')

def filter(pattern, d):
  """grep like"""
  return d

def find(pattern, d):
  """sed like"""
  m = re.search(pattern, d)
  if m:
    return m[1]
  return None
