import os
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("API_KEY")

class ReadBarcode:

	def __init__(self):
		print(key)