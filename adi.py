import numpy as np
import scipy.interpolate as intp
from astropy.io import fits
from astropy.io import ascii
import sys

files = ascii.read('NIRC2_sci_20020_1.txt')
fileNames = np.array(files['fileNames'])
targets = np.array(files['target'])

positions = ascii.read('starPositions.txt')

ROXs42B = fits.getdata('results/ROXs42Bmed.fits')
ROXs12 = fits.getdata('results/ROXs12med.fits')
o = 512 #psf center (origin)

n = np.size(targets)
for i in range(n):
    if targets[i]!=0:
        im = fits.getdata('calfits/'+fileNames[i])
        x, y = positions['x'][i], positions['y'][i]

        if targets[i]==1:
            spsf = intp.shift(ROXs42B,[positions['y'][i]-o,positions['x'][i]]-o)
            #find scaling ratio
        if targets[i]==2:
            spsf = intp.shift(ROXs12,[positions['y'][i]-o,positions['x'][i]]-o)
            #find scaling ratio

        im = im - s*spsf
        fits.writeto('results/'+fileNames[i][:-5]+'.adi.fits',im)
