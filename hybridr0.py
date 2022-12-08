import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from scalefree import array, people, numPpl
from spatial import sarray, s
import copy
import matplotlib.pyplot as plt
from scipy import stats
import random

fig, (model, data_plot) = plt.subplots(1, 2)

#print('This is scale free array')
#print(array)
#print('This is spatial array')
#print(sarray)
# this copies the scale free model's array
harray = copy.deepcopy(array)
#print('copy of array')
#print(harray)
# this part adds the 1's from the spatial model array to the array created for the hybrid model
for i in range(len(sarray)):
  for j in range(len(sarray[i])):
    if sarray[i][j] == 1 and harray[i][j] == 0:
      harray[i][j] = 1
#print('Hybrid Array')
#print(harray)

sConnection = {}
for k in range(1, numPpl + 1):
  sConnection[k] = []
for i in range(len(harray)):
  for j in range(len(harray[0])):
    if harray[i][j] != 0:
      sConnection[i+1].append(j+1)

def create_graph():
  G = nx.Graph()
  G.add_nodes_from(people)
  for i in range(len(harray)):
    for j in range(len(harray[i])):
      if harray[i][j] == 1:
        e = (i+1, j+1)
        G.add_edge(*e)

  plt.figure(figsize = (5.5, 5.5)) 
  nx.draw_networkx(G, ax=model)

# counting the number of 1's in the matrix to check
count = 0
for i in sConnection.values():
  count += len(i)
print('Average connections per node:', count/numPpl)

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
  plt.show(block=False)
  slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
  metrics = ['slope','intercept','r value','p value','std err']
  summary = [slope, intercept, r_value, p_value, std_err]
  for i in range(5):
    print(metrics[i],':',summary[i])
  lsrl=[]
  for each in x:
    lsrl.append(slope*each+intercept)
  data_plot.plot(x,lsrl)

#print('creating graph')
create_graph()
#print('plotting')
r0plot(keys,values)