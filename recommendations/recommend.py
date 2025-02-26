from parse import get_data_dict
from collections import defaultdict
import numpy as np
import heapq


def cosine_similarity(v1, v2):
  return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))


K = 30
def v1(train_filename, test_filename, out_filename):

  data = get_data_dict(train_filename)

  test = defaultdict(dict)
  results = []
  ifile = open(test_filename)
  for line in ifile:
    U, M, R = map(int, line.split())

    if R:
      test[U][M] = R
      continue
    
    min_heap = []
    for user in data:
      if M not in data[user]:
        continue
      intersect = set(test[U].keys()) & set(data[user].keys())
      # print(U, "&", user, "=", intersect)
      if intersect:
        v1 = np.array([test[U][movie] for movie in intersect])
        v2 = np.array([data[user][movie] for movie in intersect])
        sim = cosine_similarity(v1, v2)
        if len(min_heap) < K:
          heapq.heappush(min_heap, (sim, user))
        else:
          heapq.heappushpop(min_heap, (sim, user))
        # print(v1, "vs.", v2, "=", sim)
    
    if not min_heap:
      print(f"{test_filename} : No user similar to {U} found with movie rating on {M}")
      results.append((U, M, 3))
    else:
      weighted_average = sum([neighbor[0] * data[neighbor[1]][M] for neighbor in min_heap]) / sum([neighbor[0] for neighbor in min_heap])
      # print([f"{neighbor[0]} * {data[neighbor[1]][M]}" for neighbor in min_heap], "=", weighted_average)
      results.append((U, M, round(weighted_average)))

  ifile.close()

  ofile = open(out_filename, "w")
  for result in results:
    ofile.write(f"{result[0]} {result[1]} {result[2]}\n")
  ofile.close()

  return results
