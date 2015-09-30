import numpy as np
import scipy.interpolate as intp
from astropy.io import fits
from astropy.io import ascii
import sys
import imageSubs as iS

print 'matching psf (BDI?)'

#get file names and target list
files = ascii.read('NIRC2_sci_20020_1.txt')
fileNames = np.array(files['fileNames'])
targets = np.array(files['target'])
o = 512 #psf center (origin)


#prepare output file
f = open('bestFitPSF.txt','w')
f.write('image\tbestMatch\n')

#create mask- 1's in a ring from r=10-30 pixels, 0 otherwise
mask = np.zeros((1024,1024))
for i in range(1024):
    for j in range(1024):
        if (np.sqrt((i-o)**2+(j-o)**2)<30 and np.sqrt((i-o)**2+(j-o)**2)>10):
            mask[j,i]=1.


n = np.size(targets)
for i in range(n):
    #exclude acquisition images
    if targets[i]!=0:
        #get data and prepare arrays for xhi^2 and scaling ratios
        im = fits.getdata('results/'+fileNames[i][:-5]+'.reg.fits')
        Chi = np.ones(n)*np.inf
        ss = np.zeros(n)

        for j in range(n):
            #loop over images of the other target
            if (targets[i]==1 and targets[j]==2) or (targets[i]==2 and targets[j]==1):
                tim = fits.getdata('results/'+fileNames[j][:-5]+'.reg.fits')
                #find scaling ratio and chi^2
                ss[j] = findRatio(im,tim,mask)
                Chi[j] = np.sum((im - ss[j]*tim)**2) ### what to use for sigma???
                #progress bar
                percent1 = float(i) / n
                hashes1 = '#' * int(round(percent1 * 20))
                spaces1 = ' ' * (20 - len(hashes1))
                percent2 = float(j) / n
                hashes2 = '#' * int(round(percent2 * 20))
                spaces2 = ' ' * (20 - len(hashes2))
                sys.stdout.write("\rImages: [{0}] {1}%\tTemplates: [{2}] {3}%".format(hashes1 + spaces1, int(round(percent1 * 100)),hashes2+spaces2, int(round(percent2*100))))
                sys.stdout.flush()

        #find and write min chi^2
        best = np.argmin(Chi)
        f.write(fileNames[i]+'\t'+fileNames[best]+'\n')
        
        #output subtracted image
        sim = im - ss[best]*fits.getdata('results/'+fileNames[best][:-5]+'.reg.fits')
        fits.writeto('results/'+fileNames[i][:-5]+'.bdi.fits',sim)

sys.stdout.write("\n")
f.close()

#register and stack bdi images
positions = ascii.read('starPositions.txt')
positions['x'] = np.ones(n)*512
positions['y'] = np.ones(n)*512
xref, yref = 512., 512.

iS.register(2,'results/',fileNames,'bdi.', targets, positions, (xref,yref))
