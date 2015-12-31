from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
from scipy.spatial import distance
from collections import deque
from scipy import misc
from random import randrange
import cv2
def plot(data, title):
    plot.i += 1
    plt.subplot(4,4,plot.i)
    plt.imshow(data)
    plt.gray()
    plt.title(title)
plot.i = 0


#Read a list of images        
#Images are cut from a video frames gap

#Starting position of for first meanover the object instead of any random vector
start_dustbin_images_=7031
start_basketball_images=21378
#Change at line 54 to assign first index for mean to track(A point on the object)

hs=15
hr=40                
                                                
t_mean=[]
for i in range(1,17):
    try:
        print i
        fname=str(i)+'.jpg'
        arr = misc.imread("mean_basket\\"+fname) # 640x480x3 array
    #    im=Image.open("C:\\Users\\Sahil\\mean_vid\\"+fname)
    #    arr=np.array(im, dtype="np.unit8")
        #arr=arr[0:200,0:200]
        arr2 = misc.imread("mean_basket\\"+fname) # 640x480x3 array
        #arr2=arr2[0:200,0:200]
        size=len(arr)*len(arr[0])
    
        #vectors=np.zeros((size,5))
        vectors=np.empty([size,5], dtype=int)
        count=0
        for p in range(len(arr)):
            for j in range(len(arr[0])):
                vectors[count]=[arr[p][j][0],arr[p][j][1],arr[p][j][2],p,j]
                count=count+1       
        #r=randrange(0,len(vectors))
        if(i==1):
#            print 'here'
            #r=7031#dusbin start
            r=start_basketball_images
            t_mean=vectors[r]
            print 'Start_mean'
            print t_mean
            xb=int(round(t_mean[3]))
            yb=int(round(t_mean[4]))
            arr[xb-1][yb]=[0,255,255]
            arr[xb][yb-1]=[0,255,255]
            arr[xb+1][yb]=[0,255,255]
            arr[xb][yb+1]=[0,255,255]
        else:
            xb=int(round(t_mean[3]))
            yb=int(round(t_mean[4]))
        #pl=square(arr,xx,yy)
        
        rem=[]
        some_count=0
        store_rem={}
                
#        print 'len(vectors)'
#        print len(vectors)
        for hh in range(len(vectors)):
    #        dst = distance.euclidean(vectors[hh],t_mean)
            dsths = distance.euclidean(vectors[hh][0:3],t_mean[0:3])
            dsthr = distance.euclidean(vectors[hh][3:5],t_mean[3:5])
            #print dst
            #if(dsths<60) and (dsthr<60):#dust
            if(dsths<hs) and (dsthr<hr):
                rem.append(hh)
#        print 'len rem'
#        print len(rem)
        temp_vectors=vectors[rem]
        t_avg=temp_vectors.mean(axis=0)
        print 'Calculated mean'
        print t_avg
        
#        print i
#        print 't_avg'
#        print t_avg
        t_mean=t_avg
        print 'mean for new window'
        print t_avg        
        xx=int(round(t_mean[3]))
        yy=int(round(t_mean[4]))
        #pl=square(arr,xx,yy)
        arr[xx-1][yy]=[0,255,255]
        arr[xx][yy-1]=[0,255,255]
        arr[xx+1][yy]=[0,255,255]
        arr[xx][yy+1]=[0,255,255]
        
        k=20
#        k=int(len(rem)/50)
        try:
            for m in range(xx-k,xx+k):
                arr[m][yy-k]=[0,0,0]
                arr[m][yy+k]=[0,0,0]
            for n in range(yy-20,yy+20):
                arr[xx-k][n]=[0,0,0]
                arr[xx+k][n]=[0,0,0]
            for m in range(xx-k+2,xx+k+2):
                arr[m][yy-k]=[0,0,0]
                arr[m][yy+k]=[0,0,0]
            for n in range(yy-k+2,yy+k+2):
                arr[xx-k][n]=[0,0,0]
                arr[xx+k][n]=[0,0,0]
        except ValueError:
            print "Oops!  Some try catch error"   
        if(i!=1):
            cv2.line(arr,(yb,xb),(yy,xx),(0,255,0),2)  
        plot(arr,'new 5dmean ['+str(int(round(t_mean[0])))+' '+str(int(round(t_mean[1])))+' '+str(int(round(t_mean[2])))+' '+str(int(round(t_mean[3])))+' '+str(int(round(t_mean[4])))+']')
    except ValueError:
        print "Oops!  That was no valid number.  Try again..."                  

plt.show()    
        

                