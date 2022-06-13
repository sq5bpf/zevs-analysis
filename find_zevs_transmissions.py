#!/usr/bin/python3

# find_zevs_transmissions.py:
# naiive algorithm to find the ZEVS messages in the file produced by parse_zevsdir.py
# this looks for 82Hz, some message in MFSK (tones other than 82Hz), 82Hz
#
# note: we are treating each sample separately (as produced by parse_zevsdir.py), 
# while we should look at the magnitude of the ZEVS frequencies in all samples 
# in each symbol. this would yield much better decodes in case of interference
#
# write to stdout: 
# time, number of frequencies, the MFSK message, the same message in easy to read ascii format, number of times this message was seen
#
#
# (c) 2022 Jacek Lipkowski <sq5bpf@lipkowski.org>
#
# this file is licensed under the GNU General Public License v3
#


from datetime import datetime, timezone

F="testwy3"

lastfreq=0.0
numsamples=16*4
timediff=60

com=""



def fillzero():
    global numsamples
    slst=[]
    for i in range(numsamples):
        slst.append(0)
    return(slst)

    

# given 4 samples, find the most probable frequency
# output probability,frequency
def findtone(lst):
    b={}
    probmax=0
    tonemax=0

    for i in set(lst[-4:]):
        b[i]=lst.count(i)
        if b[i] > probmax:
            probmax=b[i]
            tonemax=i

    if probmax==4 or probmax==3:
        return(probmax/4,tonemax)
    elif probmax==2 and (len(b)==3):
        return(probmax/4,tonemax)

    return(0,0)


# go through the tone buffer, try to find the tones in it
def findtones(lst):
    tones=[]
    b=0
    

    while b<len(lst):
        p,t=findtone(lst[b:b+4])
        tones.append([t,p])
        b+=4
    return(tones)

# find a message: 82Hz + some tones + 82Hz
def findseq(lst):
    STATE_NOISE=0
    STATE_82HZ=1
    STATE_TRANSMISSION=2
    state=STATE_NOISE


    tones=findtones(lst)
    rx=[]
    tidx=0
    nt=0
    np=0.0

    for b in tones:
        tidx+=1
        if b[1]==0:
            state=STATE_NOISE
            continue
        if state==STATE_NOISE and b[0]==82.0:
            state=STATE_82HZ
            continue

        if state==STATE_82HZ and b[0] != 82.0:
            state=STATE_TRANSMISSION
            nt=0
            np=0.0
            rx=[]

        if state==STATE_TRANSMISSION:
            if b[0]==82.0:
                state==STATE_82HZ
                if len(rx)>0:
                    return(nt,np/nt,rx,tidx-1)
            else:
                rx.append(b[0])
                nt+=1
                np+=b[1]

    return(0,0,[],0)



# convert the tones to easily readable text. it's easier to compare the output by eye
def tones2str(lst):
    zfreqs={ 80.8: "A" ,81.0:"b" , 81.2:"C" , 81.4:"d" , 81.6:"E" , 81.8:"f" , 82.0:"G" , 82.2:"h" , 82.4:"I" , 82.6:"j" , 82.8:"K" , 83.0:"l" , 83.2:"M" }
    a=""
    for i in lst:
        if i in zfreqs:
            a+=zfreqs[i]
        else:
            a+="_"
    return(a)    



prevtime=0
slst=fillzero()
decodes={}

f=open(F,"r")

for i in f:
    i=i.strip()
    a=i.split(" ")

    t=int(a[0])

    if (t-prevtime) == timediff:
        nt,prob,rx,samp=findseq(slst)
        if prob>0.8:
            starttime=t+(timediff*samp*4)-(timediff*nt*4)-(numsamples*timediff)
            #print("time:",t," start:",starttime," samp:",samp,"   nt:",nt," rx:",rx," prob:",prob)
            if not starttime in decodes:
                ss=tones2str(rx)
                
                decodes[starttime]=[nt,prob,"tones: "+str(rx),ss]
            
    else:
        #not continious time
        slst=fillzero()

    prevtime=t
    slst.pop(0)
    slst.append(float(a[1]))
    




f.close()

# find if we can delete some decodes
# the above algorithm will show a decode with 0.75 probability when the start of symbol is misaligned by one sample
# we will try to make a list of these misaligned decodes, so that we can delete them
todel=[]
for k,v in decodes.items():
    if k in decodes:
        pr1=decodes[k][1]
    else:
        pr1=0
    if k+timediff in decodes:
        pr2=decodes[k+timediff][1]
    else:
        pr2=0

    if k+2*timediff in decodes:
        pr3=decodes[k+2*timediff][1]
    else:
        pr3=0

    if pr2>pr1 and pr1!=0:
       todel.append(k) 

    if pr2>pr3 and pr3!=0:
        todel.append(k+2*timediff)

for i in todel:
    del decodes[i]


#count the times each message appeared. thought might be interesting to check if they repeat (they do, but not often)
calls={}
for k,v in decodes.items():
    if v[3] in calls:
        calls[v[3]]+=1
    else:
        calls[v[3]]=1




for k,v in decodes.items():
    dt = datetime.fromtimestamp( k, tz=timezone.utc )
    print(dt,"     |  ",v[0],v[2],"   ",v[3],"(",calls[v[3]],")")

# sorry, python is not my native language. your eyes will bleed --sq5bpf

