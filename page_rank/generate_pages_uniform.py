import random

file = open("custom.txt", "w")

n = 10000

for node in range(n):
  edges = set([int(random.uniform(0, n)) for _ in range(int(random.uniform(1, max(5, n/800))))])
  while edges == {node}:
    edges = set([int(random.uniform(0, n)) for _ in range(int(random.uniform(1, max(5, n/800))))])
  file.write(f"{node}:{','.join(map(str, edges))}\n")

file.close()