"""
Common fast data processing methods
"""
import os
from scipy.interpolate import make_interp_spline
from scipy.signal import savgol_filter
import numpy as np
import matplotlib.pyplot as plt

def __version__():
	version = "1.0.3"
	return version

def smooth_MIS(x,y,factor=300):
	"""
	smooth data
	x: x axis data
	y: y axis data
	factor: smooth factor, like, factor=300
	"""
	x_smooth = np.linspace(x.min(), x.max(), factor)
	y_smooth = make_interp_spline(x, y)(x_smooth)
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
	return x_smooth,y_smooth


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
	return files

def add_fig(figsize=(10,8),size=22):
	"""
	add a canvas, return ax
	figsize=(10,8),
	size=22
	"""
	plt.rc('font', family='Times New Roman', size=size)
	fig = plt.figure(figsize=figsize)
	ax = fig.add_subplot(1,1,1)
	return ax

def plot_fig(ax,x,y,label=False,linewidth=1,
	factors=False,color="r",savefig="temp.png",
	xlabel=False,ylabel=False,fontweight="bold",alpha=1.0,
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
	fontweight: fontweight="bold",
	alpha=1.0,
	dpi: dpi=300,
	transparent: transparent=True)
	"""
	if factors==False:
		if label == False:
			ax.plot(x,y,color=color,linewidth=linewidth,alpha=alpha)
		else:
			ax.plot(x,y,color=color,label=label,linewidth=linewidth,alpha=alpha)
	else:
		x,y = smooth_SF(x,y,factors=factors)
		if label == False:
			ax.plot(x,y,color=color,linewidth=linewidth,alpha=alpha)
		else:
			ax.plot(x,y,color=color,label=label,linewidth=linewidth,alpha=alpha)
	if xlabel==False:
		pass
	else:
		ax.set_xlabel(xlabel,fontweight=fontweight,fontsize=fontsize)
	if ylabel==False:
		pass
	else:
		ax.set_ylabel(ylabel,fontweight=fontweight,fontsize=fontsize)

	ax.patch.set_alpha(0) 
	ax.legend(loc="best",ncols=1).get_frame().set_alpha(0)
	if savefig and savefig != "temp.png":
		plt.savefig(savefig,dpi=dpi,transparent=transparent)
	else:
		pass
	return ax


if __name__ == "__main__":
	print(__version__())
