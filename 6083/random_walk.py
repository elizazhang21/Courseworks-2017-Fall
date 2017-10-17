import matplotlib
from  matplotlib import pyplot as plt
import random


position = 0
walk = [position]
steps = 10000
for i in range(steps):
	step = random.choice([-1,-1,1,1,1])
	position += step
	walk.append(position)

print(walk)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(walk)
plt.show()

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(walk)
plt.show()


