"""
Common fast data processing methods
"""
import os
from scipy.interpolate import make_interp_spline
from scipy.signal import savgol_filter
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import ezdxf
from tqdm import tqdm
import re
import requests
import PyPDF2
from scipy import ndimage
from reportlab.pdfgen import canvas
import time


def __version__():
	version = "1.0.5"
	return version

def print_version():
	version = __version__()
	print("𝒇𝒂𝒔𝒕𝒅𝒂𝒕𝒂𝒊𝒏𝒈-"+version)
	print("\t>>> A collection of frequently employed functions!")
	return

def print_line(func):
    
    def wrapper(*args, **kwargs):
        print(21*"-"," Program Start ",21*"-")
        start_time = time.time()
        func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(20*"-","Run time:",round(elapsed_time,2),"s ",20*"-")
    return wrapper


def cal_diff_coeff(t,msd):
	"""line fitting"""
	fit=np.polyfit(t,msd,1)
	fit_fn = np.poly1d(fit)
	# return slope,x,y
	slope, x, y = fit[0], t, fit_fn(t)	
	return slope, x, y

def Einstein_diffusion(x,y,t1,t2,color="b",ax=False):
	"""
	x,y: time, msd
	t1,t2： range of x
	"""
	Ans2ms=1e-20*1e9
	xf,yf = [],[]
	for i in range(len(x)):
		if x[i] >= t1 and x[i] <= t2:
			xf.append(x[i])
			yf.append(y[i])
	slope,xf,yf = cal_diff_coeff(xf,yf)
	diffcoef = slope*Ans2ms/6
	print("Diffusion coefficient:" ,diffcoef,"(m^2/s)")
	if ax:
		ax.scatter(x,y,s=5,color=color,alpha=0.2)
		ax.plot(xf,yf,color=color,linewidth=2)
		ax.set_xlabel('Time (ns)',size=26)
		ax.set_ylabel('MSD($\mathregular{Å^2}$)',size=26)

	return diffcoef


def smooth_MIS(x,y,factor=300):
	"""
	smooth data
	x: x axis data
	y: y axis data
	factor: smooth factor, like, factor=300
	"""
	x_smooth = np.linspace(x.min(), x.max(), factor)
	y_smooth = make_interp_spline(x, y)(x_smooth)

	print("\n>>> smooth_MIS successfully !\n")
	return x_smooth,y_smooth


def smooth_SF(x,y,factors=[5,3]):
	"""
	smooth data
	x: x axis data
	y: y axis data
	factors: smooth factors, like, factors=[5,3]
	"""
	y_smooth = savgol_filter(y, factors[0], factors[1], mode= 'nearest')
	x_smooth = x
	print("\n>>> smooth_SF successfully !\n")
	return x_smooth,y_smooth


def cal_solpes(x,y):
	"""
	calculating slope
	x: x axis data
	y: y axis data
	"""
	slopes = []

	for i in range(1, len(x)):
	    delta_x = x[i] - x[i - 1]
	    delta_y = y[i] - y[i - 1]
	    slope = abs(delta_y / delta_x)
	    slopes.append(slope)

	x_values = x[1:]
	return 	x_values,slopes


def average_xy(x,y,window_size=10):
	"""
	average data
	x: x axis data
	y: y axis data
	window_size: window size
	"""
	avg_x = []
	avg_y = []
	for i in range(0, len(x), window_size):
	    avg_x.append(sum(x[i:i + window_size]) / window_size)
	    avg_y.append(sum(y[i:i + window_size]) / window_size)
	return avg_x, avg_y


def get_files(directory, suffix):
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

def add_fig(figsize=(10,8),size=22,inout="in",family='Times New Roman',fontset='stix'):
	"""
	add a canvas, return ax
	figsize=(10,8),
	size=22
	"""
	plt.rc('font', family=family, size=size)
	plt.rcParams['mathtext.fontset'] = fontset
	plt.rcParams['xtick.direction'] = inout
	plt.rcParams['ytick.direction'] = inout
	fig = plt.figure(figsize=figsize)
	print("\n>>> add a fig successfully !\n")
	return fig

def add_ax(fig,subplot=(1,1,1)):
	"""
	add a ax
	fig: a  figure
	subplot=(1,1,1)
	"""
	if isinstance(subplot, int):
		subplot = (subplot,)
		subplot = tuple(int(ch) for ch in str(subplot[0]))
	ax = fig.add_subplot(subplot[0],subplot[1],subplot[2])
	return ax


def plot_fig(ax,x,y,label=False,linewidth=1,
	factors=False,color="r-",savefig="temp.png",
	xlabel=False,ylabel=False,fontweight="normal",alpha=1.0,loc="best",ncols=1,
	dpi=300,transparent=True,fontsize=26):
	"""
	plot fig
	x,y: x,y
	label: label="label", default label=False
	linewidth: linewidth=1,
	factors: factors=[199,3],
	color: color="r",
	savefig: savefig="temp.png",
	xlabel: xlabel="X axis",
	ylabel: ylabel="Y axis",
	fontweight: fontweight="normal",
	alpha=1.0,
	ncols = 1
	dpi: dpi=300,
	transparent: transparent=True)
	"""
	if factors==False:
		if label == False:
			ax.plot(x,y,color,linewidth=linewidth,alpha=alpha)
		else:
			ax.plot(x,y,color,label=label,linewidth=linewidth,alpha=alpha)
	else:
		x,y = smooth_SF(x,y,factors=factors)
		if label == False:
			ax.plot(x,y,color,linewidth=linewidth,alpha=alpha)
		else:
			ax.plot(x,y,color,label=label,linewidth=linewidth,alpha=alpha)
	if xlabel==False:
		pass
	else:
		ax.set_xlabel(xlabel,fontweight=fontweight,fontsize=fontsize)
	if ylabel==False:
		pass
	else:
		ax.set_ylabel(ylabel,fontweight=fontweight,fontsize=fontsize)

	ax.patch.set_alpha(0) 
	ax.legend(loc=loc,ncols=ncols).get_frame().set_alpha(0)
	if savefig and savefig != "temp.png":
		plt.savefig(savefig,dpi=dpi,transparent=transparent)
	else:
		pass
	print("\n>>> plot a fig successfully !\n")
	return ax



def plot_scatter(ax,x,y,s=None,marker="o",color="r",linewidths=1.5,edgecolors='face',label=False,
	xlabel=False,ylabel=False,fontweight="normal",fontsize=26,alpha=1.0,loc="best",ncols=1):
	"""
	plot a scatter fig
	x,y: x,y
	s: markersize
	label: label="label", default label=False
	linewidth: linewidth=1,
	marker: marker="o"...
	color: color="r",
	edgecolors: 'face',
	xlabel: xlabel="X axis",
	ylabel: ylabel="Y axis",
	fontweight: fontweight="normal",
	fontsize=26
	alpha=1.0,
	loc="best"
	ncols = 1
	"""
	if label == False:
		ax.scatter(x,y,s=s,marker="o",color=color,alpha=1,linewidths=1.5,edgecolors='face')
	else:
		ax.scatter(x,y,s=s,marker="o",color=color,label=label,alpha=1,linewidths=1.5,edgecolors='face')
	if xlabel==False:
		pass
	else:
		ax.set_xlabel(xlabel,fontweight=fontweight,fontsize=fontsize)
	if ylabel==False:
		pass
	else:
		ax.set_ylabel(ylabel,fontweight=fontweight,fontsize=fontsize)

	ax.patch.set_alpha(0) 
	ax.legend(loc=loc,ncols=ncols).get_frame().set_alpha(0)
	return

def plot_dotsline(ax,x,y,yerr=None, fmt='',markersize=12,markeredgecolor=None,
	elinewidth=1.5,capsize=5,barsabove=True, capthick=1,label=False,
	xlabel=False,ylabel=False,fontweight="normal",fontsize=26,alpha=1.0,loc="best",ncols=1):
	"""
	plot a scatter fig
	x,y: x,y
	yerr: None
	fmt: "ro--"
	markersize: markersize
	markeredgecolor: "r"
	elinewidth: elinewidth=1.5,
	capsize: capsize=5
	barsabove: True,
	capthick: 1,
	label: label="label", default label=False
	xlabel: xlabel="X axis",
	ylabel: ylabel="Y axis",
	fontweight: fontweight="normal",
	fontsize=26
	alpha=1.0,
	loc="best"
	ncols = 1
	"""
	if label == False:
		s1 = ax.errorbar(x,y,yerr=yerr,capsize=capsize,capthick=capthick,alpha=.5,barsabove=barsabove,elinewidth=elinewidth,
				fmt=fmt,mec=markeredgecolor,markersize=markersize)
	else:
		s1 = ax.errorbar(x,y,yerr=yerr,capsize=capsize,capthick=capthick,alpha=.5,barsabove=barsabove,elinewidth=elinewidth,
				fmt=fmt,mec=markeredgecolor,markersize=markersize,label=label)
	
	if xlabel==False:
		pass
	else:
		ax.set_xlabel(xlabel,fontweight=fontweight,fontsize=fontsize)
	if ylabel==False:
		pass
	else:
		ax.set_ylabel(ylabel,fontweight=fontweight,fontsize=fontsize)

	ax.patch.set_alpha(0) 
	ax.legend(loc=loc,ncols=ncols).get_frame().set_alpha(0)
	return



def plot_bars(ax,x,height, width=0.8, bottom=None,align='center',color='b',
	linewidth=0, tick_label=None, label=False,xerr=None, yerr=None,ecolor='black',capsize=0.0,
	hatch=None,edgecolor=None,
	xlabel=False,ylabel=False,fontweight="normal",fontsize=26,alpha=1.0,loc="best",ncols=1):
	"""
	plot a bars fig
	x,height: The x coordinates of the bars, The height(s) of the bars.
	s: markersize
	width: The width(s) of the bars.
	bottom: The y coordinate(s) of the bottom side(s) of the bars.
	align: Alignment of the bars to the x coordinates:
	color: The colors of the bar faces.
	edgecolor: The colors of the bar edges.
	linewidth: Width of the bar edge(s). If 0, don't draw edges.
	tick_label: The tick labels of the bars. Default: None (Use default numeric labels.)
	label: label="label", default label=False
	xerr, yerr: If not None, add horizontal / vertical errorbars to the bar tips.
	ecolor: The line color of the errorbars.	
	capsize: The length of the error bar caps in points.
	hatch: {'/', '\', '|', '-', '+', 'x', 'o', 'O', '.', '*'}
	error_kw: 
	xlabel: xlabel="X axis",
	ylabel: ylabel="Y axis",
	fontweight: fontweight="normal",
	fontsize=26
	alpha=1.0,
	loc="best"
	ncols = 1
	"""
	if label == False:
		ax.bar(x,height,width=width,bottom=None,align=align,color=color,linewidth=linewidth,
			tick_label=None,xerr=xerr, yerr=yerr,ecolor=ecolor,capsize=capsize,hatch=hatch,
			edgecolor=edgecolor)
	else:
		ax.bar(x,height,width=width,bottom=None,align=align,color=color,linewidth=linewidth,
			tick_label=None,xerr=xerr, yerr=yerr,ecolor=ecolor,capsize=capsize,hatch=hatch,
			edgecolor=edgecolor,label=label)
	if xlabel==False:
		pass
	else:
		ax.set_xlabel(xlabel,fontweight=fontweight,fontsize=fontsize)
	if ylabel==False:
		pass
	else:
		ax.set_ylabel(ylabel,fontweight=fontweight,fontsize=fontsize)

	ax.patch.set_alpha(0) 
	ax.legend(loc=loc,ncols=ncols).get_frame().set_alpha(0)
	return




class Figure(object):
	"""Figure class: picture processing"""
	def __init__(self,):
		super(Figure, self).__init__()

	def fig2ico(self,png_file,ico_file=False):
		"""
		convert png to ico file
		png_file: png file name
		ico_file: ico file name
		"""
		image = Image.open(png_file)
		if image.mode != "RGBA":
			image = image.convert("RGBA")
		sizes = [(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)]
		if ico_file==False:
			ico_file = png_file.split(".")[0]+".ico"
		image.save(ico_file, format="ICO", sizes=sizes)
		print("\n>>> png2ico successfully !\n")

		return
		
	def fig2binary(self, fig_file, binary_file=False, threshold=128):
		"""
		convert fig to binary image
		fig_file: fig file name
		threshold: RGB threshold
		"""
		img = Image.open(fig_file)
		gray_image = img.convert("L")
		binary_image = gray_image.point(lambda x: 0 if x < threshold else 255, "1")
		if binary_file==False:
			binary_file = "binary_"+fig_file
		binary_image.save(binary_file)
		print("\n>>> fig2binary successfully !\n")
		return binary_image

	def binary2dxf(self,binary_image_file,dxf_file=False):
		"""
		convert binary to dxf format
		binary_image_file: binary image file name
		dxf_file: dxf file name
		"""
		doc = ezdxf.new("R2010")
		msp = doc.modelspace()
		binary_image = Image.open(binary_image_file)
		width, height = binary_image.size
		for y in tqdm(range(height)):
			for x in range(width):
				pixel = binary_image.getpixel((x, y))
				if pixel == 0:
					msp.add_point((x, y))
		if dxf_file==False:
			dxf_file = "binary_"+binary_image_file
		doc.saveas(dxf_file)
		print("\n>>> binary2dxf successfully !\n")
		return


	def figZoom(self,picture,nzoom,zoom_picture=False,transparent=True):
		"""
		zoom a picture
		picture: a picture file
		nzoom: times of zoom
		zoom_picture: new zoomed picture
		transparent: transparent
		"""
		fig = add_fig(figsize=(6,6))
		ax = add_ax(fig,subplot=(111))

		image = Image.open(picture)
		fig_array = np.array(image)
		data0 = fig_array[:,:,0]
		data1 = fig_array[:,:,1]
		data2 = fig_array[:,:,2]
		zoom_array0 = ndimage.zoom(data0, nzoom, order=3)
		zoom_array1 = ndimage.zoom(data1, nzoom, order=3)
		zoom_array2 = ndimage.zoom(data2, nzoom, order=3)
		zoom_array = np.stack([zoom_array0,zoom_array1,zoom_array2],axis=2)
		ax.imshow(zoom_array,vmin=0, vmax=255)
		ax.set_xticks([])
		ax.set_yticks([])
		ax.set_axis_off()
		ax.patch.set_alpha(0) 

		if zoom_picture:
			plt.savefig(zoom_picture, dpi=300,transparent=transparent)
		else:
			plt.savefig(picture.split(".")[0]+"_zoom.png", dpi=300,
				transparent=transparent)
		
		plt.show()
		return


	@print_line
	def img2pdf(self,pdf_filename,folder_path="./",suffix="png"):
	    """
	    convert images to pdf
	    Parameters:
	    - folder_path: folder path,default "./", the images in folder path should like 0.png ... 10.png ... n.png
	    - suffix: suffix of image file, default="png"
	    """
	    all_files = os.listdir(folder_path)
	    image_filenames = [file for file in all_files if file.endswith("png")]
	    image_filenames = sorted(image_filenames, key=lambda x: int(''.join(filter(str.isdigit, x))))

	    pdf = canvas.Canvas(pdf_filename)

	    for image_filename in tqdm(image_filenames):
	        img = Image.open(image_filename)
	        width, height = img.size
	        pdf.setPageSize((width, height))
	        pdf.drawImage(image_filename, 0, 0, width, height)
	        pdf.showPage()
	    pdf.save()

	    print(f">>> PDF file '{pdf_filename}' created successfully.")




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
	        print("Article not found.")



if __name__ == "__main__":
	print_version()

	# f = Figure()
	# f.fig2binary("toux.jpg","toux_1.jpg")
	# f.binary2dxf("toux_1.jpg","toux_1.dxf")
	# f.fig2ico("toux.jpg","toux.ico")
	# f.figZoom("toux_zoom.png",nzoom=5,)

