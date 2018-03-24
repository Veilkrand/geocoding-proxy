from geoClients.HEREGeoClient import HEREGeoClient, GeoClientException
#import json

APP_ID='GERc7Yl4X1AOB1ruz8RY'
APP_CODE='476gjAWxDJ1qN2x2rmG__g'

here_client=HEREGeoClient(APP_ID,APP_CODE)

address='toledo' # Multiple results
#address='1600 Amphitheatre Parkway, Mountain View, CA' # Well defined result
#address='braaaa' # no results

try:
	results=here_client.queryAddress(address,3)
	print(results)
except GeoClientException as e:
	print('Error: '+str(e))