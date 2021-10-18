#!/usr/bin/env python

import pychromecast

services, browser = pychromecast.discovery.discover_chromecasts()
print(services, browser)
