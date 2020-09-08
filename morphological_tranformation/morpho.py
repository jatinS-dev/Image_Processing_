import numpy as np
import matplotlib.pyplot as plt

def add_Padding(array):
  new_array = np.ones((array.shape[0]+4,array.shape[1]+4,array.shape[2]),dtype = array.dtype)
  for c in range(array.shape[2]):
    for i in range(array.shape[0]):
      for j in range(array.shape[1]):
        new_array[i+2,j+2,c] = array[i,j,c]
  return new_array
#print('array',array)

def dilation(matrix,option):
  kernel = np.zeros((5,5,1),dtype = matrix.dtype)
  filtered = np.zeros((matrix.shape[0],matrix.shape[1],matrix.shape[2]),dtype = matrix.dtype)
  padded = add_Padding(matrix)
  for c in range(4):
    for i in range(matrix.shape[0]):
      for j in range(matrix.shape[1]):
        for x in range(5):
          for y in range(5):
            kernel[y,x] = padded[i+y,j+x,c]
        if 1 in kernel and option == 2:
          filtered[i,j,c] = 1
        elif np.all(kernel) and option == 1:
          filtered[i,j,c] = 1
        else:
          filtered[i,j,c] = 0
  return filtered
#print('matrix',matrix)              
image = plt.imread('morphological.png')
option = int(input('Enter 1 for erosion and 2 for dilation\n1)Erosion\n2)Dilation'))
filtered1 = dilation(image,1)
filtered2 = dilation(image,2)
if option==1:
   plt.imshow(filtered1)
   plt.title("Erosion")
   plt.show()
if option==2:
   plt.imshow(filtered2)
   plt.title("Dilation")
   plt.show()
