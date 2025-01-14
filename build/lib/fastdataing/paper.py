"""
Papers utils
"""
import re
import requests
import PyPDF2
import sys
# sys.path.append("..") 
from fastdataing import print_line

class Papers(object):

	"""Papers class: Papers processing"""
	def __init__(self,):
		super(Papers, self).__init__()

	def read_pdf(self,file_path,page_num=0):
		with open(file_path, 'rb') as file:
			reader = PyPDF2.PdfReader(file)
			num_pages = len(reader.pages)
			if page_num<=num_pages:
				page = reader.pages[page_num]
				text = page.extract_text()
			else:
				print("Warning: Your selected page_num is too much")
		return text

	@print_line
	def read_pdf_doi(self,file_path):
		text = self.read_pdf(file_path,page_num=0)

		try:
			a = r"/doi(.*?)\n"
			doi_string = re.findall(a,text)[0]
			doi = doi_string.strip().split("/")
			doi = doi[-2]+"/"+doi[-1]
		except:
			a = r"DOI(.*?)\n"
			doi_string = re.findall(a,text)[0]
			doi = doi_string.strip().split("/")
			doi = doi[-2]+"/"+doi[-1]

		return doi
		
	@print_line
	def read_title(self,text):
		doi = self.read_pdf_doi(text)
		url = f"https://api.crossref.org/works/{doi}"
		r = requests.get(url)
		if r.status_code == 200:
			data=r.json()
			doi = data['message']['DOI']
			title = data['message']['title'][0]
			return title,doi
		else:
			return None,None
			print("Article not found."