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
TEMPLATE_PATH.append('./templates')

APP_CONFIG = {}
APP_CONFIG["DBNAME"] = "gigzibit"
APP_CONFIG["THUMBNAIL_COLOR"] = "#FEFEFE"
APP_CONFIG["HEADING_COLOR"] = "#EBE0D6"
APP_CONFIG["NAV_COLOR"] = "#FDFDFA"



    
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


@route('/')
def hello_world():
    return template('home.html', APP_CONFIG = APP_CONFIG)
    

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

@route('/scan', method='POST')
def scan(): 
	POST_REQUEST = request.POST
	demojobs_table = pymongo.Connection('localhost', 27017)[APP_CONFIG["DBNAME"]]['demojobs']
	demojobs = []
	demojobs.extend([job for job in demojobs_table.find({"demotype": POST_REQUEST['requesttype']})])
	jobsites_table = pymongo.Connection('localhost', 27017)[APP_CONFIG["DBNAME"]]['jobsites']
	jobsites = []
	jobsites.extend([job for job in jobsites_table.find().sort("vpm", pymongo.DESCENDING)])
	return template('userhome.html', POST_REQUEST = POST_REQUEST, APP_CONFIG = APP_CONFIG, demojobs = demojobs, jobsites = jobsites, noofsites = len(jobsites))



