from geoClients.GeoClient import GeoClient, GeoClientException, Location


class GoogleGeoClient(GeoClient):

	def __init__(self, API_KEY):
		
		self.API_KEY=API_KEY

	def queryAddress(self,address,max_results=10):
		self.max_results=max_results
		
		url='https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}'.format(address,self.API_KEY)

		data=GeoClient.queryService(self,url)

		return self.parseData(data)	


	def parseData(self,data):

		if 'status' not in data:
			raise GeoClientException("Bad Results")
			return None

		if data['status'] != 'OK':
			raise GeoClientException("Bad Status: " + data['status'])
			return None
		
		if 'results' not in data:
			raise GeoClientException("Bad Results")
			return None

		if len(data['results'])==0:
			raise GeoClientException("No Results")
			return None


		results=[]

		results_n=0


		for result in data['results']:

			if results_n == self.max_results: break

			label_address=result["formatted_address"]
			loc=result['geometry']['location']

			results.append(Location(label_address,loc['lat'],loc['lng']))

			results_n+=1
			
		return results

