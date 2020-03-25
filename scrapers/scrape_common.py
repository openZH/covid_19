#!/usr/bin/env python3

# Various small utilities used by scrapers.

import datetime
import os
import subprocess
import re

def download(url, encoding='utf-8'):
  """curl like"""
  downloader = os.path.join(os.path.dirname(__file__), 'download.sh')
  return subprocess.run([downloader, url], capture_output=True).stdout.decode(encoding)

def filter(pattern, d, flags=re.I):
  """grep like"""
  return "\n".join(l for l in d.split('\n') if re.search(pattern, l, flags=flags))

def find(pattern, d, group=1, flags=re.I):
  """sed like. Ignore character case by default"""
  m = re.search(pattern, d, flags=flags)
  if m:
    return m[group]
  return None

def timestamp():
  now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).astimezone()
  print("Scraped at:", now.isoformat(timespec='seconds'))
