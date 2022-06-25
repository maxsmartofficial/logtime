
from .FileWriter import DefaultFileWriter
import time
from collections import defaultdict
from functools import wraps

class Logger:
	def __init__(self, filewriter, time_function):
		self.filewriter = filewriter
		self.time_function = time_function
		self.results = defaultdict(list)
		self.timed_functions = []

	def _set_filewriter(self, filewriter):
		self.filewriter = filewriter

	def _set_time_function(self, time_function):
		self.time_function = time_function

	def logtime(self, f):
		self.timed_functions.append(f.__name__)
		@wraps(f)
		def wrapper(*args, **kwargs):
			start_time = self.time_function()
			result = f(*args, **kwargs)
			end_time = self.time_function()
			total_time = end_time - start_time
			self.results[f.__name__].append(total_time)
			return result
		return wrapper

	def mean(self, function_name: str):
		self._check_if_timed(function_name)
		lst = self.results[function_name]
		if len(lst) == 0:
			raise Exception("Must have been called at least once")
		total = sum(lst)
		return total/len(lst)

	def std(self, function_name: str):
		self._check_if_timed(function_name)
		lst = self.results[function_name]
		if len(lst) <= 2:
			raise Exception("Must have been called at least twice")
		total = 0
		mean = self.mean(function_name)
		for t in lst:
			total += (t - mean) ** 2
		std = (total / len(lst))**0.5
		return std

	def _check_if_timed(self, function_name: str):
		if not function_name in self.timed_functions:
			raise Exception("Function " + function_name + " is not timed")

	def list(self):
		timed = list(set(self.timed_functions))
		called = [t for t in timed if len(self.results[t]) > 0]
		return called


def create_logger():
	filewriter = DefaultFileWriter()
	return Logger(filewriter, time.time)
