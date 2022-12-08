import random
from math import sqrt
import networkx as nx
import numpy as np
people=[]
locations={}
distances={}
numPpl = 50
maxX = 100
maxY = 100
import matplotlib.pyplot as plt
import copy

plt.ion()

fig, (model, data_plot) = plt.subplots(1, 2)

#small-world network

G = nx.watts_strogatz_graph(numPpl, 4, 0.1) 
pos = nx.circular_layout(G) 

s = (numPpl,numPpl)
array = np.zeros(s, dtype=int)
# this part changes the matrix so that the the matrix has ones where there are connections
array = nx.to_numpy_array(G, dtype = int)
strArray = str(array)
count = strArray.count('1')

null = nx.watts_strogatz_graph(numPpl, 4, 0)
array0 = np.zeros(s, dtype=int)
array0 = nx.convert_matrix.to_numpy_matrix(null)
#print(array0)

sConnection = {}
for k in range(1, numPpl + 1):
  sConnection[k] = []
for i in range(len(array)):
  for j in range(len(array[0])):
    if array[i][j] != 0:
      sConnection[i+1].append(j+1)
print(sConnection)

rewires = 0
for a in range(numPpl):
  for b in range(numPpl):
    if array[a,b]!=array0[a,b]:
      rewires += 1

rewires = rewires/4
print('Total rewires:',rewires)

plt.ion()
plt.figure(figsize = (5.5, 5.5)) 
#posdraw_networkxla, asx=modelypo
nx.draw_networkx(pos)
model.set_title('Small-World Model')
#nx.draw_networkx(null)

plt.show(block = False)
print('Plotting Finished')

time=[0]
#susceptible 
sus = []
#store susceptible at each time
sus_values = []
for i in range(1, numPpl + 1):
  sus.append(i)
sus_values.append(len(sus))
# want n people who is infected
inf = []
n = 1
for i in range(0,n):
  rand_inf = random.randint(1, numPpl)
  while rand_inf in inf:
    rand_inf = random.randint(1, numPpl)
  inf.append(rand_inf)
  sus.remove(rand_inf)
newinf = []
inf_values = [n]
#removed nodes
rem = []
rem_values = [0]
#rate of infection upon contact with infected person
infected_rate = 0.5
removal_rate = 0.4
current_time = 0
num_checked = 0
val_checked = []
while len(inf) > 0:
  current_time += 1
  time.append(current_time)
  not_checked = copy.deepcopy(inf)
  current_infected = inf_values[-1]
  current_removed = rem_values[-1]
  current_susceptible = sus_values[-1]
  while len(not_checked) != 0:
    # randomly get node from infected list
    if len(not_checked) == 1:
      chosen = not_checked[0]
    else:
      chosen = not_checked[random.randint(0, len(not_checked)-1)]
      while chosen in val_checked:
        chosen = not_checked[random.randint(0, len(not_checked)-1)]
    val_checked.append(chosen)
    not_checked.remove(chosen)
    num_checked += 1
    # we will see if the chosen node is removed
    removed = 1
    if current_time != 1:
      removed = random.random()
      if removed <= removal_rate:
        current_removed += 1
        current_infected -= 1
        inf.remove(chosen)
        rem.append(chosen)
        print(len(inf))
    # loop through the connections of the chosen infected node and use determine whether they are infected or not
    if removed > removal_rate:
      for i in sConnection[chosen]:
        if i in sus:
          infected = random.random()
          if infected <= infected_rate:
            # it is now infected
            sus.remove(i)
            newinf.append(i)
            current_susceptible -= 1
            current_infected += 1
  sus_values.append(current_susceptible)
  inf_values.append(current_infected)
  rem_values.append(current_removed)
  inf.extend(newinf)
  newinf = []
  print(f"At the end of time {current_time}, the nodes that are susceptible are \n {sus} \n with length {current_susceptible}, the nodes that are infected are \n {inf} \n with length {current_infected}, and the nodes that are removed are \n {rem} \n with length {current_removed}")
  val_checked = []
  num_checked = 0
          
#Plot values, label plot, show plot    
#create_graph()

def subplot():
  data_plot.plot(time,sus_values, label='Susceptible')
  data_plot.plot(time,inf_values, label='Infected')
  data_plot.plot(time,rem_values, label='Recovered')

  data_plot.set_xlabel('Time passed')
  data_plot.set_ylabel('Number of people')
  data_plot.set_title('SIR Small-World Network Model')
  data_plot.legend()
  fig.tight_layout()
  plt.show(block = False)

subplot()