import json
import os

DEFAULT_FILENAME = "./logtime_cache/default.json"

class DefaultFileWriter:
	def __init__(self, filename = None):
		if filename:
			self.filename = filename
		else:
			self.filename = DEFAULT_FILENAME
	def write(self, data):
		json_string = json.dumps(data)
		os.makedirs(os.path.dirname(self.filename), exist_ok=True)
		with open(self.filename, 'w') as f:
			f.write(json_string)

	def load(self):
		try:
			with open(self.filename, 'r') as f:
				json_string = f.read()
			return json.loads(data)
		except FileNotFoundError:
			return {}
