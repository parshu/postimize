import time
import re
import mechanize
TIMEOUT = 5
import imaplib
import sys


def log(msg):
	print msg
	sys.stdout.flush()
	
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
	
def logHtml(html, file):
	of = open(file, "w")
	of.write(html)
	of.close()
	log("[HTML_LOG] Most recent browsed page logged: %s" % (file))

def autoPost(br, API_REQUEST, autopoststeps, CONFIG):
	jsonresp = {'username': API_REQUEST['username'], 'postedurl': 'Error Processing Request'}
	response = ""
	for destination in CONFIG["destinations"]:
		site = destination["site"]
		log( "** Processing site: %s" % (site))
		for step in destination[autopoststeps]:
			if(step["type"] == "form"):
				url = step["url"]
				formname = step["formname"]
				if(url != ""):	
					data = {}
					for input in step["inputs"].keys():
						if(step["inputs"][input][0] == '['):
							field = step["inputs"][input].replace("[","")
							field = field.replace("]","")
							data[input] = API_REQUEST[field]
						else:
							data[input] = step["inputs"][input]
					br.open(url)
					br.select_form(name=formname)
					for key in data.keys():
						br[key] = data[key]
						log("Filling form with { %s : %s }" % (key, data[key]))
					response = br.submit()
					logHtml(response.read(), CONFIG["temphtmllog"])
					if ( len(list(br.links(text_regex=step['validationtext']))) > 0 ):
						log("[OPERATION][FORM_SUBMIT] Form Submit operation successful")
					else:
						log("[ERROR][OPERATION][FORM_SUBMIT] Form Submit operation Failed")
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
						logHtml(response.read(), CONFIG["temphtmllog"])
					
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
				return jsonresp
				
			if(CONFIG["wait"]):
				raw_input("Press Enter to continue...")
	return 	br
			
			
