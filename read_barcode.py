from __future__ import print_function
import os
from dotenv import load_dotenv
import cloudmersive_barcode_api_client
from cloudmersive_barcode_api_client.rest import ApiException
import urllib.request
import json

load_dotenv()


class ReadBarcode:

	def __init__(self):
		# Configure API key authorization: Apikey
		self.configuration = cloudmersive_barcode_api_client.Configuration()
		load_dotenv()
		self.key = os.getenv("API_KEY")
		self.configuration.api_key['Apikey'] = self.key
		self.lookup_key = os.getenv("LOOKUP_KEY")
		self.results = {}


	def scan_image(self, path):
		# create an instance of the API class
		api_instance = cloudmersive_barcode_api_client.BarcodeScanApi(
			cloudmersive_barcode_api_client.ApiClient(self.configuration))
		image_file = path
		try:
			# Scan and recognize an image of a barcode
			api_response = api_instance.barcode_scan_image(image_file)
			return api_response.raw_text
		except ApiException:
			return False

	def get_product_details(self, value):
		# set the url
		url = f"https://api.barcodelookup.com/v2/products?barcode={value}&formatted=y&key=" + self.lookup_key
		# reset results before new lookup
		self.results = {}
		# attempt search on API for barcode info
		try:
			with urllib.request.urlopen(url) as url:
				data = json.loads(url.read().decode())
			# set dictionary to results received
			self.results["barcode"] = data["products"][0]["barcode_number"]
			self.results["name"] = data["products"][0]["product_name"]
			self.results["brand"] = data["products"][0]["brand"]
			self.results["description"] = data["products"][0]["description"]
			self.results["image"] = data["products"][0]["images"][0]
			self.results["manufacturer"] = data["products"][0]["manufacturer"]
			# return True for control flow
			result = True
		except urllib.error.URLError:
			# if error return False for control flow
			result = False
		finally:
			return result
