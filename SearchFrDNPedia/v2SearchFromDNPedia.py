import requests
import json
import datetime

# Provide your keys

apikey = "223c85556e5e62512f546e39a"
apisecret = "bec7bfd39738d1e9b974"
apiurl = "https://api.codepunch.com/dnfeed.php"

dayForReview = 2

url = []

# Read each Keyword from Keyword file 
with open ("Proyects\SearchFrDNPedia\keywords.txt", "r") as eachKeyword:
    keywords = [kw.strip() for kw in eachKeyword]

# get_api_token
def get_api_token():
	parameters = {"c": "auth", "k": apikey, "s": apisecret}
	response = requests.get(apiurl, params=parameters)  
	if(response.status_code == 200):
		if response.content.startswith(b"OK: "):
			#print('authentication OK') 
			return response.content[4:]			
		else:
			raise Exception('Authentication: {}' . format(response.content))
	else:
		raise Exception('Authentication: {}' . format(response.status_code))
	
# get_api_data
def get_api_data(parameters):
	response = requests.get(apiurl, params=parameters)
	if(response.status_code == 200):
		if response.content.startswith(b"Error: "):
			raise Exception(format(response.content[7:]))
	else:
		raise Exception('Invalid response code: {}' . format(response.status_code))
	return response.content

def exportTxt (listToCheck):
	unique_url = []
	#Save urls without repeat them 
	[unique_url.append(elements) for elements in listToCheck if elements not in unique_url]
	#Export the results in a .txt file 
	with open ('Proyects\SearchFrDNPedia\suspiciousURLS.txt', 'w+', encoding="utf-8") as results:
		for url in unique_url:
			results.write('http://'+ url +'\n')
	
#	get_api_zip_file
#	get_api_zip_file(parameters, "latest.zip")
'''def get_api_zip_file(parameters, filename):
	response = requests.get(apiurl, params=parameters)
	totalbits = 0
	if response.status_code == 200:
		with open(filename, 'wb') as f:
			for chunk in response.iter_content(chunk_size=1024):
				if chunk:
					totalbits += 1024
					f.write(chunk)
		print("Downloaded",totalbits*1025,"KB...")'''

for k in keywords:
	kw = '%'+k+'%'
	days=0
	while days < dayForReview:
		try:
			# Get the token and then the data
			token = get_api_token()
			search_on_day = datetime.date.today() - datetime.timedelta(days)
			datecode = search_on_day.strftime("%Y%m%d")
			parameters = {"t": token, "d": datecode, "f": "json", "limit": 500, "kw": kw}
			thedata = get_api_data(parameters)
			domaindata = json.loads(thedata)

			for d in domaindata['domains']:
				url.append (d['domain'])
			result = exportTxt(url)
		except Exception as e:
			print (f'{type(e)}, {str(e)} in: {search_on_day}, {k}')
		days +=1