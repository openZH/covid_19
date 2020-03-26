#!/usr/bin/env python3

# Various small utilities used by scrapers.

import datetime
import os
import subprocess
import re

def download(url, encoding='utf-8'):
  """curl like"""
  print("Downloading:", url)
  downloader = os.path.join(os.path.dirname(__file__), 'download.sh')
  return subprocess.run([downloader, url], capture_output=True, check=True).stdout.decode(encoding)

def pdfdownload(url, encoding='utf-8'):
  """Download a PDF and convert it to text"""
  print("Downloading:", url)
  downloader = os.path.join(os.path.dirname(__file__), 'download.sh')
  with subprocess.Popen([downloader, url], stdout=subprocess.PIPE) as pdf:
    with subprocess.Popen(['pdftotext', '-', '-'], stdin=pdf.stdout, stdout=subprocess.PIPE) as text:
      t = text.stdout.read()
      text.wait()
      return t.decode(encoding)


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
