
CONFIG = {
	"dbname": "gigzibit",
	"temphtmllog": "/Users/parkulkarni/html/temphtml.html",
	"wait": True,
	"destinations" : [
		{
			"site": "craigslist.org",
			"loginsteps": [
				{
					"url": "https://accounts.craigslist.org/login",
					"formname": "login",
					"inputs": {
							"inputEmailHandle": "[username]",
							"inputPassword": "[password]"
						},
					"type": "form",
					"validationtext": "log out"

				}
			],
			"postingsteps": [
				{
					"url": "[posturl]",
					"type": "newlink"
				
				},
				{
					"linktext":"post to classifieds",
					"type": "followlink"

				},
				{
					"url": "",
					"formname": "",
					"formindex":0,
					"inputs": {
							0 : "128"
						},
					"type": "form"

				},
				{
					"url": "",
					"formname": "",
					"formindex":0,
					"inputs": {
							0 : "jo"
						},
					"type": "form"

				},
				{
					"url": "",
					"formname": "",
					"formindex":0,
					"type": "form"

				},
				{
					"url": "",
					"formname": "",
					"formindex":0,
					"inputs": {
							0 : "23"
						},
					"type": "form"

				},
				{
					"url": "",
					"formname": "",
					"formindex":0,
					"inputs": {
							0 : "[title]",
							1 : "[location]",
							3 : "[description]",
							4 : "[compensation]"
						},
					"type": "form"

				},
				{
					"url": "",
					"formname": "",
					"formindex":0,
					"type": "form"

				},
				{
					"type": "emailaction",
					"username":"postimize1@gmail.com",
					"password": "u4muixarm7tdmi",
					"searchkey": "POST/EDIT/DELETE: \"[title]\"",
					"postedkey": "\"[title]\"",
					"delay": 5,
					"linkpattern": "https://post.craigslist.*\W",
					"linkafter": "\r",
					"postedlinkpattern": "http://.*\W"
				},
				{
					"type": "result",
					"linkindex": 3
				
				}
				


			]
			
			
		}
		
	]
}
        		
        			
        				