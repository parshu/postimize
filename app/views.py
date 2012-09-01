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

@route('/HTML-KickStart/:filename')
def serve_static(filename):
    return static_file(filename, root='./HTML-KickStart/')


@route('/')
def hello_world():
    return template('home.html', APP_CONFIG = APP_CONFIG)
    



@route('/scan', method='POST')
def scan(): 
	POST_REQUEST = request.POST
	demojobs_table = pymongo.Connection('localhost', 27017)[APP_CONFIG["DBNAME"]]['demojobs']
	print POST_REQUEST['requesttype']
	demojobs = []
	demojobs.extend([job for job in demojobs_table.find({"demotype": POST_REQUEST['requesttype']})])
	sys.stdout.flush()
	return template('userhome.html', POST_REQUEST = POST_REQUEST, APP_CONFIG = APP_CONFIG, demojobs = demojobs)



