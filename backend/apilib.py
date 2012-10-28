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
import imaplib

def getLatestCLPostLink(username, password, subject):
	mail = imaplib.IMAP4_SSL('imap.gmail.com')
	mail.login(username, password)
	mail.select("inbox") # connect to inbox.
	result, data = mail.search(None, 'SUBJECT', subject)
	ids = data[0]
	id_list = ids.split() # ids is a space separated string
	try:
		latest_email_id = id_list[-1]
		result, data = mail.fetch(latest_email_id, "(RFC822)") # fetch the email body (RFC822) for the given ID
		raw_email = data[0][1]
	except IndexError, e:
		raw_email = ""
	
	return raw_email
	


def autoPost(API_REQUEST):
	jsonresp = {'username': API_REQUEST['username'], 'postedurl': 'Error Processing Request'}
	br = mechanize.Browser()
	br.set_handle_robots(False)
	response = ""
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
						if(step.has_key("inputs")):
							for input in step["inputs"].keys():
								if( type(input) == int):
									if(step["inputs"][input][0] == '['):
										field = step["inputs"][input].replace("[","")
										field = field.replace("]","")
										br.set_value(API_REQUEST[field], kind="text", nr=input)
										
									else:
										br.find_control(nr=input).get(step["inputs"][input]).selected = True
									
										
								else:
									br[input] = step["inputs"][input]
						response = br.submit()
					else:
						pass
				
			elif(step["type"] == "newlink"):
				response = br.open("https://post.craigslist.org")
			elif(step["type"] == "followlink"):
				response = br.open("https://post.craigslist.org")
			elif(step["type"] == "emailaction"):
				subjectsearch = step["searchkey"]
				if((subjectsearch.find("[") >= 0) and (subjectsearch.find("]") >= 0)):
					field = subjectsearch.split("[")[1].split("]")[0]
					p = re.compile('\[.*\]')
					subjectsearch = p.subn(API_REQUEST[field],subjectsearch)[0]
				time.sleep(step["delay"])
				print subjectsearch
				email = getLatestCLPostLink(step["username"], step["password"], subjectsearch)
				'''email = email.replace(" ","")
				email = email.replace("\n","")
				email = email.replace("\r","")'''
				print "Email:\"" + email + "\""
				sys.stdout.flush()
				p = re.compile(step["linkpattern"])
				retresult = 0
				if(email == ""):
					subjectsearch = step["postedkey"]
					if((subjectsearch.find("[") >= 0) and (subjectsearch.find("]") >= 0)):
						field = subjectsearch.split("[")[1].split("]")[0]
						p = re.compile('\[.*\]')
						subjectsearch = p.subn(API_REQUEST[field],subjectsearch)[0]
						email = getLatestCLPostLink(step["username"], step["password"], subjectsearch)
						p = re.compile(step["postedlinkpattern"])
						retresult = 1
						
				res = p.search(email).group()
				if(step.has_key("linkbef")):
					res = res.lstrip(step["linkbef"])
				if(step.has_key("linkafter")):
					res = res.split(step["linkafter"])[0]
				if(retresult == 1):
					jsonresp['postedurl'] = res
					return 'Posted to : <a href="%s">%s</a>' % (jsonresp['postedurl'], jsonresp['postedurl'])
				else:			
					response = br.open(res)	
			elif(step["type"] == "result"):
				jsonresp['postedurl'] = br.find_link(nr=step["linkindex"]).url()			
	return 	'Posted to : <a href="%s">%s</a>' % (jsonresp['postedurl'], jsonresp['postedurl'])
			
			

if __name__ == '__main__':
	'''API_REQUEST = {"username": "paccha9999", "password": "u4muixarm7tdmi"}
	print autoPost(API_REQUEST)
	sys.stdout.flush()'''
	email = getLatestCLPostLink("postimize1@gmail.com", "u4muixarm7tdmi", "POST/EDIT/DELETE: \"Assistant\"")
	p = re.compile('https://post.craigslist.*\W')
	print "\"" + p.search(email).group() + "\""


