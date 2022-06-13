#!/usr/bin/python3

# parse_zevsdir.py :
# naiive algorithm to find the ZEVS transmit frequency in vtnspec files
# this finds the frequency with the highest magnitude among the frequencies used by ZEVS
#
# write to stdout: the filename, frequency, frequency number and the ratio of rms magnitude of this frequency to the average rms magnitude of all ZEVS frequencies
#
# (c) 2022 Jacek Lipkowski <sq5bpf@lipkowski.org>
#
# this file is licensed under the GNU General Public License v3
#

from os import walk

#change this to the directory where you have all of your data
ZDIR="zevs_dir"

def find_peak(DIR,fname):
    filename=DIR+"/"+fname
    f=open(filename,"r")

    sdict={}
    nel=0
    mags=0

    for i in f:
        a=i.split(" ")
        #freq,mag
        sdict[round(float(a[0]),3)]=float(a[3])
        nel+=1
        mags+=float(a[3])

    if nel == 0 :
        return()

    avgmag=mags/float(nel)

    zfreqs=[80.8,81.0,81.2,81.4,81.6,81.8,82.0,82.2,82.4,82.6,82.8,83.0,83.2]
    odict={}
    peakz=0
    peaknum=0
    peakfreq=0
    avgz=0

    for i in range(len(zfreqs)):
        freq=zfreqs[i]
        odict[freq]=sdict[freq]
        avgz+=odict[freq]
        if odict[freq]>peakz:
            peakz=odict[freq]
            peakfreq=freq
            peaknum=i

    avgz=avgz/len(zfreqs)


    print(fname,peakfreq,peaknum,peakz/avgz)




### main
f = []
for (dirpath, dirnames, filenames) in walk(ZDIR):
    f.extend(filenames)

for i in f:
    find_peak(ZDIR,i)

# sorry, python is not my native language. your eyes will bleed --sq5bpf


