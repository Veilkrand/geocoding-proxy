import requests, json

class Location(dict):
	"""Object to represent a physical address with longitude and latitude coords"""
	def __init__(self,address, lat,lon):
		self['address']=address
		self['coords']={'latitude': lat, 'longitude': lon}

	def toJson(self):
		return json.dumps(self.__dict__)

class GeoClientException(Exception):
	"""Simple custom exception"""

class GeoClient(object):
	"""Abstract class to implement basic handling of different geocoding services"""
	
	def __init__(self):
		"""Prototype to overload"""
	
	def queryAddress(address):
		"""Prototype to overload"""

	def queryService(self,url):
		"""Low level http get request handling"""
		try:
			response = requests.get(url)
			response.raise_for_status()
		except requests.exceptions.RequestException as e:
			print(e)
			raise GeoClientException("Bad request")

		if response.status_code != 200:
			raise GeoClientException("Bad HTTP Status Code: "+response.status_code)

		return response.json()

	def parseData(self,data):
		"""Prototype to overload"""


