##Convolution using DoG (Differentiation of Gaussian) and LoG (Laplacian of Gaussian) kernels.
##Find Zero Crossings
##Set Threshold for zero crossing

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage

def plot(data, title):
    plot.i += 1
    plt.subplot(3,3,plot.i)
    plt.imshow(data)
    plt.gray()
    plt.title(title)
plot.i = 0

def function_zero_cross_threshold(Image,threshold=550,threshrequired=1):    
    zerocrossimg= np.zeros((len(Image), len(Image[0])))
    for i in range(len(Image)-1):
        for j in range(len(Image[0])-1):
            tlist=[]
            tlist.append(Image[i:i+2,j:j+2])
            if (np.sign(np.amax(tlist))*np.sign(np.amin(tlist))) <= -1:    
                if threshrequired==1:
                    if np.amax(tlist)-np.amin(tlist)>=threshold:
                        zerocrossimg[i][j]=1
                else:
                    zerocrossimg[i][j]=1    
    return zerocrossimg              

im=Image.open('Bridge.jpg')
data=np.array(im, dtype=float)
plot(data, 'original')

DoGkernel= np.array(([[0,0,-1,-1,-1,0,0],
                    [0,-2,-3,-3,-3,-2,0],
                    [-1,-3,5,5,5,-3,-1],
                    [-1,-3,5,16,5,-3,-1],
                    [-1,-3,5,5,5,-3,-1],
                    [0,-2,-3,-3,-3,-2,0],
                    [0,0,-1,-1,-1,0,0]]), np.float32)                        
DoGkernelFlipped= np.flipud(np.fliplr(DoGkernel))

DoGImage=ndimage.convolve2d(data, DoGkernelFlipped,mode='full', boundary='fill', fillvalue=0)

plot(DoGImage, 'DoG Image')

threshold=800               
no_Threshold=function_zero_cross_threshold(DoGImage,threshold,0)                 
plot(no_Threshold, 'No Threshold applied')
thresh_to_DoG=function_zero_cross_threshold(DoGImage,threshold,1)                 
plot(thresh_to_DoG, 'Threshold '+str(threshold)+'ZeroCross to DoG')

LoGkernel= np.array(([[0,0,1,0,0],
                        [0,1,2,1,0],
                        [1,2,-16,2,1],
                        [0,1,2,1,0],
                        [0,0,1,0,0]]), np.float32)                        
LoGkernelflipped= np.flipud(np.fliplr(LoGkernel))
LoGImage=ndimage.convolve2d(data, LoGkernelflipped,mode='full', boundary='fill', fillvalue=0)

plot(LoGImage, 'LoG image')

nothresh_to_LOG=function_zero_cross_threshold(LoGImage,threshold,0)
plot(nothresh_to_LOG,'No Threshold ZeroCross to LOG')
threshold=270
thresh_to_LOG=function_zero_cross_threshold(LoGImage,threshold,1)                        

plot(thresh_to_LOG,'Threshold '+str(threshold)+' ZeroCross to LOG')
plt.show()