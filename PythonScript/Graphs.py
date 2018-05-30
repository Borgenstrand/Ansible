#Example python code from https://pythonspot.com/matplolib-bar-chart/
import numpy as np
import matplotlib.pyplot as plt


#ASA case first:

#Data to plot
n_groups = 5 #This is how many bars that should be created
means_Manual = ('83.48','176.23','232.91','306.54','398.51') #Manual time data
means_Ansible = ('19.611','49.990','62.935','67.872','68.335') # Ansible time data
fig, ax=plt.subplots() 
index = np.arange(n_groups)
bar_width=0.35
opacity= 0.8

#First bar, manual bar.
rects1 = plt.bar(index,means_Manual, bar_width,
                 alpha=opacity,
                 color='b',
                 label='Manual')

#Second bar, Ansible bar
rects2 = plt.bar(index+bar_width, means_Ansible, bar_width,
                 alpha=opacity,
                 color='g',
                 label='Ansible')

#Below is some information about how the graph should be presented.
plt.xlabel("Amount of ASA's")
plt.ylabel("Time in seconds")
plt.title("ASA testing")
plt.xticks(index+bar_width,('1','2','3','4','5'))
plt.legend()

plt.tight_layout()
plt.savefig('ASA.png')
plt.show()



#VLAN case second:

#Data to plot
n_groups = 6 #This is how many bars that should be created
means_Manual = ('99.23','85.73','84.56','196.19','171.39','170.39') #Manual time data
means_Ansible = ('7.752','8.162','7.945','7.854','6.714','7.834') # Ansible time data
fig, ax=plt.subplots() 
index = np.arange(n_groups)
bar_width=0.35
opacity= 0.8

#First bar, manual bar.
rects1 = plt.bar(index,means_Manual, bar_width,
                 alpha=opacity,
                 color='b',
                 label='Manual')

#Second bar, Ansible bar
rects2 = plt.bar(index+bar_width, means_Ansible, bar_width,
                 alpha=opacity,
                 color='g',
                 label='Ansible')

#Below is some information about how the graph should be presented.
plt.xlabel("Amount of switches")
plt.ylabel("Time in seconds")
plt.title("VLAN testing")
plt.xticks(index+bar_width,('1','1','1','2','2','2'))
plt.legend()

plt.tight_layout()
plt.savefig('VLAN.png')
plt.show()


