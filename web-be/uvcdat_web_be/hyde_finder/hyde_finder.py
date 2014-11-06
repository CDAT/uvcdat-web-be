from django.contrib.staticfiles.finders import BaseFinder
from django.conf import settings

class HydeFinder(BaseFinder):
	"""
	A static files finder that builds static files using hyde
	Uses the HYDE_APPS setting to find the hyde sites
	"""
	def __init__(self):
		print "HydeFinder b1"
		self.locations = []
	
	def find(self, path, all=False):
		print "Find", path, all
		return []
	
	def list(self, ignore_patterns):
		print settings.HYDE_APPS
		yield ""
		raise StopIteration
		
