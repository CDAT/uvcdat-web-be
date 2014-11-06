from django.contrib.staticfiles.finders import BaseFinder, searched_locations
from django.contrib.staticfiles import utils
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.files.storage import FileSystemStorage
from collections import OrderedDict
import os.path
import os

class HydeFinder(BaseFinder):
	"""
	A static files finder that builds static files using hyde
	Uses the HYDE_APPS setting to find the hyde sites
	"""
	def __init__(self):
		try:
			self.locations = settings.HYDE_SITES
		except AttributeError:
			self.locations = []

		if not isinstance(self.locations, (list, tuple)):
			raise ImproperlyConfigured("HYDE_SITES should be list or tuple.")

		self.storages = OrderedDict()
		for loc in self.locations:
			# Let's be lazy right now... search for deploy directory
			path = os.path.join(settings.BASE_DIR, loc, "deploy")
			if os.path.exists(path):
				self.storages[loc] = FileSystemStorage(location=path)

	def find(self, path, all=False):

		matches = []
		for loc in self.storages:
			path_gen = (part for part in path.split(os.path.sep) if part)
			current_part = next(path_gen)

			p = os.path.join(settings.BASE_DIR, loc, "deploy")
			if p not in searched_locations:
				searched_locations.append(path)

			while os.path.exists(os.path.join(p, current_part)):
				try:
					current_part = next(path_gen)
				except StopIteration:
					return os.path.join(p, current_part)

		return matches
	
	def list(self, ignore_patterns):
		for loc in self.storages:
			storage = self.storages[loc]
			for path in utils.get_files(storage, ignore_patterns):
				yield path, storage
