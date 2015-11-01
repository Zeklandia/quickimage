import Quickimage as qi
import pyfits as pf
import matplotlib.pyplot as plt
import numpy as np
import robust as rb
import glob
import img_scale

band = ‘V’
files = glob.glob('Mantis*[0-9]'+band+'_cal.fit*’)
image,header = qi.readimage(files[0])
ysz,xsz = np.shape(image)
zsz = len(files)
refim = files[zsz/2]
qi.makeband()
qi.makeband(band='R’)
qi.makeband(band='ip’)
qi.make_RGB()
