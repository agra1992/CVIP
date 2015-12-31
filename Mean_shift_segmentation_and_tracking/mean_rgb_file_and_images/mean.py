# -*- coding: utf-8 -*-
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
from scipy.spatial import distance
from collections import deque
from scipy import misc
from random import randrange

def plot(data, title):
    plot.i += 1
    plt.subplot(2,3,plot.i)
    plt.imshow(data)
    plt.gray()
    plt.title(title)
plot.i = 0

#C:\\Users\\Sahil\\mean_vid\\1.jpg
#Image_Butterfly.jpg
arr = misc.imread('Image_Butterfly.jpg') # 640x480x3 array
plot(arr,'original')
#arr=arr[200:400,200:400]
arr2 = misc.imread('Image_Butterfly.jpg') # 640x480x3 array
#arr2=arr2[200:400,200:400]

arr50=arr2.copy()
arr60=arr2.copy()


arr50.fill(0)
size=len(arr)*len(arr[0])

#***   (a)   **
#*** Perform mean shift discontinuity preserving filtering to the given images; Proper
#****parameters need to be selected


#5 dimentional feature vector array
vectors=np.empty([size,5], dtype=int)
count=0
for i in range(len(arr)):
    for j in range(len(arr[0])):
        vectors[count]=[arr[i][j][0],arr[i][j][1],arr[i][j][2],i,j]
        count=count+1
        
                      
r=randrange(0,len(vectors))
rem=[]

#*** first random vector which is checked for local maxima
t_mean=vectors[r]
some_count=0

#***store 5 dimensional vectors within a region for each local maxima
store_region={}

#*** (b) ***
#*** Store all information about the d-dimensional convergence points 𝐲𝑖,con
store_mean={}
store_rem={}
##hs and hr when mean shift iscontinuity preserving filtering is done
hs=40
hr=20

#shift vector to consider be compared with iter to confirm local maxima is reached
iter=5
store=[]

#*** until 5 D vectors has data we find local maximas
while(len(vectors)):
    try:                
        print 'len(vectors)'
        print len(vectors)
        for i in range(len(vectors)):
#****spacial and rande euclidean distance calculation            
            dsths = distance.euclidean(vectors[i][0:3],t_mean[0:3])
            dsthr = distance.euclidean(vectors[i][3:5],t_mean[3:5])
#            print 'here'
#            print dsths*dsthr
            prod=dsths*dsthr
#            print prod
            store.append(prod)
#            if(prod<7000):
            if (dsths<hs and dsthr<hr):
                rem.append(i)
#        print 'len rem'
#        print len(rem)
#        print 'l_vec'
#        print len(vectors)
        if(len(vectors)==0):
            break
        if(len(rem)==0):
            print 'ins'
            print len(vectors)
            r=randrange(0,len(vectors))
            rem=[]
            t_mean=vectors[r]
            continue                
        temp_vectors=vectors[rem]
#** Convergence point of a region in consideration is mean along column of the 5 D vectors in a region
        t_avg=temp_vectors.mean(axis=0)
#** Shift from of new Convergence point to previous one
        shift=distance.euclidean(t_mean[3:5],t_avg[3:5])
#        shift=distance.euclidean(t_mean[0:5],t_avg[0:5])
        print 'shift dist'
        print shift
#        print 'l_vec'
#        print len(vectors)
        if(len(vectors)==1):
            vectors=np.delete(vectors, rem, 0)
            store_rem[some_count]=rem
#*** Check if local maxima is reached else iterate again
        if(shift<iter and len(vectors)>1):

#            if(len(rem)>0):
            if(1):
                no_boundary=0;
                if(no_boundary==0):
                    for key in rem:                    
                        arr2[vectors[key][3]][vectors[key][4]][0]=t_avg[0]
                        arr2[vectors[key][3]][vectors[key][4]][1]=t_avg[1]
                        arr2[vectors[key][3]][vectors[key][4]][2]=t_avg[2]

#*** Delete 5 D feature vectors when local maxima is found out
            vectors=np.delete(vectors, rem, 0)
#*** Restart from a random point as mean
            r=randrange(0,len(vectors))
            rem=[]
            t_mean=vectors[r]

            store_rem[some_count]=rem
#*** Store on key values each region mean/ locatl maxima
            store_mean[some_count]=t_avg
#*** Store on key values each region 5D vectors
            store_region[some_count]=temp_vectors
            some_count=some_count+1
#            print 'some count'
#            print some_count
            if(some_count==1):
                arr3=arr2.copy()
                
                plot(arr3,'found maxima 1')
            if(some_count==10):
                arr4=arr2.copy()
                plot(arr4,'found maxima 10')
            if(some_count==15):
                arr5=arr2.copy()
#                plot(arr5,'found maxima 15')
        else:
#*** NO local maxima found reiterate with mean as new Convergence point mean
            rem=[]
            t_mean=t_avg
        print 'end'
    except ValueError:
        print "Oops!  Some try catch error"    


#*** (c) ****
#** Determine the clusters {𝐂𝑝}by grouping all which are closer than in the spatial domain and 
#*** in the range domain. That is, merge the basins of attraction of these convergence points


#**** REGION MERGING
hs_region=80
hr_region=75
merged_region_size_threshold=350

#*** Means of the regions under hs_region region into consideration to be merged
#** Average with these values will be assigned to all the regions merged
store_current_mean={}

while(len(store_mean.keys())):
    reg_mean=store_mean[store_mean.keys()[0]]
    store_current_mean[store_mean.keys()[0]]=reg_mean
    count=1
    for j in store_mean.keys():
        color = distance.euclidean(reg_mean[0:3],store_mean[j][0:3])
        space = distance.euclidean(reg_mean[3:5],store_mean[j][3:5])
        if(color<hs_region):# and space<hr_region
#            print j
            store_current_mean[j]=store_mean[j]
            count=count+1
    compute_array=np.array(store_current_mean.values(), dtype=float)
    compute_mean=compute_array.mean(axis=0)
    keys=store_current_mean.keys()
    
    empty1=arr2.copy()
    empty1.fill(0)
    
#*** merged region pixels count to ignore small regions
    combined_region_pixels_count=0
    for eachkey in keys:    
        actual_key=eachkey
        each_region=store_region[actual_key]
        for m in range(len(store_region[actual_key])):            
            combined_region_pixels_count=combined_region_pixels_count+1
# **** (e) ****
#*** Select a proper parameter P so that regions smaller than P pixels will be eliminated.
    if(combined_region_pixels_count<merged_region_size_threshold):
        for eachkey in keys:        
            actual_key=eachkey
            each_region=store_region[actual_key]
            for m in range(len(store_region[actual_key])):
                arr50[each_region[m][3]][each_region[m][4]]=arr[each_region[m][3]][each_region[m][4]]
            del store_mean[actual_key]
        store_current_mean={}                                
    else: 
        
#***** (d) *****
#****Assign 𝐿𝑖 = {𝑝|𝐳𝑖 ∈ 𝐂𝑝} for each pixel 𝑖 = 1, … ,n 

        for eachkey in keys:
            actual_key=eachkey
            each_region=store_region[actual_key]
            for m in range(len(store_region[actual_key])):            
    #*** New empty array will be filled in all the indices of the regions merged by ther averge of local maximas RGB value
                arr50[each_region[m][3]][each_region[m][4]]=[compute_mean[0],compute_mean[1],compute_mean[2]]
                empty1[each_region[m][3]][each_region[m][4]]=50
            del store_mean[actual_key]
        store_current_mean={}
    
    #*** Boundary of each reach marked by blue color
        try:
            for qwe in range(len(empty1)-2):
                for rty in range(len(empty1[0])-2):
                    if empty1[qwe][rty][0]!=empty1[qwe][rty+1][0]:
                        arr60[qwe][rty-1]=[0,0,255]
                        arr60[qwe][rty]=[0,0,255]
                        arr60[qwe][rty+1]=[0,0,255]                                                
                    if empty1[qwe][rty][0]!=empty1[qwe+1][rty][0]:
                        arr60[qwe-1][rty]=[0,0,255]
                        arr60[qwe][rty]=[0,0,255]
                        arr60[qwe+1][rty]=[0,0,255]                                                
        except ValueError:
            print "Oops!  Boundary out of image"             
#*** (e) ***
#**Visualize properly the mean shift segmentation results for the selected test images                         

                                                                           
                                                                                                                                                                                                                                 
plot(arr2,'means shift filter preserving hs '+str(hs)+' hr '+str(hr)+' iter '+str(iter))
plot(arr50,'Region merged hs_region '+str(hs_region)+' hs_region')
plot(arr60,'Boundary merged hs_region '+str(hs_region)+' hs_region')
#plt.imshow(arr2)
plt.show()



#*** (f) ****
#*** Bonus (5%): Perform the mean shift algorithm for track objects over image sequences
#****(see reference [5] for algorithmic details)

# in another python file
#***vid.py