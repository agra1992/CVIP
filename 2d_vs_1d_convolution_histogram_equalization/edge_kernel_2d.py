## Convolution with edge kernel
## with 2d filter

import matplotlib.pyplot as plt
import numpy as np
from scipy import ndimage
from PIL import Image
import time

def plot(data, title):
    plot.i += 1
    plt.subplot(3,3,plot.i)
    plt.imshow(data)
    plt.gray()
    plt.title(title)
plot.i = 0

def function_convolve(full,kernel):
    
    convolved=np.empty([len(full),len(full[0])])
    

    kernel=np.flipud(np.fliplr(kernel))
    dy=len(kernel)
    dx=len(kernel[0])

    stop_cumm=0
    time_diff=0.0
    time_diff_temp=0.0
    for y in range(len(full)):
        for x in range(len(full[0])):    
            

            if(x>2 and x<len(full[0])-2 and y>2 and y<len(full)-2) :                
                if (dy>1 and dx>1):
                #print y-(dy/2), " ",y+((dy/2)+1)," ",x-(dx/2)," ",x+((dx/2)+1)
                    first=full[y-(dy/2):y+((dy/2)+1),x-(dx/2):x+((dx/2)+1)]

                elif(dx>1):
                    first=full[y,x-(dx/2):x+((dx/2)+1)]
                elif(dy>1):
                    first=full[y-(dy/2):y+((dy/2)+1),x]
                else:
                    first=full[y,x]
                    
                second=kernel
                ##together=np.empty([len(first),len(first[0])])
                start_time = time.time()
                mul_sum=0
                for p in range(len(first)):
                    for q in range(len(first[0])):
                        corresponding_mul=first[p][q]*second[p][q]
                        mul_sum=mul_sum+corresponding_mul

                t=mul_sum
                time_diff_temp=time.time()-start_time
                convolved[y][x]=t
            time_diff=time_diff+time_diff_temp   
    
    return convolved,time_diff



im = Image.open('lena_gray.png')
data = np.array(im, dtype=float)
#data=data[1:200]

plot(data, 'Original')



kernel = np.array([[-1, 0, 1],
                   [-2,  0, 2],
                   [-1, 0, 1]])

                                     
                   



self_dx,timetotal1=function_convolve(data,kernel)                   
plot(self_dx, 'SELF CONVOLVED GX '+str(timetotal1))

inbuilt_dx = ndimage.convolve(data, kernel)

plot(inbuilt_dx, 'Inbuilt convolve GX')


kernel = np.array([[-1, -2, -1],
                   [0,  0, 0],
                   [1, 2, 1]])

self_dy,timetotal2=function_convolve(data,kernel)                   
plot(self_dy, 'SELF CONVOLVED GY '+str(timetotal2))

inbuilt_dy = ndimage.convolve(data, kernel)
plot(inbuilt_dy, 'Inbuilt convolve GY')

new=np.sqrt(np.square(inbuilt_dx)+np.square(inbuilt_dy))
new_c=np.sqrt(np.square(self_dx)+np.square(self_dy))


print 'total time of mul Gx '+str(timetotal1)
print 'total time of mul Gx '+str(timetotal2)
print 'total time of mul G'+str(timetotal1+timetotal2)
plot(new, 'CONVOLVE G INBUILT')
plot(new_c, 'CONVOLVE G FINAL '+str(timetotal1+timetotal2))
plt.show()