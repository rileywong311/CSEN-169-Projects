from parse import get_data_dict
from collections import defaultdict
import numpy as np


def cosine_similarity(v1, v2):
  return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))


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
    
    closest = {"user": 0, "sim": 0}
    for user in data:
      if M not in data[user]:
        continue
      intersect = set(test[U].keys()) & set(data[user].keys())
      # print(U, "&", user, "=", intersect)
      if intersect:
        v1 = np.array([test[U][movie] for movie in intersect])
        v2 = np.array([data[user][movie] for movie in intersect])
        sim = cosine_similarity(v1, v2)
        closest = max((closest, {"user": user, "sim": sim}), key=lambda x: x["sim"])
        # print(v1, "vs.", v2, "=", sim)
    
    if not closest["user"]:
      print(f"{test_filename} : No user similar to {U} found with movie rating on {M}")
      results.append((U, M, 3))
    else:
      results.append((U, M, data[closest["user"]][M]))

  ifile.close()

  ofile = open(out_filename, "w")
  for result in results:
    ofile.write(f"{result[0]} {result[1]} {result[2]}\n")
  ofile.close()

v1("train.txt", "test5.txt", "results/result5.txt")
v1("train.txt", "test10.txt", "results/result10.txt")
v1("train.txt", "test20.txt", "results/result20.txt")