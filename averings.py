import numpy as np
import scipy.interpolate as intp
from astropy.io import fits
from astropy.io import ascii
import sys
import imageSubs as iS

print 'subtracting average radial profile (this may take a while)'

#load file names, target list and median psf
files = ascii.read('NIRC2_sci_20020_1.txt')
fileNames = np.array(files['fileNames'])
targets = np.array(files['target'])

o = 512 #psf center (origin)

n = np.size(targets)
for i in range(n):
    #exclude acquisition images
    if targets[i]!=0:
        #load and generate a non-discrete image
        im = fits.getdata('results/'+fileNames[i][:-5]+'.reg.fits')
        smoothim = intp.RectBivariateSpline(range(1024),range(1024),im)

        #prepare f(r,theta) for radial average
        f = np.zeros((300,360))
        R = np.arange(300)
        theta = np.arange(360)
        for r in R:
            for t in theta:
                trad = np.radians(t)
                xp = o + r*np.cos(trad)
                yp = o + r*np.sin(trad)
                f[r,t] = smoothim(yp,xp)

        #median over all theta for every r and generate a non-discrete function
        f = np.median(f, axis=1)
        smoothf = intp.interp1d(R,f,bounds_error=False,fill_value=f[299])

        #generate the r coordinate of every point in the image
        xp, yp = np.arange(1024),np.arange(1024)
        xg, yg = np.meshgrid(xp,yp)
        rp = np.sqrt((xg-o)**2 + (yg-o)**2)

        #subtract the subtracted image and output to file
        imsub = im - smoothf(rp)
        fits.writeto('results/'+fileNames[i][:-5]+'.ringsub.fits',imsub)

        #progress bar
        percent = float(i) / n
        hashes = '#' * int(round(percent * 20))
        spaces = ' ' * (20 - len(hashes))
        sys.stdout.write("\rPercent: [{0}] {1}%".format(hashes + spaces, int(round(percent * 100))))
        sys.stdout.flush()
sys.stdout.write("\n")

#register and stack images
positions = ascii.read('starPositions.txt')
positions['x'] = np.ones(n)*512
positions['y'] = np.ones(n)*512
xref, yref = 512., 512.

iS.register(2,'results/',fileNames,'ringsub.', targets, positions, (xref,yref))
