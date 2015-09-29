import numpy as np
import scipy.interpolate as intp
from astropy.io import fits
from astropy.io import ascii
import sys
import imageSubs as iS

print 'subtracting psf (ADI)'

files = ascii.read('NIRC2_sci_20020_1.txt')
fileNames = np.array(files['fileNames'])
targets = np.array(files['target'])

ROXs42B = fits.getdata('results/target1med.fits')
ROXs12 = fits.getdata('results/target2med.fits')
o = 512 #psf center (origin)

#create mask
mask = np.zeros((1024,1024))
for i in range(1024):
    for j in range(1024):
        if (np.sqrt((i-o)**2+(j-o)**2)<30 and np.sqrt((i-o)**2+(j-o)**2)>10):
            mask[j,i]=1.

n = np.size(targets)
for i in range(n):
    if targets[i]!=0:
        im = fits.getdata('results/'+fileNames[i][:-5]+'.reg.fits')

        if targets[i]==1:
            psf = ROXs42B
        if targets[i]==2:
            psf = ROXs12
        s = iS.findRatio(im,psf,mask)#(o,o),15,15)
        im = im - s*psf
        fits.writeto('results/'+fileNames[i][:-5]+'.adi.fits',im)


    percent = float(i) / n
    hashes = '#' * int(round(percent * 20))
    spaces = ' ' * (20 - len(hashes))
    sys.stdout.write("\rPercent: [{0}] {1}%".format(hashes + spaces, int(round(percent * 100))))
    sys.stdout.flush()
sys.stdout.write("\n")

#register adi images
positions = ascii.read('starPositions.txt')
positions['x'] = np.ones(n)*512
positions['y'] = np.ones(n)*512
xref, yref = 512., 512.

iS.register(2,'results/',fileNames,'adi.', targets, positions, (xref,yref))
