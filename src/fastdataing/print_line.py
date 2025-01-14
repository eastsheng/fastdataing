import functools

def print_line(func):
	@functools.wraps(func)
	def wrapper(*args, **kwargs):
		print(21*"-"," Program Start ",21*"-")
		start_time = time.time()
		results = func(*args, **kwargs)
		end_time = time.time()
		elapsed_time = end_time - start_time
		print(20*"-","Run time:",round(elapsed_time,2),"s ",20*"-")
		return results
	return wrapper