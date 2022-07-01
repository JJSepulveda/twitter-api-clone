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
