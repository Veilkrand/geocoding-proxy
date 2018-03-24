from geoClients.GoogleGeoClient import GoogleGeoClient, GeoClientException
from geoClients.HEREGeoClient import HEREGeoClient

import json


class LocationResults(object):
	"""Object to store all results from providers"""
	def __init__(self):
		self.results=[]
	def add(self,provider,locations):
		self.results.append({'service_provider': provider, 'locations':locations})
	def toJson(self):
		return json.dumps(self.__dict__)


if __name__=='__main__':


	#address='1600 Amphitheatre Parkway, Mountain View, CA' # Well defined result
	address='braaaa' # no results
	#address='toledo street' # Multiple results

	GOOGLE_API_KEY='AIzaSyCOfngr1c4dcDFH9HHSC9CDP-pKzH683cU'
	HERE_APP_ID='GERc7Yl4X1AOB1ruz8RY'
	HERE_APP_CODE='476gjAWxDJ1qN2x2rmG__g'

	all_results=LocationResults()

	
	google_client=GoogleGeoClient(GOOGLE_API_KEY)	

	try:
		results=google_client.queryAddress(address,3)
		all_results.add('Google',results)
	except GeoClientException as e:
		print('Error: '+str(e))


	here_client=HEREGeoClient(HERE_APP_ID,HERE_APP_CODE)
	try:
		results=here_client.queryAddress(address,3)
		all_results.add('HERE',results)
	except GeoClientException as e:
		print('Error: '+str(e))

	print(all_results.toJson())
	

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
