import os
import pymongo
import string
from bottle import TEMPLATE_PATH, route, jinja2_template as template, request, response
from models import *
from bottle import static_file, request
import urllib
import urllib2
import sys
import json
import datetime
TEMPLATE_PATH.append('./templates')
sys.path.append('./backend/configs')
sys.path.append('./backend')
import apilib
APP_CONFIG = {}
APP_CONFIG["DBNAME"] = "gigzibit"
APP_CONFIG["LOGTABLE"] = "log"
APP_CONFIG["THUMBNAIL_COLOR"] = "#FEFEFE"
APP_CONFIG["HEADING_COLOR"] = "#EBE0D6"
APP_CONFIG["NAV_COLOR"] = "#FDFDFA"


@route('/bootstrap/<dir1>/<dir2>/:filename')
def serve_static(dir1, dir2, filename):
    return static_file(dir1 + '/' + dir2 + '/' + filename, root='./bootstrap/docs/')
    
@route('/HTML-KickStart/<dir1>/:filename')
def serve_static(dir1, filename):
    return static_file(dir1 + '/' + filename, root='./HTML-KickStart/')
    
@route('/HTML-KickStart/<dir1>/<dir2>/:filename')
def serve_static(dir1, dir2, filename):
    return static_file(dir1 + '/' + dir2 + '/' + filename, root='./HTML-KickStart/')

@route('/HTML-KickStart/<dir1>/<dir2>/<dir3>/:filename')
def serve_static(dir1, dir2, dir3, filename):
    return static_file(dir1 + '/' + dir2 + '/' + dir3 + '/' + filename, root='./HTML-KickStart/')


@route('/HTML-KickStart/:filename')
def serve_static(filename):
    return static_file(filename, root='./HTML-KickStart/')

@route('/dist/:filename')
def serve_static(filename):
    return static_file(filename, root='./dist/')
  
@route('/dist/<dir1>/:filename')
def serve_static(dir1, filename):
    return static_file(dir1 + '/' + filename, root='./dist/')  


@route('/')
def hello_world():
    return template('home.html', APP_CONFIG = APP_CONFIG, page = "home")
    

@route('/log/<jsonlog>')
def logger(jsonlog):
	print jsonlog
	sys.stdout.flush()
	logobj = json.loads(jsonlog)
	logobj['time'] = datetime.datetime.utcnow()
	print "LOG: " + str(logobj)
	sys.stdout.flush()
	table = pymongo.Connection('localhost', 27017)[APP_CONFIG["DBNAME"]][APP_CONFIG["LOGTABLE"]]
	table.insert(logobj)

@route('/getsitevalues/<plan>/<damping>')
def getsitevalues(plan, damping):
	damping = float(damping)
	jobsites_table = pymongo.Connection('localhost', 27017)[APP_CONFIG["DBNAME"]]['jobsites']
	jobsites = []
	jobsites.extend([job for job in jobsites_table.find({},{'sourceid':1, plan:1, 'vpm': 1, 'ourcpm':1})])
	i = 0
	jobsiteshash = {}
	for site in jobsites:
		site['vpm'] = int(damping * site['vpm'])
		site['vpm'] = int((site[plan]/10.0) * site['vpm'])
		jobsiteshash[site['sourceid']] = site
		i = i + 1
	return jobsiteshash
	
@route('/metrics')
def metrics():
	logtable = pymongo.Connection('localhost', 27017)[APP_CONFIG["DBNAME"]]['log']
	logs = []
	logs.extend([log for log in logtable.find()])
	users = {}
	for log in logs:
		if(users.has_key(log['user'])):
			if(users[log['user']].has_key(log['action'])):
				users[log['user']][log['action']] = users[log['user']][log['action']] + 1
			else:
				users[log['user']][log['action']] = 1
		else:
			users[log['user']] = {log['action']: 1}
	
	
	return template('metrics.html',users = users)
	
@route('/getsitebulkvalues/<onetcode>/<jobid>')
def getsitebulkvalues(onetcode, jobid):
	onetcodes = onetcode.split("|")
	clause = []
	for onetcode in onetcodes:
		clause.append({'onetcode': onetcode})
	jobid = int(jobid)
	demojobs_table = pymongo.Connection('localhost', 27017)[APP_CONFIG["DBNAME"]]['demojobs']
	demojobs = []
	demojobs.extend([job for job in demojobs_table.find({'$or': clause})])
	jobsitehash = {}
	
	first = True
	for job in demojobs:
		if(job['jobid'] != jobid):
			if(first == True):
				jobsitehash = getsitevalues('rating' + str(job['plan']),job['damping'])
				first = False
			else:
				temphash = getsitevalues('rating' + str(job['plan']),job['damping'])
				for sourceid in jobsitehash.keys():
					jobsitehash[sourceid]['vpm'] = jobsitehash[sourceid]['vpm'] + temphash[sourceid]['vpm']
					jobsitehash[sourceid]['ourcpm'] = jobsitehash[sourceid]['ourcpm'] + temphash[sourceid]['ourcpm']
				
	return jobsitehash

@route('/scan', method='GET')
def scan(): 
	POST_REQUEST = request.GET
	demojobs_table = pymongo.Connection('localhost', 27017)[APP_CONFIG["DBNAME"]]['demojobs']
	demojobs = []
	if(POST_REQUEST['requesttype'] == 'all'):
		demojobs.extend([job for job in demojobs_table.find()])
	else:
		demojobs.extend([job for job in demojobs_table.find({'demotype':POST_REQUEST['requesttype']})])
	jobsites_table = pymongo.Connection('localhost', 27017)[APP_CONFIG["DBNAME"]]['jobsites']
	jobsites = []
	jobsites.extend([job for job in jobsites_table.find().sort("vpm", pymongo.DESCENDING)])
	
	jobsbyonet = {}
	onetcounts = {}
	jobsbycompany = {}
	onetdesctocode = {}
	for job in demojobs:
		if(not jobsbyonet.has_key(job['onetdesc'])):
			jobsbyonet[job['onetdesc']] = []
			onetdesctocode[job['onetdesc']] = job['onetcode']
		jobsbyonet[job['onetdesc']].append(job)
		if(not jobsbycompany.has_key(job['company'])):
			jobsbycompany[job['company']] = []
		jobsbycompany[job['company']].append(job)
	for onet in jobsbyonet.keys():
		onetcounts[onet] = len(jobsbyonet[onet])
	return template('userhome.html', POST_REQUEST = POST_REQUEST, APP_CONFIG = APP_CONFIG, demojobs = demojobs, jobsites = jobsites, noofsites = len(jobsites), demotype = POST_REQUEST['requesttype'], user = POST_REQUEST['user'], page = "scan", jobsbycompany = jobsbycompany, jobsbyonet = jobsbyonet, onetcounts = onetcounts, onetdesctocode = onetdesctocode)


@route('/autopost', method='GET')
def autopost(): 
	API_REQUEST = request.GET
	return apilib.autoPost(API_REQUEST)

@route('/test')
def test():
	return template('test.html') 

