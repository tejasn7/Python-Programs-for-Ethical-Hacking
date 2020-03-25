import requests
from optparse import OptionParser
from bs4 import BeautifulSoup
import sys

def spider(url,depth):
	print("Starting depth "+str(depth))
	if "http" in url:
		data = requests.get(url)
		
		soup = BeautifulSoup(data.text,"html.parser")
		for a in soup.find_all("a",href=True):
		 	endpoints.append(a["href"])
		for endpoint in endpoints:
			if final_host in endpoint:
				final_repeated_endpoints.append(endpoint)
		for i in final_repeated_endpoints:
			if i in final_endpoints:
				pass
			else:
				final_endpoints.append(i)
		if depth == 0:
			print("\n\n=======ENDPOINTS=======\n")
			print("Found "+str(len(final_endpoints))+" endpoints\n\n")
			for j in final_endpoints:
				print(j)
			sys.exit(1)
		for url1 in final_endpoints:
			spider(url1,depth-1)
	
parser = OptionParser()
parser.add_option("-u", "--url", dest="url",help="URL to spider with protocol prefix (HTTP/HTTPS)")
parser.add_option("-d", "--depth", dest="depth",help="Depth of spider",default="1")
(options, args) = parser.parse_args()

url = str(options.url)
depth = int(options.depth)

d = 0
final_repeated_endpoints = []
final_endpoints = []
endpoints = []
#url = sys.argv[1]
try:
	host = url.split("/")[2]

except IndexError:
	print("[-] Use -h option for help menu")
	sys.exit(1)

if "www" in host:
	print("Spidering Host: "+host.split(".")[1]+"."+host.split(".")[2])
	final_host = host.split(".")[1]+"."+host.split(".")[2]
else:
	print("Spidering Host: "+host)
	final_host = host
spider(url,depth)