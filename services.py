"""
Refactor functions that are needed more than one time.
"""
# Python
import json

class FileMannager:
	@staticmethod
	def read_file(file_name: str):
		with open(file_name, "r", encoding="utf-8") as f:
			results = json.loads(f.read())
		
		return results

	@staticmethod
	def write_file(file_name: str, content: list):
		with open(file_name, "w", encoding="utf-8") as f:
			
			f.seek(0) # nos movemos al principio del archivo
			f.write(json.dumps(content)) # lista a json y escribo