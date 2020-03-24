#!/usr/bin/env python3

# Various small utilities used by scrapers.

import datetime
import subprocess
import re

def download(url, encoding='utf-8'):
  """curl like"""
  return subprocess.run(["./download.sh", url], capture_output=True).stdout.decode(encoding)

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
