import json, sys, os

from geoClients.GoogleGeoClient import GoogleGeoClient, GeoClientException
from geoClients.HEREGeoClient import HEREGeoClient


class LocationResults(object):
	"""Object to store all results from providers"""
	def __init__(self):
		self.results=[]
	def add(self,provider,locations):
		self.results.append({'service_provider': provider, 'locations':locations})
	def toJson(self):
		return json.dumps(self.__dict__, indent=4,  ensure_ascii=False)

def google_geoclient(address,GOOGLE_API_KEY,max_results=5):

	google_client=GoogleGeoClient(GOOGLE_API_KEY)	

	try:
		results=google_client.queryAddress(address,max_results)
	except GeoClientException as e:
		print('Google service provider Error: '+str(e))
		return None

	return results

def here_geoclient(address,HERE_APP_ID,HERE_APP_CODE,max_results=5):

	here_client=HEREGeoClient(HERE_APP_ID,HERE_APP_CODE)

	try:
		results=here_client.queryAddress(address,max_results)
	except GeoClientException as e:
		print('HERE service provider Error: '+str(e))
		return None

	return results

def findAddress_both_providers(address,max_results=5):
	
	GOOGLE_API_KEY=os.environ["GOOGLE_API_KEY"]
	HERE_APP_ID=os.environ["HERE_APP_ID"]
	HERE_APP_CODE=os.environ["HERE_APP_CODE"]

	all_results=LocationResults()

	results_google=google_geoclient(address,GOOGLE_API_KEY,max_results)
	results_here=here_geoclient(address,HERE_APP_ID,HERE_APP_CODE,max_results)

	if results_google is not None:
		all_results.add('Google',results_google)

	if results_here is not None:
		all_results.add('Here',results_here)

	return all_results

def findAddress_with_failover(address,max_results=5):

	GOOGLE_API_KEY=os.environ["GOOGLE_API_KEY"]
	HERE_APP_ID=os.environ["HERE_APP_ID"]
	HERE_APP_CODE=os.environ["HERE_APP_CODE"]

	all_results=LocationResults()

	results=google_geoclient(address,GOOGLE_API_KEY,max_results)

	if results is not None:
		all_results.add('Google',results)
		return all_results
	else:
		results = here_geoclient(address,HERE_APP_ID,HERE_APP_CODE,max_results)
		if results is not None:
			
			all_results.add('HERE',results)
			return all_results
		else:
			return None

def parse_arguments():

	providers=['failover','all']
	help_string=(	
		"Usage: \npython proxy.py [Address] [Max_results] [Provider_mode] \n"
		"Address: Address e.g. 'Toledo street' (required) \n"
		"Max_results: Number of max results per service provider \n"
		"Provider_mode: 'all' or 'failover' \n"
	)

	max_results=5
	provider=providers[0]

	if len(sys.argv)>4:
		print('Error: Too many arguments')
		print(help_string)
		sys.exit(1)

	if len(sys.argv)<2:
		print('Error: You need to provide an address.')
		print(help_string)
		sys.exit(1)
	else:
		address=sys.argv[1]
		
		if len(sys.argv)>2:
			if sys.argv[2].isnumeric() and int(sys.argv[2])>0:
				max_results=int(sys.argv[2])
			else:
				print('Error: `max_results` has to be a number bigger than zero.')
				print(help_string)
				sys.exit(1)


			if len(sys.argv)==4:
				if sys.argv[3] in providers:
					provider=sys.argv[3]
				else:
					print('Error: You need to supply a valid provider.')
					print(help_string)
					sys.exit(1)
		





	return address, max_results, provider

if __name__=='__main__':

	#address='1600 Amphitheatre Parkway, Mountain View, CA' # Well defined result
	#address='braaaa' # no results
	#address='toledo street' # Multiple results

	address, max_results, provider = parse_arguments()

	if provider=='all':
		results=findAddress_both_providers(address,max_results)
	else:
		results=findAddress_with_failover(address,max_results)


	print(results.toJson())

	"""

	{"results": [
			{"service_provider": "Google", "locations": [{"address": "Toledo, Spain", "coords": {"latitude": 39.8628316, "longitude": -4.027323099999999}}]}, 
			{"service_provider": "HERE", 
				"locations": [{
					"address": "Toledo, Castilla-La Mancha, Espa\u00f1a", 
					"coords": {"latitude": 39.86183, "longitude": -4.02524}
				}
			]}
	]}


	"""
