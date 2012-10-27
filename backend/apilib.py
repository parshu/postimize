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
import re
TIMEOUT = 5

def autoPost(API_REQUEST):
	br = mechanize.Browser()
	br.set_handle_robots(False)
	for destination in destinations.CONFIG["destinations"]:
		site = destination["site"]
		print "Processing site: %s" % (site)
		sys.stdout.flush()
		for step in destination["postingsteps"]:
			if(step["type"] == "form"):
				url = step["url"]
				formname = step["formname"]
				if(url != ""):	
					data = {}
					for input in step["inputs"].keys():
						data[input] = API_REQUEST[step["inputs"][input]]
					br = pybrowser.fillForm(br, url, formname, data)
					response = br.submit()
				else:
					if(formname == ""):
						br.select_form(nr=step["formindex"])
						for input in step["inputs"].keys():
							if( type(input) == int):
								br.find_control(type="select", nr=0).get("570").selected = True
								response = br.submit()
								return response.read()
					else:
						pass
				
			elif(step["type"] == "newlink"):
				response = br.open("https://post.craigslist.org")
			elif(step["type"] == "followlink"):
				response = br.open("https://post.craigslist.org")
				
			
			
			

if __name__ == '__main__':
	API_REQUEST = {"username": "paccha9999", "password": "u4muixarm7tdmi"}
	print autoPost(API_REQUEST)
	sys.stdout.flush()		


