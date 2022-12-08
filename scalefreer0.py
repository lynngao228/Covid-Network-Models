import random
from math import sqrt
import networkx as nx
import numpy as np
from scipy import stats
people=[]
locations={}
distances={}
numPpl = 50
maxX = 100
maxY = 100
import matplotlib.pyplot as plt
import copy


#plt.ion()
fig, (model, data_plot) = plt.subplots(1, 2)
#fig, (model, data_plot) = plt.subplots(1, 2)
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

# This section adds new nodes to the network and uses probability to determine if they will be connected to other nodes
# probability of adding connection = # current connections of node / # total connections in model
prob = 0
for p in range(m0+1, numPpl + 1):
  sConnection[p]=[]
  for k, v in sConnection.items():
    if p != k:
      prob = len(v) / numConnect
      num = random.random()
      if num <= prob:
        sConnection[p].append(k)
        sConnection[k].append(p)
        numConnect += 1

# this part creates the matrix with the number of people, filled with zeros
s = (numPpl,numPpl)
array = np.zeros(s, dtype=int)

# this part changes the matrix so that the the matrix has ones where there are connections
for k, v in sConnection.items():
  for i in v:
    array[k-1][i-1] = 1
# print('printing array')
# print(array)
# draws the visual representation of the scale-free network model
def create_graph():
  G = nx.Graph()
  G.add_nodes_from(people)
  for i in range(len(array)):
    for j in range(len(array[i])):
      if array[i][j] == 1:
        e = (i+1, j+1)
        G.add_edge(*e)

  #pos = nx.draw(G) 

  plt.plot(figsize = (5.5, 5.5))
  nx.draw_networkx(G, ax = model) 

  plt.show(block = False)

# counting the number of 1's in the matrix to check
count = 0
for i in sConnection.values():
  count += len(i)
print('Average connections per node:', count/numPpl)

create_graph()

trials = 100
trial_data = {}
to_test = []
for i in range(1, numPpl +1):
  trial_data[i] = []
  to_test.append(i)
iterations = 0

#create_graph()
def infection(iterations):
  while True:
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
    if len(to_test) == 0:
      break
    for i in range(0,n):
      index = random.randint(0, len(to_test) - 1)
      rand_inf = to_test[index]
      while rand_inf in inf:
        index = random.randint(0, len(to_test) - 1)
        rand_inf = to_test[index]
      inf.append(rand_inf)
      sus.remove(rand_inf)
    transmissions = 0
    newinf = []
    inf_values = [n]
    #removed nodes
    rem = []
    rem_values = [0]
    #rate of infection upon contact with infected person
    infected_rate = 0.2
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
        #print('beginning of inner while loop')
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
        #print('reached num_checked += 1')
        # we will see if the chosen node is removed
        removed = 1
        if current_time != 1:
          removed = random.random()
          #print(f'probability number = {removed}')
          if removed <= removal_rate:
            current_removed += 1
            current_infected -= 1
            inf.remove(chosen)
            rem.append(chosen)
            #print(len(inf))
        # loop through the connections of the chosen infected node and use determine whether they are infected or not
        if removed > removal_rate:
          #print('node was not removed, not infecting...')
          for i in sConnection[chosen]:
            if i in sus:
              infected = random.random()
              if infected <= infected_rate:
                # it is now infected
                sus.remove(i)
                newinf.append(i)
                current_susceptible -= 1
                current_infected += 1
                if chosen == rand_inf:
                  transmissions += 1
                  
      sus_values.append(current_susceptible)
      inf_values.append(current_infected)
      rem_values.append(current_removed)
      inf.extend(newinf)
      newinf = []
      #print(len(inf))
      #print(f"At the end of time {current_time}, the nodes that are susceptible are \n {sus} \n with length {current_susceptible}, the nodes that are infected are \n {inf} \n with length {current_infected}, and the nodes that are removed are \n {rem} \n with length {current_removed}")
      val_checked = []
      num_checked = 0
    trial_data[rand_inf].append(transmissions)
    if len(trial_data[rand_inf])>=trials:
      to_test.remove(rand_inf)
    iterations += 1
  return iterations, sus_values, inf_values, rem_values, time

itera, sus_values, inf_values, rem_values, time = infection(iterations)
print('number of iterations:',itera)
keys = []
values = []
for key, value in trial_data.items():
  keys.append(len(sConnection[key]))
  values.append(sum(value)/len(value))
  #print(f'{key}: {sum(value)/len(value)}')
print('average r0 value for all nodes:',sum(values)/len(values))

def r0plot(x,y):
  data_plot.scatter(x,y)
  data_plot.set_xlabel('Number of connections')
  data_plot.set_ylabel('Average number of people infected')
  fig.tight_layout()
  slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
  metrics = ['slope','intercept','r value','p value','std err']
  summary = [slope, intercept, r_value, p_value, std_err]
  for i in range(5):
    print(metrics[i],':',summary[i])
  lsrl=[]
  for each in x:
    lsrl.append(slope*each+intercept)
  data_plot.plot(x,lsrl)
  plt.show(block=False)
  plt.show(block=False)

r0plot(keys,values)