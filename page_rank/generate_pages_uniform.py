import random

file = open("custom.txt", "w")

n = 5

for node in range(n):
  edges = set([int(random.uniform(0, n)) for _ in range(int(random.uniform(0, 5)))])
  print(edges)
  if edges:
    file.write(f"{node}:{','.join(map(str, edges))}\n")

file.close()