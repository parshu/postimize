import mechanize

def fillForm(br, url,formname,data):
	br = mechanize.Browser()
	br.set_handle_robots(False)
	br.open(url)
	
	br.select_form(name=formname)
	for key in data.keys():
		br[key] = data[key]
	
	
	return br
	
if __name__ == '__main__':
	data = {"inputEmailHandle": "paccha9999", "inputPassword": "u4muixarm7tdmi"}
	print postForm("https://accounts.craigslist.org/login", "login", data)
	sys.stdout.flush()	