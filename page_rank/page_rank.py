from collections import defaultdict
import numpy as np
import sys


ifile = sys.argv[1]
d = float(sys.argv[2])

incoming_pages = defaultdict(set) # target page : links into it from other pages
outgoing_count = {} # target page : count of outgoing links from the page
seen = set()

file = open(ifile)
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

# print("Incoming Pages -", dict(incoming_pages))
# print("Outgoing Counts -", outgoing_count)



n = count + 1
M = np.zeros((n, n))

for row in range(n):
  for col in range(n):
    if col in incoming_pages[row]:
      M[row][col] = 1/outgoing_count[col]

# print(M)



v_0 = v_prev = np.full((n, 1), 1/n)
v_curr = d * np.matmul(M, v_prev) + (1 - d) * v_0
# v_curr = np.matmul(M, v_prev)

epsilon = 0.00001
while(np.linalg.norm(v_curr - v_prev) > epsilon):
  v_prev = v_curr
  v_curr = d * np.matmul(M, v_prev) + (1 - d) * v_0
  # v_curr = np.matmul(M, v_prev)

# print(v_curr)
# print("Total -", sum(v_curr))

for val in v_curr:
  print("{:.10f}".format(val[0]))