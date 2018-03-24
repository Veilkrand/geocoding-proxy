from geoClients.GoogleGeoClient import GoogleGeoClient, GeoClientException
#import json

API_KEY='AIzaSyCOfngr1c4dcDFH9HHSC9CDP-pKzH683cU'

google_client=GoogleGeoClient(API_KEY)

address='toledo street' # Multiple results
#address='1600 Amphitheatre Parkway, Mountain View, CA' # Well defined result
#address='braaaa' # no results

try:
	results=google_client.queryAddress(address,3)
	print(results)
except GeoClientException as e:
	print('Error: '+str(e))