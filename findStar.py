from astropy.io import fits
from astropy.io import ascii
import numpy as np


files = ascii.read('NIRC2_sci_20020_1.txt')
f = open('starPositions.txt','w')
f.write('x\ty\n')

for i in files['fileNames']:
    im = fits.getdata('calfits/'+i[:-5]+'_drp.fits')

