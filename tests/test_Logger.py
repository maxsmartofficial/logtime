import pytest

from logtime.Logger import create_logger


class FileWriter:
	def __init__(self, path: str):
		pass
	def write(self, data: dict):
		self.data = data
	def get(self):
		return self.data


class CountingFileWriter:
	def __init__(self, path: str):
		self.count = 0
	def write(self, data: dict):
		self.data = data
		self.count += 1
	def get(self):
		return self.data

class Timer:
	def __init__(self):
		self.count = 0
	def time(self):
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


def test_list_only_called_functions():
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

def test_mean_raises_exception_if_not_called():
	logger = setup_sample_logger()

	@logger.logtime
	def f(n):
		return n

	with pytest.raises(Exception):
		logger.std(f.__name__)

def test_std_raises_exception_if_only_called_once():
	logger = setup_sample_logger()

	@logger.logtime
	def f(n):
		return n

	f(2)

	with pytest.raises(Exception):
		logger.std(f.__name__)


def test_data_is_saved_continuously():
	logger = create_logger()
	filewriter = CountingFileWriter('')
	time_function = Timer().time
	logger._set_filewriter(filewriter)
	logger._set_time_function(time_function)

	@logger.logtime
	def f(n):
		return n

	initial_count = filewriter.count

	f(2)
	count_1 = filewriter.count
	f(5)
	count_2 = filewriter.count

	assert(initial_count == 0 and count_1 == 1 and count_2 == 2)


def test_data_is_unsaved_when_specified():
	logger = create_logger(save=False)
	filewriter = CountingFileWriter('')
	time_function = Timer().time
	logger._set_filewriter(filewriter)
	logger._set_time_function(time_function)

	@logger.logtime
	def f(n):
		return n

	initial_count = filewriter.count

	f(2)
	count_1 = filewriter.count
	
	assert(initial_count == 0 and count_1 == 0)


def test_data_is_saved_when_called():
	logger = create_logger(save=False)
	filewriter = CountingFileWriter('')
	time_function = Timer().time
	logger._set_filewriter(filewriter)
	logger._set_time_function(time_function)	

	@logger.logtime
	def f(n):
		return n
	
	initial_count = filewriter.count

	f(2)
	count_1 = filewriter.count
	f(5)
	count_2 = filewriter.count

	logger.save()
	count_3 = filewriter.count

	assert(initial_count == 0 and count_1 == 0 and count_2 == 0 and count_3 == 1)
