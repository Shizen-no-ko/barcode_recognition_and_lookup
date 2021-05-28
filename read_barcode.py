from __future__ import print_function
import os
from dotenv import load_dotenv
import cloudmersive_barcode_api_client
from cloudmersive_barcode_api_client.rest import ApiException
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
		image_file = path  # file | Image file to perform the operation on.  Common file formats such as PNG, JPEG are supported.

		try:
			# Scan and recognize an image of a barcode
			api_response = api_instance.barcode_scan_image(image_file)
			pprint(api_response)
		except ApiException as e:
			print("Exception when calling BarcodeScanApi->barcode_scan_image: %s\n" % e)


