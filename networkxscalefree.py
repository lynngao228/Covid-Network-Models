import random
from math import sqrt
import networkx as nx
import numpy as np
people=[]
locations={}
distances={}
numPpl = 20
maxX = 100
maxY = 100
import matplotlib.pyplot as plt

G = nx.barabasi_albert_graph(numPpl, 1) 
pos = nx.circular_layout(G) 

plt.figure(figsize = (5.5, 5.5)) 
nx.draw_networkx(G, pos)

# getting the people
# for each in range(1, numPpl+1):
#   people.append(each)
# #print(people)
# # assigning everybody a location
# for each in people:
#   locations[each]=[random.randint(1,maxX),random.randint(1,maxY)]
# #printing locations
# #for k,v in locations.items():
#   #print(k,v)
# # finding distances between the people
# for a in people:
#   for b in people:
#     if a < b:
#       distances[(a,b)]= sqrt(((locations[a][0]-locations[b][0])**2)+((locations[a][1]-locations[b][1])**2))

# scale free network
# this part adds the initial nodes (total of m0) and creates connections between them in the network
m0 = 3
numConnect = 0
# sConnection is a dictionary that shows {node: nodes it is connected to}
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

#Plot the locations of each point
# xvals=[]
# yvals=[]
# for each in locations:
#   xvals.append(locations[each][0])
#   yvals.append(locations[each][1])

# plt.plot(xvals,yvals,'ro')
# plt.show()



# # this part creates the matrix with the number of people, filled with zeros
# s = (numPpl,numPpl)
# array = np.zeros(s, dtype=int)

# # this part changes the matrix so that the the matrix has ones where there are connections
# for k, v in sConnection.items():
#   for i in v:
#     array[k-1][i-1] = 1
# print(array)

# # draws the visual representation of the spatial network model
# def create_graph():
#   G = nx.Graph()
#   G.add_nodes_from(people)
#   for i in range(len(array)):
#     for j in range(len(array[i])):
#       if array[i][j] == 1:
#         e = (i+1, j+1)
#         G.add_edge(*e)

#   pos = nx.circular_layout(G) 

#   plt.figure(figsize = (5.5, 5.5)) 
#   nx.draw_networkx(G, pos)
#   plt.show()

# create_graph()