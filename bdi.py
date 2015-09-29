import numpy as np
import scipy.interpolate as intp
from astropy.io import fits
from astropy.io import ascii
import sys
import imageSubs as iS

print 'matching psf (BDI?)'

files = ascii.read('NIRC2_sci_20020_1.txt')
fileNames = np.array(files['fileNames'])
targets = np.array(files['target'])

ROXs42B = fits.getdata('results/target1med.fits')
ROXs12 = fits.getdata('results/target2med.fits')
o = 512 #psf center (origin)

n = np.size(targets)


def findRatio(im,psf,mask):
    ratio = (im/psf)*mask
    return np.median(ratio[np.where(mask!=0)])

f = open('bestFitPSF.txt','w')
f.write('image\tbestMatch\n')

#create mask
mask = np.zeros((1024,1024))
for i in range(1024):
    for j in range(1024):
        if (np.sqrt((i-o)**2+(j-o)**2)<30 and np.sqrt((i-o)**2+(j-o)**2)>10):
            mask[j,i]=1.

for i in range(n):
    if targets[i]!=0:
        im = fits.getdata('results/'+fileNames[i][:-5]+'.reg.fits')
        Chi = np.ones(n)*np.inf
        ss = np.zeros(n)

        for j in range(n):
            if (targets[i]==1 and targets[j]==2) or (targets[i]==2 and targets[j]==1):
                tim = fits.getdata('results/'+fileNames[j][:-5]+'.reg.fits')
                ss[j] = findRatio(im,tim,mask)
                Chi[j] = np.sum((im - ss[j]*tim)**2) ### what to use for sigma???
                percent1 = float(i) / n
                hashes1 = '#' * int(round(percent1 * 20))
                spaces1 = ' ' * (20 - len(hashes1))
                percent2 = float(j) / n
                hashes2 = '#' * int(round(percent2 * 20))
                spaces2 = ' ' * (20 - len(hashes2))
                sys.stdout.write("\rImages: [{0}] {1}%\tTemplates: [{2}] {3}%".format(hashes1 + spaces1, int(round(percent1 * 100)),hashes2+spaces2, int(round(percent2*100))))
                sys.stdout.flush()

        best = np.argmin(Chi)
        f.write(fileNames[i]+'\t'+fileNames[best]+'\n')
        
        sim = im - ss[best]*fits.getdata('results/'+fileNames[best][:-5]+'.reg.fits')
        fits.writeto('results/'+fileNames[i][:-5]+'.bdi.fits',sim)
sys.stdout.write("\n")

#register bdi images
positions = ascii.read('starPositions.txt')
positions['x'] = np.ones(n)*512
positions['y'] = np.ones(n)*512
xref, yref = 512., 512.

iS.register(2,'results/',fileNames,'bdi.', targets, positions, (xref,yref))
