from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
from collections import deque

def plot(data, title):
    plot.i += 1
    plt.subplot(1,2,plot.i)
    plt.imshow(data)
    plt.gray()
    plt.title(title)
plot.i = 0

#merge two regions
#empty on adjacency into other one
def merge_2_region(a,b):
    global regions_data
    global tree_adj_list
    global region_means
    global region_sum
    global region_size
    for i in range(len(regions_data)):
        for j in range(len(regions_data[0])):
            if regions_data[i][j]==b:
                regions_data[i][j]=a
    try:
        region_sum[a]=region_sum[a]+region_sum[b]
        region_size[a]=region_size[a]+region_size[b]-1
        try:        
            region_means[a]=region_sum[a]/region_size[a]
        except IndexError:
            do_nothing=1
        tree_adj_list[a]=tree_adj_list[a]+tree_adj_list[b]
        tree_adj_list[b]=[]
    except IndexError:
        do_nothing=1
    return tree_adj_list,regions_data,region_means,region_sum,region_size    

#from regions array as mark boundaries on region change verticaly or horizontaly
def region_to_boundary_original_smaller_regions(regions_data,region_size,original_cp):
    for i in range(len(regions_data)-1):
        for j in range(len(regions_data[0])-1):     
            if regions_data[i][j]!=regions_data[i+1][j]:
                original_cp[i][j]=255
                original_cp[i+1][j]=255
            if regions_data[i][j]!=regions_data[i][j+1]:
                original_cp[i][j]=255
                original_cp[i][j+1]=255
    return original_cp

#ignoring smaller regions
def region_to_boundary_original(threshold,regions_data,region_size,original_cp_small):
    for i in range(len(regions_data)-1):
        for j in range(len(regions_data[0])-1):     
            if regions_data[i][j]!=regions_data[i+1][j] and region_size[regions_data[i][j]]>threshold and region_size[regions_data[i+1][j]]>threshold:
                original_cp_small[i][j]=255
                original_cp_small[i+1][j]=255
            if regions_data[i][j]!=regions_data[i][j+1] and region_size[regions_data[i][j]]>threshold and region_size[regions_data[i][j+1]]>threshold:
                original_cp_small[i][j]=255
                original_cp_small[i][j+1]=255
    return original_cp_small
    
im=Image.open('Peppers.jpg')

data=np.array(im, dtype=float)

original_cp=np.array(im, dtype=float)
original_cp_small=np.array(im, dtype=float)

#regions string array initiated to 0
regions_data=np.array(im, dtype=str)

#data=data[100:270,100:270]
#original_cp=original_cp[100:270,100:270]
#original_cp_small=original_cp_small[100:270,100:270]
#regions_data=regions_data[100:270,100:270]

regions_data[:] = '0'

#plot(data, 'original')

threshold=10
region_count=1

# p array will find '0' in data and we extract first position of '0' (not covered in any region)
#Qx Qy queues to maintain the next indices on which 4 neighbours are checked for threshold difference 
# Recursive function gave the error of out of stack memory so Queue is used
#regions assigned as rg1 rg2 rg3

p=np.where(regions_data == str(0))
while len(p[0]):

    x=p[0][0]
    y=p[1][0]
    Qx=deque([x],262144)
    Qy=deque([y],262144)
    regions_data[x][y]='rg'+str(region_count)

    while len(Qx)!=0 :

        x=Qx.popleft()
        y=Qy.popleft()
        try:
            if regions_data[x-1][y]==str(0) and abs(data[x][y]-data[x-1][y])<threshold: 

                Qx.append(x-1)
                Qy.append(y)
                regions_data[x-1][y]='rg'+str(region_count)
        except IndexError:
            do_nothing=1
        try:
            if regions_data[x+1][y]==str(0) and abs(data[x][y]-data[x+1][y])<threshold:

                Qx.append(x+1)
                Qy.append(y)
                regions_data[x+1][y]='rg'+str(region_count)
        except IndexError:
            do_nothing=1
        try:
            if regions_data[x][y+1]==str(0) and abs(data[x][y]-data[x][y+1])<threshold:
                Qx.append(x)
                Qy.append(y+1)
                regions_data[x][y+1]='rg'+str(region_count)
        except IndexError:
            do_nothing=1
        try:
            if regions_data[x][y-1]==str(0) and abs(data[x][y]-data[x][y-1])<threshold:
                Qx.append(x)
                Qy.append(y-1)
                regions_data[x][y-1]='rg'+str(region_count)
        except IndexError:
            do_nothing=1
    region_count=region_count+1
    p=np.where(regions_data == str(0))
    
#

region_sum={}
region_size={}
region_means={}
frozen_region={}
tree_adj_list={}
for i in range(1,region_count):
    tree_adj_list['rg'+str(i)]=[]
    frozen_region['rg'+str(i)]='n'


#Adjacency list for regions conectivity in tree structure
for i in range(len(regions_data)-1):
    for j in range(len(regions_data[0])-1):
        if regions_data[i][j]!=regions_data[i+1][j] and regions_data[i+1][j] not in tree_adj_list[regions_data[i][j]]:
            tree_adj_list[regions_data[i][j]].append(regions_data[i+1][j])

for i in range(len(regions_data)-1):
    for j in range(len(regions_data[0])-1):
        if regions_data[i][j]!=regions_data[i][j+1] and regions_data[i][j+1] not in tree_adj_list[regions_data[i][j]]:
            tree_adj_list[regions_data[i][j]].append(regions_data[i][j+1])
 
#means for every region in 
for i in range(region_count):
    arr2=np.ma.masked_where(regions_data=='rg'+str(i), regions_data)
    sub=data[arr2.mask]
    region_sum['rg'+str(i)]=sum(sub)
    region_size['rg'+str(i)]=len(sub)
    region_means['rg'+str(i)]=region_sum['rg'+str(i)]/region_size['rg'+str(i)]

    
#for iterate in range(1):
#merge_all_regions using means
for j in tree_adj_list:              
    for i in tree_adj_list[j]:
        if abs(region_means[i]-region_means[j])<threshold:
            merge_2_region(j,i)


#length=len(tree_adj_list)
#for i in range(1,length):
#    if tree_adj_list['rg'+str(i)]==[]:
#        del tree_adj_list['rg'+str(i)]
threshold=10
original_cp_small=region_to_boundary_original(threshold,regions_data,region_size,original_cp_small)
threshold=3000
original_cp=region_to_boundary_original(threshold,regions_data,region_size,original_cp)

plot(original_cp_small,'Region boundary marked including smaller')
plot(original_cp,'Region boundary marked')
plt.show()   