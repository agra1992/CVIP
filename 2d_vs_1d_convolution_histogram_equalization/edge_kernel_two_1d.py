## Convolution with edge kernel
## with two 1d kernels instead of 2d kernel

import matplotlib.pyplot as plt
import numpy as np
from scipy import ndimage
from PIL import Image
import time

def plot(data, title):
    plot.i += 1
    plt.subplot(3,4,plot.i)
    plt.imshow(data)
    plt.gray()
    plt.title(title)
plot.i = 0


def function_convolve(full,kernel):
    
    full=np.lib.pad(full, ((2,2),(2,2)), 'constant', constant_values=(0))
    convolved=np.zeros([len(full),len(full[0])])
    kernel=np.flipud(np.fliplr(kernel))
    dy=len(kernel)
    dx=len(kernel[0])

    stop_cumm=0
    time_diff=0.0
    time_diff_temp=0.0
    for y in range(len(full)):
        for x in range(len(full[0])): 
              
            if(x>2 and x<len(full[0])-2 and y>2 and y<len(full)-2) :                
                if (dy>2 and dx>2):

                    first=full[y-(dy/2):y+((dy/2)+1),x-(dx/2):x+((dx/2)+1)]

                elif(dx>2):
                    first=full[y,x-(dx/2):x+((dx/2)+1)]
                elif(dy>2):
                    first=full[y-(dy/2):y+((dy/2)+1),x]
                    first=first[:, None] 
                else:
                    first=full[y,x]                    
                second=kernel
                start_time = time.time() 
                together=first*second
                time_diff_temp=time.time()-start_time                                           
                t=sum(sum(together))

                convolved[y][x]=t
    
            time_diff=time_diff+time_diff_temp
                            
    convolved=convolved[2:-2,2:-2]            
    return convolved,time_diff



im = Image.open('lena_gray.png')
data = np.array(im, dtype=float)
#data=data[1:200]
plot(data, 'Original')




kernel = np.array([[1],
                   [2],
                   [1]])



self_gxa,total_dx_a=function_convolve(data,kernel)                   
plot(self_gxa, 'Self Connvolve GX_A '+str(total_dx_a))
                                                                           
inbuilt_gxa = ndimage.convolve(data, kernel)

plot(inbuilt_gxa, 'inbuilt GX_A')


kernel = np.array([[-1, 0, 1]])

self_convolved_gxb,total_dx_b=function_convolve(self_gxa,kernel)

plot(self_convolved_gxb, 'Self CONVOLVED GX_B '+str(total_dx_b))

inbuilt_gxb = ndimage.convolve(inbuilt_gxa, kernel)

plot(inbuilt_gxb, 'Inbuilt GX_B')




kernel = np.array([[-1],
                   [0],
                   [1]])


self_convolved_gya,total_dy_a=function_convolve(data,kernel)
plot(self_convolved_gya, 'self CONVOLVED GY_A '+str(total_dy_a))

DY = ndimage.convolve(data, kernel)
plot(DY, 'Inbuilt GY_A')


kernel = np.array([[1, 2, 1]])

self_convolved_gyb,total_dy_b=function_convolve(self_convolved_gya,kernel)

plot(self_convolved_gyb, 'self CONVOLVED GY_B '+str(total_dy_b))


DY = ndimage.convolve(DY, kernel)
plot(DY, 'inbuilt GY_B')

new=np.sqrt(np.square(inbuilt_gxb)+np.square(DY))
new_c=np.sqrt(np.square(self_convolved_gxb)+np.square(self_convolved_gyb))
plot(new, 'Inbuilt func convolve')
plot(new_c, 'Self Convolved G '+str(total_dx_a+total_dx_b+total_dy_a+total_dy_b))
print 'total time of mul total_dx_a '+str(total_dx_a)
print 'total time of mul total_dx_b '+str(total_dx_b)
print 'total time of mul total_dy_a '+str(total_dy_a)
print 'total time of mul total_dy_b '+str(total_dy_b)
print 'total time of mul Total '+str(total_dx_a+total_dx_b+total_dy_a+total_dy_b)
lowpass = ndimage.gaussian_filter(data, 3)
gauss_highpass = data - lowpass



plt.show()

