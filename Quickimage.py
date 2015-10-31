# -*- coding: utf-8 -*-
"""
Spyder Editor
This is a temporary script file.
"""
# 001V image has an airplane
# Some of the brighter stars are saturated

import pyfits as pf
import matplotlib.pyplot as plt
import numpy as np
import robust as rb
import glob,os
import img_scale
import hcongrid as h

def readimage(imfile,plot=False,siglo=3,sighi=7):
    image,header = pf.getdata(imfile,0,header=True)
    np.median(image)
    med = np.median(image)
    sig = rb.std(image)
    if plot:
        plt.ion()
        plt.figure()
        vmax = med + 5*sig
        vmin = med - 2*sig
        plt.imshow(image,vmin=vmin,vmax=vmax,cmap='gray')

    return image,header
    
def show_image(image,siglo=3,sighi=7):
    med = np.median(image)
    sig = rb.std(image)   
    plt.ion()
    plt.figure()
    vmin = med - siglo*sig    
    vmax = med + sighi*sig
    plt.imshow(image,vmin=vmin,vmax=vmax,cmap='gray')
    return

    
def makeband(band='V'):
    
    files = glob.glob('Mantis*[0-9]'+band+'_cal.fit*')
    zsz = len(files)
    reffile = files[zsz/2]
    image0,header0 = readimage(reffile)
    ysz,xsz = np.shape(image0)
    
    refim = h.pyfits.open(reffile)
    refh = h.pyfits.getheader(reffile)
    
    stack = np.zeros((xsz,ysz,zsz))
    for i in range(zsz):
       im = h.pyfits.open(files[i])
       newim = h.hcongrid(im[0].data,im[0].header,refh)
       stack[:,:,i] = newim
       
    final = np.median(stack,axis=2)
    
    if band == 'V':
        tag = 'Blue'
        
    if band == 'R':
        tag = 'Green'
        
    if band == 'ip':
        tag = 'Red'
        
    test = glob.glob(tag+'.fit')
    if test:
        os.remove(tag+'.fit')
    pf.writeto(tag+'.fit',final,header0)
    
def make_RGB():

    Blue,header = pf.getdata('Blue.fit',0,header=True)
    Green,header = pf.getdata('Green.fit',0,header=True)
    Red,header = pf.getdata('Red.fit',0,header=True)

    G = h.pyfits.open('Green.fit')
    Gh = h.pyfits.getheader('Green.fit')
    
    B = h.pyfits.open('Blue.fit')
    Bh = h.pyfits.getheader('Blue.fit')
    
    R = h.pyfits.open('Red.fit')
    Rh = h.pyfits.getheader('Red.fit')

    Bnew = h.hcongrid(B[0].data,B[0].header,Gh)
    Rnew = h.hcongrid(R[0].data,R[0].header,Gh)
    
    Blue = Bnew
    Green,header = readimage('Green.fit')
    Red = Rnew

    bmed = np.median(Blue)
    gmed = np.median(Green)
    rmed = np.median(Red)
    
    bsig = rb.std(Blue)
    gsig = rb.std(Green)
    rsig = rb.std(Red)
    
    final = np.zeros((Blue.shape[0],Blue.shape[1],3),dtype=float)  
    
    sigmin = 0.25
    sigmax = 5
    
    final[:,:,0] = img_scale.sqrt(Red,scale_min=rmed+sigmin*rsig,scale_max=rmed+0.6*sigmax*rsig)
    final[:,:,1] = img_scale.sqrt(Green,scale_min=gmed+sigmin*gsig,scale_max=gmed+0.6*sigmax*gsig)
    final[:,:,2] = img_scale.sqrt(Blue,scale_min=bmed+sigmin*bsig,scale_max=bmed+0.6*sigmax*bsig)
    
    plt.ion()
    plt.figure(99)
    plt.imshow(final,aspect='equal')

    return
    


    




