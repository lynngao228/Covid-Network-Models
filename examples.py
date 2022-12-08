# sphinx_gallery_thumbnail_number = 11

import matplotlib.pyplot as plt
import numpy as np

# Some example data to display
x = np.linspace(0, 2 * np.pi, 400)
y = np.sin(x ** 2)

fig, (ax1, ax2) = plt.subplots(1, 2)
fig.suptitle('Horizontally stacked subplots')
ax1.plot(x, y)
ax2.plot(x, -y)

plt.show(block=False)

# import networkx as nx 
# import matplotlib.pyplot as plt 
# import numpy as np
  
# x = [1,2,3]
# y=[2,4,6]

# fig, axs = plt.subplots(2, 2)
# axs[0, 0].plot(x, y)
# axs[0, 0].set_title('Axis [0,0]')
# axs[0, 1].plot(x, y, 'tab:orange')
# axs[0, 1].set_title('Axis [0,1]')
# axs[1, 0].plot(x, -y, 'tab:green')
# axs[1, 0].set_title('Axis [1,0]')
# axs[1, 1].plot(x, -y, 'tab:red')
# axs[1, 1].set_title('Axis [1,1]')

# for ax in axs.flat:
#     ax.set(xlabel='x-label', ylabel='y-label')

# # Hide x labels and tick labels for top plots and y ticks for right plots.
# for ax in axs.flat:
#     ax.label_outer()

# # G = nx.watts_strogatz_graph(10, 1) 
# # pos = nx.circular_layout(G) 

# # plt.figure(figsize = (5.5, 5.5)) 
# # nx.draw_networkx(G, pos)
# # #nx.draw(G, with_labels=True, font_weight='bold')

# # plt.show()

# # nx.to_numpy_array(G)

# # print(array)
# # A = [[1, 4, 5, 12], [-5, 8, 9, 0], [-6, 7, 11, 19]]
# # A[1] = [-5, 8, 9, 0]
# # A[1][2] = 9
# # A[0][-1] = 12

# # print(A)

# # s = (10,10)
# # array = np.zeros(s, dtype=int)
# # print(array)