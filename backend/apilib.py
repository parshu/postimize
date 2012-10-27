import time
import urllib2
import json
import urllib
import sys
import os
import datetime
import hashlib
import unicodedata
import re
from operator import itemgetter
import itertools
import math
from BeautifulSoup import BeautifulSoup
sys.path.append('./configs')
import destinations
import mechanize
import pybrowser
TIMEOUT = 5

def autoPost(API_REQUEST):
	br = mechanize.Browser()
	br.set_handle_robots(False)
	for destination in destinations.CONFIG["destinations"]:
		site = destination["site"]
		print "Processing site: %s" % (site)
		sys.stdout.flush()
		for step in destination["postingsteps"]:
			url = step["url"]
			formname = "login"
			data = {}
			for input in step["inputs"].keys():
				data[input] = API_REQUEST[step["inputs"][input]]
			br = pybrowser.fillForm(br, url, formname, data)
			response = br.submit()
			return response.read()
			
			
			

if __name__ == '__main__':
	API_REQUEST = {"username": "paccha9999", "password": "u4muixarm7tdmi"}
	print autoPost(API_REQUEST)
	sys.stdout.flush()		


