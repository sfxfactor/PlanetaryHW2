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

def findRatio(im,psf,(xc,yc),r,d):
    xs, ys = np.shape(im)
    ratios = np.array([])
    for i in range(xs):
        for j in range(ys):
            if (np.sqrt((i-xc)**2+(j-yc)**2)<r+d and np.sqrt((i-xc)**2+(j-yc)**2)>r):
                ratios = np.append(ratios,im[j,i]/psf[j,i])
    return np.median(ratios)

for i in range(n):
    if targets[i]!=0:
        im = fits.getdata('results/'+fileNames[i][:-5]+'.reg.fits')

        if targets[i]==1:
            psf = ROXs42B
        if targets[i]==2:
            psf = ROXs12
        s = findRatio(im,psf,(o,o),15,15)
        im = im - s*psf
        fits.writeto('results/'+fileNames[i][:-5]+'.adi.fits',im)


    percent = float(i) / n
    hashes = '#' * int(round(percent * 20))
    spaces = ' ' * (20 - len(hashes))
    sys.stdout.write("\rPercent: [{0}] {1}%".format(hashes + spaces, int(round(percent * 100))))
    sys.stdout.flush()
