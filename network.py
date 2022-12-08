import random
from math import sqrt
import networkx as nx
import numpy as np
people=[]
locations={}
distances={}
numPpl = 10
maxX = 100
maxY = 100
import matplotlib.pyplot as plt

# getting the people
for each in range(1, numPpl+1):
  people.append(each)
#print(people)
# assigning everybody a location
for each in people:
  locations[each]=[random.randint(1,maxX),random.randint(1,maxY)]
#printing locations
#for k,v in locations.items():
  #print(k,v)
# finding distances between the people
for a in people:
  for b in people:
    if a < b:
      distances[(a,b)]= sqrt(((locations[a][0]-locations[b][0])**2)+((locations[a][1]-locations[b][1])**2))

# for k,v in distances.items():
#   print(k,v)

# spatial network
# spatial={}

# r=3
# for each in people:
#   spatial[each]=[]
  
# for pair, dist in distances.items():
#   if dist <= 3.0:
#     spatial[pair[0]].append(pair[1])
#     spatial[pair[1]].append(pair[0])
# print('Spatial Model')
# for k,v in spatial.items():
#   print(k,v)


# scale free network
# probability of adding connection = # current connections of node / # total connections in model
m0 = 3
numConnect = 0
sConnection = {}
for h in range(1, m0+1):
  sConnection[h]=[]
for x in range(1, m0+1):
  for y in range(1, m0+1):
    if x < y:
      numConnect += 1
      sConnection[x].append(y)
      sConnection[y].append(x)

print('Scale-Free Model')
print(numConnect)
for k, v in sConnection.items():
  print(k, v)

prob = 0
for p in range(m0+1, numPpl + 1):
  sConnection[p]=[]
  for k, v in sConnection.items():
    if p != k:
      prob = len(v) / numConnect
      num = random.randint(1,100)
      if num <= prob * 100:
        sConnection[p].append(k)
        sConnection[k].append(p)
        numConnect += 1
print('Next part of scale free model')
for k, v in sConnection.items():
  print(k, v)

#Plot the locations of each point
# xvals=[]
# yvals=[]
# for each in locations:
#   xvals.append(locations[each][0])
#   yvals.append(locations[each][1])

# plt.plot(xvals,yvals,'ro')
# plt.show()

# this part creates the matrix with the number of people, filled with zeros
s = (numPpl,numPpl)
array = np.zeros(s, dtype=int)
# this part changes the matrix so that the the matrix has ones where there are connections
for k, v in sConnection.items():
  for i in v:
    array[k-1][i-1] = 1
print(array)
