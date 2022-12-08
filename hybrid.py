import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from scalefree import array, people, numPpl
from spatial import sarray, s
import copy
import matplotlib.pyplot as plt
import random

#fig, (model, data_plot) = plt.subplots(1, 2)

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

# draws the visual representation of the spatial network model
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

  plt.show()

sConnection = {}
for k in range(1, numPpl + 1):
  sConnection[k] = []
for i in range(len(harray)):
  for j in range(len(harray[0])):
    if harray[i][j] != 0:
      sConnection[i+1].append(j+1)

def infection():
  # list of time for plotting
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
  # rate of removal
  removal_rate = 0.4
  current_time = 0
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
    val_checked = []
  return sus_values, inf_values, rem_values, time
          
    
#Plot values, label plot, show plot    
#create_graph()


#def subplot(sus_values, inf_values, rem_values, time):
def subplot():
  #plt.ion()
  fig, (model, data_plot) = plt.subplots(1, 2)
  G = nx.Graph()
  G.add_nodes_from(people)
  for i in range(len(harray)):
    for j in range(len(harray[i])):
      if harray[i][j] == 1:
        e = (i+1, j+1)
        G.add_edge(*e)

  plt.figure(figsize = (5.5, 5.5)) 
  nx.draw_networkx(G, ax=model)
  model.set_title('Hybrid Model')

  data_plot.plot(time,sus_values, label='Susceptible')
  data_plot.plot(time,inf_values,label='Infected')
  data_plot.plot(time,rem_values,label='Recovered')

  data_plot.set_xlabel('Time passed')
  data_plot.set_ylabel('Number of people')
  data_plot.set_title('Infection Spread')
  data_plot.legend()
  fig.tight_layout()
  plt.show(block = False)
sus_values, inf_values, rem_values, time = infection()
subplot()