from geoClients.GeoClient import GeoClient, GeoClientException, Location


class HEREGeoClient(GeoClient):

	def __init__(self, APP_ID, APP_CODE):
		
		self.APP_ID=APP_ID
		self.APP_CODE=APP_CODE


	def queryAddress(self,address,max_results=10):
		self.max_results=max_results
		url='https://geocoder.cit.api.here.com/6.2/geocode.json?app_id={}&app_code={}&searchtext={}'.format(self.APP_ID,self.APP_CODE,address)
		data=GeoClient.queryService(self,url)

		return self.parseData(data)	


	def parseData(self,data):

		if 'Response' not in data:
			raise GeoClientException("Bad Results")
			return None

		if 'View' not in data['Response']:
			raise GeoClientException("Bad Results")
			return None

		if len(data['Response']['View'])==0:
			raise GeoClientException("No Results")
			return None

		results=[]

		results_n=0

		for result in data['Response']['View'][0]['Result']:

			if results_n == self.max_results: break


			label_address=result['Location']['Address']['Label']
			loc=result['Location']['DisplayPosition']

			results.append(Location(label_address,loc['Latitude'],loc['Longitude']))

			results_n+=1
			
		return results

