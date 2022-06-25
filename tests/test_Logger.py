import pytest

from logtime.Logger import create_logger


class FileWriter:
	def __init__(self, path: str):
		pass
	def write(self, data: dict):
		self.data = data
	def get(self):
		return self.data


class Timer:
	def __init__(self):
		self.count = 0
	def time():
		result = self.count
		self.count += 1
		return result


def setup_sample_logger():
	logger = create_logger()
	my_filewriter = FileWriter('')
	my_time_function = Timer().time
	logger._set_filewriter(my_filewriter)
	logger._set_time_function(my_time_function)

	return logger

def test_mean():
	logger = setup_sample_logger()

	@logger.logtime
	def f(n):
		return n + 1
	
	f(4)
	f(5)
	f(10)

	assert(logger.mean(f.__name__) == 1)

def test_std():
	logger = setup_sample_logger()

	@logger.logtime
	def f(n):
		return n + 2
	f(4)
	f(10)
	f(200)

	assert(logger.std(f.__name__) == 0)


def test_function_list():
	logger = setup_sample_logger()

	@logger.logtime
	def f(n):
		return n

	@logger.logtime
	def g(n):
		return n

	@logger.logtime
	def h(n):
		return n

	f(2)
	g(4)
	h(6)

	lst = logger.list()
	assert(f.__name__ in lst and g.__name__ in lst and h.__name__ in lst)


def test_list_only_run_functions():
	logger = setup_sample_logger()

	@logger.logtime
	def f(n):
		return n

	@logger.logtime
	def g(n):
		return n

	f(2)

	lst = logger.list()
	assert(f.__name__ in lst and g.__name__ not in lst)


def test_std_raises_exception_if_only_run_once():
	logger = setup_sample_logger()

	@logger.logtime
	def f(n):
		return n

	f(2)

	with pytest.raises(Exception):
		logger.std(f.__name__)
