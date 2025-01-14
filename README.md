### Common fast data processing methods

> A collection of frequently employed functions!

#### Smooth

```
import fastdataing.fastdataing as fd
```

- fd.smooth_MIS(x,y,factor=300): 
  - smooth data
- fd.smooth_SF(x,y,factors=[5,3]): 
  - smooth data

### files processing

```
import fastdataing.files as ff

files = ff.get_files(directory="./",suffix="py")
print(files)
```

- get_files(directory, suffix): 
  - Read files with the same suffix in the folder and save them as a list

### plot figs

```
import fastdataing.fastdataing as fd
import matplotlib.pyplot as plt
fig = fd.add_fig()
ax = fd.add_ax(fig)
plt.show()
```

- add_fig(figsize=(10,8)): 
  - add a canvas, return ax

### Figure Processing

```
import fastdataing.figure as ff
```



- fig2ico(png_file,ico_file=False):
  - convert png to ico file
- fig2binary(fig_file, binary_file=False, threshold=128):
  - convert fig to binary image
- binary2dxf(binary_image_file,dxf_file=False):
  - convert binary to dxf format

### ...