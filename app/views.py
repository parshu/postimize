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
	return template('userhome.html', username = 'newuser', POST_REQUEST = request.POST.keys(), APP_CONFIG = APP_CONFIG)

@route('/:username')
def user(username):
    
	users_table = pymongo.Connection('localhost', 27017)[APP_CONFIG["DBNAME"]]['users']
	userinfo = users_table.find_one({'username': username})
	if not userinfo:
		return 'User %s not a part of our beta test. Please wait for your invite :-)' % username

	
		   
	response.set_cookie('username', username, path = '/')    
	
    
	return template('userhome.html', username = username, userinfo = userinfo, APP_CONFIG = APP_CONFIG)

