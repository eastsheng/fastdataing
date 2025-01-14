"""
Figure utils
"""
from PIL import Image
import ezdxf
from tqdm import tqdm
from scipy import ndimage
from reportlab.pdfgen import canvas
import sys
from print_line import print_line

# from fastdataing import add_fig, add_ax

# import matplotlib.pyplot as plt

class Figure(object):
	"""Figure class: picture processing"""
	def __init__(self,):
		super(Figure, self).__init__()

	@print_line
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
	@print_line
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
	@print_line
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

	# @print_line
	# def figZoom(self,picture,nzoom,zoom_picture=False,transparent=True):
	# 	"""
	# 	zoom a picture
	# 	picture: a picture file
	# 	nzoom: times of zoom
	# 	zoom_picture: new zoomed picture
	# 	transparent: transparent
	# 	"""
	# 	fig = add_fig(figsize=(6,6))
	# 	ax = add_ax(fig,subplot=(111))

	# 	image = Image.open(picture)
	# 	fig_array = np.array(image)
	# 	data0 = fig_array[:,:,0]
	# 	data1 = fig_array[:,:,1]
	# 	data2 = fig_array[:,:,2]
	# 	zoom_array0 = ndimage.zoom(data0, nzoom, order=3)
	# 	zoom_array1 = ndimage.zoom(data1, nzoom, order=3)
	# 	zoom_array2 = ndimage.zoom(data2, nzoom, order=3)
	# 	zoom_array = np.stack([zoom_array0,zoom_array1,zoom_array2],axis=2)
	# 	ax.imshow(zoom_array,vmin=0, vmax=255)
	# 	ax.set_xticks([])
	# 	ax.set_yticks([])
	# 	ax.set_axis_off()
	# 	ax.patch.set_alpha(0) 

	# 	if zoom_picture:
	# 		plt.savefig(zoom_picture, dpi=300,transparent=transparent)
	# 	else:
	# 		plt.savefig(picture.split(".")[0]+"_zoom.png", dpi=300,
	# 			transparent=transparent)
		
	# 	plt.show()
	# 	return


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


if __name__ == '__main__':
	f = Figure()
	# f.fig2binary("toux.jpg","toux_1.jpg")
	# f.binary2dxf("toux_1.jpg","toux_1.dxf")
	# f.fig2ico("toux.jpg","toux.ico")
	# f.figZoom("toux_zoom.png",nzoom=5,)