from astropy.io import fits
from astropy.io import ascii
import numpy as np


files = ascii.read('NIRC2_sci_20020_1.txt')
files = np.array(files['fileNames'])

f = open('starPositions.txt','w')
f.write('x\ty\n')

for i in files:
    im = fits.getdata('calfits/'+i[:-5]+'_drp.fits')

