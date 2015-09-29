from astropy.io import fits
from astropy.io import ascii
import numpy as np
from scipy.ndimage import interpolation as intp
import sys


def findStar(im, (xg, yg),r):
    x, y, tf = 0, 0, 0
    for i in range(-r,r+1):
        for j in range(-r,r+1):
            if (np.sqrt((i)**2+(j)**2)<=6):
                f = im[yg+i,xg+j]
                tf += f
                x += f*i
                y += f*j

    x = x/tf
    y = y/tf
    return (x+xg, y+yg)

def register(ntargets, directory, fileNames, extraTxt, targets, positions, (xref,yref)):
    print 'registering and stacking '+extraTxt
    n = np.size(targets)
    for t in range(1,ntargets+1):
        reg = np.array([])
        rot = np.array([])
        for i in range(n):
            if targets[i]==t:
                im = fits.getdata(directory+fileNames[i][:-4]+extraTxt+'fits')
                hdr = fits.getheader('calfits/'+fileNames[i])
                sim = intp.shift(im,[yref-positions['y'][i],xref-positions['x'][i]])
                fits.writeto('results/'+fileNames[i][:-4]+extraTxt+'reg.fits',sim)
                PA = hdr['PARANG']+hdr['ROTPPOSN']-hdr['EL']-hdr['INSTANGL']
                rim = intp.rotate(sim,-PA,reshape=False)
                if reg.sum()==0:
                    reg=np.array([sim])
                    rot=np.array([rim])
                else:
                    reg= np.append(reg,[sim],axis=0)
                    rot = np.append(rot,[rim],axis=0)

                percent = float(i) / n
                hashes = '#' * int(round(percent * 20))
                spaces = ' ' * (20 - len(hashes))
                sys.stdout.write("\rTarget {0}: Percent: [{1}] {2}%".format(t, hashes + spaces, int(round(percent * 100))))
                sys.stdout.flush()

        sumt= np.sum(reg,axis=0)
        fits.writeto('results/'+extraTxt+'target'+str(t)+'sum.fits', sumt)

        medt = np.median(reg,axis=0)
        fits.writeto('results/'+extraTxt+'target'+str(t)+'med.fits',medt)

        sumr = np.sum(rot,axis=0)
        fits.writeto('results/'+extraTxt+'target'+str(t)+'rotsum.fits',sumr)

        medr = np.median(rot,axis=0)
        fits.writeto('results/'+extraTxt+'target'+str(t)+'rotmed.fits',medr)
    sys.stdout.write("\n")

def findRatio(im,psf,mask): #(xc,yc),r,d):
    #xs, ys = np.shape(im)
    #ratios = np.array([])
    #for i in range(xs):
    #    for j in range(ys):
    #        if (np.sqrt((i-xc)**2+(j-yc)**2)<r+d and np.sqrt((i-xc)**2+(j-yc)**2)>r):
    #            ratios = np.append(ratios,im[j,i]/psf[j,i])
    #return np.median(ratios)
    ratio = (im/psf)*mask
    return np.median(ratio[np.where(mask!=0)])
