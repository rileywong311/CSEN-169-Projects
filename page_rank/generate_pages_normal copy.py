import numpy as np
import random

file = open("custom.txt", "w")

n = 5
mean = 0
std_dev = 50

for node in range(n):
  edges = set([min(max(0, node + int(np.random.normal(loc=mean, scale=std_dev))), n) for _ in range(int(random.uniform(0, 20)))])
  print(edges)
  if edges:
    file.write(f"{node}:{','.join(map(str, edges))}\n")

file.close()