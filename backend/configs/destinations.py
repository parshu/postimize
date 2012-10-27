
CONFIG = {
	"dbname": "gigzibit",
	"destinations" : [
		{
			"site": "craigslist.org",
			"postingsteps": [
				{
					"url": "https://accounts.craigslist.org/login",
					"formname": "login",
					"inputs": {
							"inputEmailHandle": "username",
							"inputPassword": "password"
						},
					"type": "form"

				},
				{
					"url": "https://post.craigslist.org",
					"type": "newlink"

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

				}
				


			]
			
			
		}
		
	]
}
        		
        			
        				