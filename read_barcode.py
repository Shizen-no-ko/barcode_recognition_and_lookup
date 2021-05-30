from __future__ import print_function
import os
from dotenv import load_dotenv
import cloudmersive_barcode_api_client
from cloudmersive_barcode_api_client.rest import ApiException
# import requests
import urllib.request
from urllib.request import Request, urlopen
import json

from pprint import pprint


load_dotenv()







class ReadBarcode:

	def __init__(self):
		# Configure API key authorization: Apikey
		self.configuration = cloudmersive_barcode_api_client.Configuration()
		load_dotenv()
		self.key = os.getenv("API_KEY")
		self.configuration.api_key['Apikey'] = self.key


	def scan_image(self, path):
		# create an instance of the API class
		api_instance = cloudmersive_barcode_api_client.BarcodeScanApi(
			cloudmersive_barcode_api_client.ApiClient(self.configuration))
		image_file = path
		try:
			# Scan and recognize an image of a barcode
			api_response = api_instance.barcode_scan_image(image_file)
			# self.barcode = api_response.raw_text
			return api_response.raw_text
		# except ApiException as e:
		except ApiException:
			return False
			# print("Exception when calling BarcodeScanApi->barcode_scan_image: %s\n" % e)

	def get_product_details(self, value):
		key = os.getenv("LOOKUP_KEY")
		api_key = key
		url = f"https://api.barcodelookup.com/v2/products?barcode={value}&formatted=y&key=" + api_key
		result = {}
		try:
			with urllib.request.urlopen(url) as url:
				data = json.loads(url.read().decode())
			result["barcode"] = data["products"][0]["barcode_number"]
			result["name"] = data["products"][0]["product_name"]
			result["brand"] = data["products"][0]["brand"]
			result["description"] = data["products"][0]["description"]
			result["image"] = data["products"][0]["images"][0]
			result["manufacturer"] = data["products"][0]["manufacturer"]
			return result
		except urllib.error.URLError:
			result = False
		finally:
			return result


