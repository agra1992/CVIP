## histogram equalization


import matplotlib.pyplot as plt
import numpy as np
from scipy import ndimage
from PIL import Image

def plot(data, title):
    plot.i += 1
    plt.subplot(3,2,plot.i)
    plt.plot(data)
    plt.gray()
    plt.title(title)
plot.i = 0

im = Image.open('scene.jpg').convert('L')
data = np.array(im, dtype=int)


plot.i += 1
plt.subplot(3,2,plot.i)
plt.imshow(data)

hist=np.zeros(256);
print data


for y in range(len(data)):
    for x in range(len(data[y])):
        hist[data[y][x]]=hist[data[y][x]]+1
            
#plt.subplot(2,2,1)
plot(hist,'Histogram')


cumulative=np.zeros((256))
cumulative[0]=hist[0]
for i in range(1,256):
    cumulative[i]=cumulative[i-1]+hist[i]
#plt.subplot(2,1,cumulative)
#plt.subplot(2,2,2)
plot(cumulative,'cummulative')



norm=np.zeros((256))
for i in range(256):
    norm[i]= round((255.0/(len(data)*len(data[i])))*cumulative[i])
    
#plt.subplot(3,1,norm)    


plot(norm,'norm_round')


newdata=np.zeros((len(data),len(data[0])))
for y in range(len(data)):
    for x in range(len(data[y])):
        newdata[y][x]=norm[data[y][x]]

plot.i += 1
plt.subplot(3,2,plot.i)
plt.imshow(newdata)

histnew=np.zeros(256);
for y in range(len(newdata)):
    for x in range(len(newdata[y])):
        histnew[newdata[y][x]]=histnew[newdata[y][x]]+1

plot(histnew,'histo_new')
plt.show()
