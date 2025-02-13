edge_list = {}

file = open("page_rank/input1.txt")
count = -1
for line in file:
  node, edges = line.split(":")
  node = int(node)
  edges = set(map(int, edges.replace("\n", "").split(",")))
  edge_list[node] = edges
  count = max(node, max(edges))
file.close()

if count == -1:
  print("No nodes")
  exit()

print(count)
print(edge_list)