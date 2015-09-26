import numpy as np
import scipy.interpolate as intp
from astropy.io import fits
from astropy.io import ascii
import sys

files = ascii.read('NIRC2_sci_20020_1.txt')
fileNames = np.array(files['fileNames'])
targets = np.array(files['target'])

ROXs42B = fits.getdata('results/ROXs42Bmed.fits')
ROXs12 = fits.getdata('results/ROXs12med.fits')
o = 512 #psf center (origin)

n = np.size(targets)
for i in range(n):
    if targets[i]!=0:
        im = fits.getdata('/'+fileNames[i])[:-5]+'.reg.fits')

        if targets[i]==1:
            psf = ROXs42B
            #find scaling ratio
        if targets[i]==2:
            psf = ROXs12
            #find scaling ratio

        im = im - s*psf
        fits.writeto('results/'+fileNames[i][:-5]+'.adi.fits',im)
