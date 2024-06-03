"""
files utils
"""
import os

def get_files(directory, suffix="py"):
	"""
	Read files with the same suffix in the folder and save them as a list
	directory: a directory for reading
	suffix: a suffix
	"""
	files = []
	for filename in os.listdir(directory):
		if filename.endswith(suffix):
			files.append(filename)
	print("\n>>> get files successfully !\n")
	return files


if __name__ == '__main__':
	get_files(directory="./",suffix="py")