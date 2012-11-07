import mechanize
import apilib2
import sys
sys.path.append('./configs')
import destinations

br = mechanize.Browser()
br.set_handle_robots(False)
API_REQUEST = {"username": "postimize2@gmail.com", "password": "test123"}
br = apilib2.autoPost(br, API_REQUEST, "loginsteps", destinations.CONFIG)



