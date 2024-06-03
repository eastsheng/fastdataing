"""
Common fast data processing methods
"""
from scipy.interpolate import make_interp_spline
from scipy.signal import savgol_filter
import numpy as np
import matplotlib.pyplot as plt
import time
import functools

def __version__():
	version = "1.0.5"
	return version

def print_version():
	version = __version__()
	print("𝒇𝒂𝒔𝒕𝒅𝒂𝒕𝒂𝒊𝒏𝒈-"+version)
	print("\t>>> A collection of frequently employed functions!")
	return

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


def cal_solpes(x,y,dn=1):
	"""
	calculating slope
	x: x axis data
	y: y axis data
	"""
	x_values, slopes = [], []
	for i in range(len(x)):
		if i < len(x)-dn:
			delta_x = x[i+dn] - x[i]
			delta_y = y[i+dn] - y[i]
			slope = delta_y / delta_x
			x_values.append(x[i]+delta_x*0.5)
			slopes.append(slope)

	return 	x_values, slopes

def polyfitting(x, y, degree=1,nx=100):
	"""
	polyfitting
	Parameters:
	x, y: x, y
	degree: n of poly
	nx: number of xbin 
	"""
	coefficients = np.polyfit(x, y, degree)
	poly_fit = np.poly1d(coefficients)
	x_fit = np.linspace(min(x), max(x), nx)
	y_fit = poly_fit(x_fit)
	return x_fit, y_fit, poly_fit


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
	return avg_x[:-1], avg_y[:-1]


def add_fig(figsize=(8,6),size=18,inout="in",family='Times New Roman',fontset='stix'):
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
	factors=False,color="r-",savefig="temp.png",bbox_to_anchor=False,
	xlabel=False,ylabel=False,fontweight="normal",alpha=1.0,loc="best",ncols=1,
	dpi=300,transparent=True,fontsize=22):
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
	transparent: transparent=True
	fontsize: fontsize = 22
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
	if bbox_to_anchor:
		ax.legend(loc=loc,ncols=ncols,bbox_to_anchor=bbox_to_anchor).get_frame().set_alpha(0)
	else:
		ax.legend(loc=loc,ncols=ncols).get_frame().set_alpha(0)

	if savefig and savefig != "temp.png":
		plt.savefig(savefig,dpi=dpi,transparent=transparent)
	else:
		pass
	print("\n>>> plot a fig successfully !\n")
	return ax

def set_fig(ax,label=False,xlabel=False,ylabel=False,zlabel=False,transparent=True,
	fontweight="normal",loc="best",bbox_to_anchor=False,ncols=1,fontsize=22):
	"""
	set fig 
	label: label="label", default label=False
	xlabel: xlabel="X axis",
	ylabel: ylabel="Y axis",
	zlabel: zlabel="Z axis" for 3D axis,
	fontweight: fontweight="normal",
	loc: "best"
	bbox_to_anchor: position of legend, (0.5, 0.5), default=False,
	ncols = 1
	fontsize: fontsize = 22
	"""
	if xlabel==False:
		pass
	else:
		ax.set_xlabel(xlabel,fontweight=fontweight,fontsize=fontsize)
	if ylabel==False:
		pass
	else:
		ax.set_ylabel(ylabel,fontweight=fontweight,fontsize=fontsize)

	if zlabel==False:
		pass
	else:
		ax.set_ylabel(zlabel,fontweight=fontweight,fontsize=fontsize)
	if bbox_to_anchor:
		leg = ax.legend(loc=loc,ncols=ncols,bbox_to_anchor=bbox_to_anchor)
	else:
		leg = ax.legend(loc=loc,ncols=ncols)

	if transparent:

		ax.patch.set_alpha(0) 
		leg.get_frame().set_alpha(0)
	
	print("\n>>> set a fig successfully !\n")
	return ax



def plot_scatter(ax,x,y,s=None,marker="o",color="r",linewidths=1.5,edgecolors='face',label=False,bbox_to_anchor=False,
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
	if bbox_to_anchor:
		ax.legend(loc=loc,ncols=ncols,bbox_to_anchor=bbox_to_anchor).get_frame().set_alpha(0)
	else:
		ax.legend(loc=loc,ncols=ncols).get_frame().set_alpha(0)

	return

def plot_dotsline(ax,x,y,yerr=None, fmt='',markersize=12,markeredgecolor=None,bbox_to_anchor=False,
	elinewidth=1.5,capsize=5,barsabove=True, capthick=1,label=False,linewidth=1,
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
				fmt=fmt,mec=markeredgecolor,markersize=markersize,linewidth=linewidth)
	else:
		s1 = ax.errorbar(x,y,yerr=yerr,capsize=capsize,capthick=capthick,alpha=.5,barsabove=barsabove,elinewidth=elinewidth,
				fmt=fmt,mec=markeredgecolor,markersize=markersize,linewidth=linewidth,label=label)
	
	if xlabel==False:
		pass
	else:
		ax.set_xlabel(xlabel,fontweight=fontweight,fontsize=fontsize)
	if ylabel==False:
		pass
	else:
		ax.set_ylabel(ylabel,fontweight=fontweight,fontsize=fontsize)

	ax.patch.set_alpha(0) 
	if bbox_to_anchor:
		ax.legend(loc=loc,ncols=ncols,bbox_to_anchor=bbox_to_anchor).get_frame().set_alpha(0)
	else:
		ax.legend(loc=loc,ncols=ncols).get_frame().set_alpha(0)
	return



def plot_bars(ax,x,height, width=0.8, bottom=None,align='center',color='b',
	linewidth=0, tick_label=None, label=False,xerr=None, yerr=None,ecolor='black',capsize=0.0,
	hatch=None,edgecolor=None,bbox_to_anchor=False,
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
	if bbox_to_anchor:
		ax.legend(loc=loc,ncols=ncols,bbox_to_anchor=bbox_to_anchor).get_frame().set_alpha(0)
	else:
		ax.legend(loc=loc,ncols=ncols).get_frame().set_alpha(0)
	return




if __name__ == "__main__":
	print_version()


