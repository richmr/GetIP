# GetIP

This is a python-based command-line tool to pull the currently visible public IP, log it for future analysis, and optionally alert on changes.

Public IP is pulled from machine-friendly websites.

Dependencies:
- urllib2
- socket (some functions won't work on Windows platform due to this)
- argparse
- logging
- time
