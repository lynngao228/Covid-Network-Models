import random
import networkx as nx
import numpy as np
import scipy.optimize
import scipy.stats
people=[]
locations={}
distances={}
numClasses = 20
maxX = 100
maxY = 100
import matplotlib.pyplot as plt
import copy

#fig, axs = plt.subplots(2, 2)

#small-world network
large = 100
medium = 50
class_sizes = {}
#list of all classes
sizes = []

# with open('Enrollment.txt') as file_in:
#   for line in file_in:
#     info = line.strip()
#     if info[0] != '>' and info != '0':
#       sizes.append(int(line)+1)

# class times has all class times (repeats allowed)
# times only has general class times

with open('MathDeptClasses Spring 2020.csv') as file_in:
  for line in file_in:
    info = line.strip().split(',')
    #print(info)
    if info[1] == 'Lec' and info[5][0:3] == 'MWF':
      if info[5] not in class_sizes:
        class_sizes[info[5]]=[]
      class_sizes[info[5]].append(int(info[9])+2)

# x=0
# for k,v in class_sizes.items():
#   for each in v:
#     print(k,each)
#     x += 1
# print(x)

for each in class_sizes:
  sizes.extend(class_sizes[each])
print(sizes)
times = []
for each in class_sizes:
  times.append(each)

print('Number of unique class starting times:',len(class_sizes))

time_dist = {}

print('Distribution of Class Times:')
for each in class_sizes:
  time_dist[each]=len(class_sizes[each])

for k,v in time_dist.items():
  print(k,v)


classification = {'morning':{},'afternoon':{},'evening':{}}
for each in class_sizes:
  if 'p' in each:
    if int(each[6]) < 4:
      if each not in classification['afternoon']:
        classification['afternoon'][each]=[]
      classification['afternoon'][each].extend(class_sizes[each])
    else:
      if each not in classification['evening']:
        classification['evening'][each]=[]
      classification['evening'][each].extend(class_sizes[each])
  else:
    if each not in classification['morning']:
      classification['morning'][each]=[]
    classification['morning'][each].extend(class_sizes[each])


#classPop = []
print('Classification of Classes')

for k,v in classification.items():
  print(k)
  for each in v:
    print(each,v[each])
    #classPop.extend(v[each])

morning = []
afternoon = []
evening = []
for time, a in classification.items():
  for b in a.values():
    if time == 'morning':
      morning.extend(b)
    elif time == 'afternoon':
      afternoon.extend(b)
    else:
      evening.extend(b)

sums = [morning,afternoon,evening]
sums_names = ['Total enrolled in morning:','Total enrolled in afternoon:','Total enrolled in evening:']
sums_time = []
enrolled = 0
for i in range(len(sums)):
  sums_time.append(sum(sums[i]))
  enrolled += sum(sums[i])
  print(sums_names[i],sum(sums[i]))

totalPpl = int(enrolled/3)

for i in range(len(sums)):
  for j in range(len(sums[i])):
    sums[i][j] = float(sums[i][j] * totalPpl/sums_time[i])
  print('New total',round(sum(sums[i])))
  
for a in sums:
    for i in range(len(a)):
        a[i] = round(a[i])
        
for each in sums:
    difference = sum(each) - totalPpl
    if difference > 0:
        for i in range(difference):
            replace = random.randint(0,len(each)-1)
            each[replace] -= 1
    elif difference < 0:
        for i in range(abs(difference)):
            replace = random.randint(0,len(each)-1)
            each[replace] += 1

class_size_data = []
for each in sums:
  class_size_data.extend(each)

#print(class_size_data)

large_data = []
medium_data = []
small_data = []

large = 150
medium = 100

for each in class_size_data:
  if each >= large:
    large_data.append(each)
  elif medium <= each < large:
    medium_data.append(each) 
  else:
    small_data.append(each)


# axs[0,0].hist(class_size_data)
# axs[0,0].set_title("Distributions of all Class Sizes")
# axs[0,0].set_xlabel("Class Size")
# axs[0,0].set_ylabel("Frequency")

# axs[1,0].hist(large_data)
# axs[1,0].set_title("Distributions of Large Class Sizes")
# axs[1,0].set_xlabel("Class Size")
# axs[1,0].set_ylabel("Frequency")

# axs[0,1].hist(medium_data)
# axs[0,1].set_title("Distributions of Medium Class Sizes")
# axs[0,1].set_xlabel("Class Size")
# axs[0,1].set_ylabel("Frequency")

# axs[1,1].hist(small_data)
# axs[1,1].set_title("Distributions of Small Class Sizes")
# axs[1,1].set_xlabel("Class Size")
# axs[1,1].set_ylabel("Frequency")

# plt.tight_layout()
# plt.show(block=False)

print(len(large_data), len(medium_data), len(small_data))
print()

# [small, medium, large]
morning_prop = [0, 0, 0]
afternoon_prop = [0, 0, 0]
evening_prop = [0, 0, 0]

for i in morning:
  if i >= large:
    morning_prop[2] += 1
  elif medium <= i < large:
    morning_prop[1] += 1
  else:
    morning_prop[0] += 1
for i in afternoon:
  if i >= large:
    afternoon_prop[2] += 1
  elif medium <= i < large:
    afternoon_prop[1] += 1
  else:
    afternoon_prop[0] += 1
for i in evening:
  if i >= large:
    evening_prop[2] += 1
  elif medium <= i < large:
    evening_prop[1] += 1
  else:
    evening_prop[0] += 1

print("ratio for morning:", morning_prop)
print("ratio for afternoon:", afternoon_prop)
print("ratio for evening:", evening_prop)

nodes = list(range(1, totalPpl+1))
nodes1 = copy.deepcopy(nodes)

random.shuffle(nodes)
nodes2 = copy.deepcopy(nodes)

random.shuffle(nodes)
nodes3 = copy.deepcopy(nodes)

numClasses = len(sizes)
print('Total classes',numClasses)
print('Total people',totalPpl)
print('Average class size',round(totalPpl/numClasses*3))
s_morn = (len(morning), len(morning))

interactions = 8
#in_group = 1
out_group=0
probs_morn = np.zeros(s_morn, dtype = float)
#probs = np.zeros(s, dtype = float)
for a in range(len(morning)):
  for b in range(len(morning)):
    if a != b:
      probs_morn[a,b]=out_group
    else:
      if morning[a] <= 8:
        probs_morn[a,b] = 1
      else:
        probs_morn[a,b]=interactions/morning[a]
#print(len(probs))

G_morn = nx.stochastic_block_model(morning, probs_morn, nodes1) 
pos_morn = nx.circular_layout(G_morn) 

s_after = (len(afternoon), len(afternoon))
probs_after = np.zeros(s_after, dtype = float)
for a in range(len(afternoon)):
  for b in range(len(afternoon)):
    if a != b:
      probs_after[a,b]=out_group
    else:
      if afternoon[a] <= 8:
        probs_after[a,b]=1
      else:
        probs_after[a,b]=interactions/afternoon[a]
#print(len(probs))

G_after = nx.stochastic_block_model(afternoon, probs_after, nodes2) 
pos_after = nx.circular_layout(G_after)

s_evening = (len(evening), len(evening))
probs_evening = np.zeros(s_evening, dtype = float)
#probs = np.zeros(s, dtype = float)
for a in range(len(evening)):
  for b in range(len(evening)):
    if a != b:
      probs_evening[a,b]=out_group
    else:
      if evening[a] <= 8:
        probs_after[a, b] = 1
      else:
        probs_evening[a,b]=interactions/evening[a]
#print(len(probs))

G_evening = nx.stochastic_block_model(evening, probs_evening, nodes1) 
pos_evening = nx.circular_layout(G_evening) 


# MORNING ARRAY
array_morn = np.zeros(s_morn, dtype=int)
# this part changes the matrix so that the the matrix has ones where there are connections
array_morn = nx.to_numpy_array(G_morn, dtype = int)
#print(array)
sConnection_morn = {}
sConnection_after = {}
sConnection_evening = {}
for k in range(1, totalPpl + 1):
  sConnection_morn[k] = []
  sConnection_after[k] = []
  sConnection_evening[k] = []
for i in range(len(array_morn)):
  for j in range(len(array_morn[0])):
    if array_morn[i][j] != 0:
      sConnection_morn[i+1].append(j+1)
#print(len(sConnection_morn))


# plt.figure(figsize = (5.5, 5.5)) 
# nx.draw_networkx(G_evening)
# plt.title('Stochastic Block Model - Evening')

# plt.show(block = False)
# print('Plotting Finished')


# AFTERNOON ARRAY

array_after = np.zeros(s_after, dtype=int)
# this part changes the matrix so that the the matrix has ones where there are connections
array_after = nx.to_numpy_array(G_after, dtype = int)
#print(array)
sConnection_after = {}
for k in range(1, totalPpl + 1):
  sConnection_after[k] = []
for i in range(len(array_after)):
  for j in range(len(array_after[0])):
    if array_after[i][j] != 0:
      sConnection_after[i+1].append(j+1)
#print(len(sConnection_after))

# EVENING ARRAY
array_evening = np.zeros(s_evening, dtype=int)
# this part changes the matrix so that the the matrix has ones where there are connections
array_evening = nx.to_numpy_array(G_evening, dtype = int)
#print(array)
sConnection_evening = {}
for k in range(1, totalPpl + 1):
  sConnection_evening[k] = []
for i in range(len(array_evening)):
  for j in range(len(array_evening[0])):
    if array_evening[i][j] != 0:
      sConnection_evening[i+1].append(j+1)
#print(sConnection_evening)

trials = 100
trial_data = {}
to_test = []
for i in range(1, totalPpl +1):
  trial_data[i] = []
  to_test.append(i)

# loop through days, then have inner loop for time periods
def infection():
  iterations = 0
  while True:
    time=[1] #count in time sections
    days = 0

    #susceptible 
    sus = list(range(1, totalPpl+1))
    #store susceptible at each time
    sus_values = []
    sus_values.append(len(sus))
    # want n people who is infected
    inf = []
    n = 1
    if len(to_test) == 0:
      break
    for i in range(0,n):
      rand_inf = random.randint(1, totalPpl)
      while rand_inf in inf:
        rand_inf = random.randint(1, totalPpl)
      inf.append(rand_inf)
      sus.remove(rand_inf)
    transmissions = 0
    newinf = []
    inf_values = [n]
    #removed nodes
    rem = []
    rem_values = [0]
    #rate of infection upon contact with infected person
    infected_rate = ((1/6)*2.5)/3
    removal_rate = 1/6
    current_week = 1
    current_day = 1
    current_time = 1
    num_checked = 0
    val_checked = []
    while rand_inf in inf:
      current_time = 1
      while current_time < 4:
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
          if current_day != 1:
            removed = random.random()
            if removed <= removal_rate:
              current_removed += 1
              current_infected -= 1
              inf.remove(chosen)
              rem.append(chosen)
              #print(len(inf))
          # loop through the connections of the chosen infected node and use determine whether they are infected or not
          if removed > removal_rate:
            if current_time == 1:
              for i in sConnection_morn[chosen]:
                if i in sus:
                  infected = random.random()
                  #print(infected)
                  if infected <= infected_rate:
                    # it is now infected
                    sus.remove(i)
                    newinf.append(i)
                    current_susceptible -= 1
                    current_infected += 1
                    if chosen == rand_inf:
                      transmissions += 1
            elif current_time == 2:
              for i in sConnection_after[chosen]:
                if i in sus:
                  infected = random.random()
                  #print(infected)
                  if infected <= infected_rate:
                    # it is now infected
                    sus.remove(i)
                    newinf.append(i)
                    current_susceptible -= 1
                    current_infected += 1
                    if chosen == rand_inf:
                      transmissions += 1
            elif current_time == 3:
              for i in sConnection_evening[chosen]:
                if i in sus:
                  infected = random.random()
                  #print(infected)
                  if infected <= infected_rate:
                    # it is now infected
                    sus.remove(i)
                    newinf.append(i)
                    current_susceptible -= 1
                    current_infected += 1
                    if chosen == rand_inf:
                      transmissions += 1
        sus_values.append(current_susceptible)
        inf.extend(newinf)
        inf_values.append(current_infected)
        rem_values.append(current_removed)
        newinf = []
        #print(f"At the end of time {current_time}, the nodes that are susceptible are length {current_susceptible}, the nodes that are infected are length {current_infected}, and the nodes that are removed are length {current_removed}")
        val_checked = []
        num_checked = 0
        current_time += 1
        time.append(time[-1] + 1)
      current_day += 1
    trial_data[rand_inf].append(transmissions)
    if len(trial_data[rand_inf])>=trials:
      to_test.remove(rand_inf)
    iterations += 1
  return iterations

itera = infection() 
print('number of iterations:',itera)
keys = []
values = []
for key, value in trial_data.items():
  keys.append(len(sConnection[key]))
  values.append(sum(value)/len(value))
  #print(f'{key}: {sum(value)/len(value)}')
print('average r0 value for all nodes:',sum(values)/len(values))         

#Plot values, label plot, show plot    

def r0plot(x,y):
  plt.scatter(x,y)
  plt.xlabel('cumber of connections')
  plt.ylabel('Average number of people infected')
  slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(x,y)
  metrics = ['slope','intercept','r value','p value','std err']
  summary = [slope, intercept, r_value, p_value, std_err]
  for i in range(5):
    print(metrics[i],':',summary[i])
  lsrl=[]
  for each in x:
    lsrl.append(slope*each+intercept)
  plt.plot(x,lsrl)
  plt.show(block=False)

print('creating graph')
#create_graph()
#print('plotting')
r0plot(keys,values)