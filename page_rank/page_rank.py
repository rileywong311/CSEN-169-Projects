from collections import defaultdict
import numpy as np

incoming_pages = defaultdict(set)
outgoing_count = {}
seen = set()

file = open("input2.txt")
count = -1
for line in file:
  node, edges = line.split(":")
  node = int(node)
  edges = set(map(int, edges.replace("\n", "").split(",")))
  outgoing_count[node] = len(edges)
  for edge in edges:
    incoming_pages[edge].add(node)
  count = max(node, max(edges))
file.close()

print("Incoming Pages", dict(incoming_pages))
print("Outgoing Counts", outgoing_count)


M = np.zeros((count + 1, count + 1))

for row in range(count + 1):
  for col in range(count + 1):
    if col in incoming_pages[row]:
      M[row][col] = 1/outgoing_count[col]

print(M)


