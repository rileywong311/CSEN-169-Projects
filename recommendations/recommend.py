from parse import get_data_dict, get_data_averages, get_data_IUFs
from collections import defaultdict
import numpy as np
import heapq

averages = get_data_averages('train.txt')
def get_movie_average(movie):
  result = averages[movie-1]
  if not result:
    return 3
  return round(result)

IUFs = get_data_IUFs('train.txt')
def get_movie_IUF(movie):
  result = IUFs[movie-1]
  return result


def cosine_similarity(v1, v2):
  normalize = np.linalg.norm(v1) * np.linalg.norm(v2)
  if not normalize:
    return 0
  return np.dot(v1, v2) / normalize


def pearson_correlation(v1, avg1, v2, avg2):
  v1_neutral = np.array(list(map(lambda x: x - avg1, v1)))
  v2_neutral = np.array(list(map(lambda x: x - avg2, v2)))
  w = cosine_similarity(v1_neutral, v2_neutral)
  # print(v1, v2, '<=>', v1_neutral, v2_neutral, '=', w)
  return w
  

def v1(train_filename, test_filename, out_filename, K=30):
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

  if out_filename:
    ofile = open(out_filename, "w")
    for result in results:
      ofile.write(f"{result[0]} {result[1]} {result[2]}\n")
    ofile.close()

  return results


def v2(train_filename, test_filename, out_filename, K=30):
  data = get_data_dict(train_filename)

  test = defaultdict(dict)  
  results = []
  ifile = open(test_filename)
  
  for line in ifile:
    U, M, R = map(int, line.split())

    if R:
      test[U][M] = R
      # center1 = np.average(list(test[U].values()))
      continue
    
    min_heap = []
    for user in data:
      if M not in data[user]:
        continue
      intersect = set(test[U].keys()) & set(data[user].keys())

      # print(U, "&", user, "=", intersect)

      if intersect:
        center1 = np.average(list(test[U].values()))
        center2 = np.average(list(data[user].values()))
        v1 = np.array([test[U][movie] for movie in intersect])
        v2 = np.array([data[user][movie] for movie in intersect])
        w = pearson_correlation(v1, center1, v2, center2)
        n = w * (data[user][M] - center2)
        d = abs(w)
        if len(min_heap) < K:
          heapq.heappush(min_heap, (d, n))
        else:
          heapq.heappushpop(min_heap, (d, n))

        # print(v1, "vs.", v2, "=", sim)
    
    numer = [i[1] for i in min_heap]
    denom = [i[0] for i in min_heap]
    if not (numer and denom):
      print(f"{test_filename} : No user similar to {U} found with movie rating on {M}")
      results.append((U, M, 3))
      # results.append((U, M, get_movie_average(M)))
    elif not sum(denom):
      print(f"{test_filename} : User {U} has sum(w) = 0")
      results.append((U, M, 3))
      # results.append((U, M, get_movie_average(M)))
    else:
      p = round(center1 + sum(numer)/sum(denom))
      p = max(1, min(p, 5))
      results.append((U, M, p))

  ifile.close()

  if out_filename:
    ofile = open(out_filename, "w")
    for result in results:
      ofile.write(f"{result[0]} {result[1]} {result[2]}\n")
    ofile.close()

  return results


def v3(train_filename, test_filename, out_filename, K=30):
  data = get_data_dict(train_filename)

  test = defaultdict(dict)  
  results = []
  ifile = open(test_filename)
  
  for line in ifile:
    U, M, R = map(int, line.split())

    if R:
      test[U][M] = R
      continue
    
    center1 = np.average(list(test[U].values()))
    min_heap = []
    for user in data:
      if M not in data[user]:
        continue
      intersect = set(test[U].keys()) & set(data[user].keys())
      # if len(intersect) > 1:
      if intersect:
        center2 = np.average(list(data[user].values()))
        IUF_center1 = np.average([get_movie_IUF(movie) * test[U][movie] for movie in test[U]])
        IUF_center2 = np.average([get_movie_IUF(movie) * data[user][movie] for movie in data[user]])
        IUF_v1 = np.array([get_movie_IUF(movie) * test[U][movie] for movie in intersect])
        IUF_v2 = np.array([get_movie_IUF(movie) * data[user][movie] for movie in intersect])
        w = pearson_correlation(IUF_v1, IUF_center1, IUF_v2, IUF_center2)
        n = w * (data[user][M] - center2)
        d = abs(w)
        if len(min_heap) < K:
          heapq.heappush(min_heap, (d, n))
        else:
          heapq.heappushpop(min_heap, (d, n))
    
    numer = [i[1] for i in min_heap]
    denom = [i[0] for i in min_heap]
    if not (numer and denom):
      print(f"{test_filename} : No user similar to {U} found with movie rating on {M}")
      results.append((U, M, 3))
    elif not sum(denom):
      print(f"{test_filename} : User {U} has sum(w) = 0")
      results.append((U, M, 3))
    else:
      p = round(center1 + sum(numer)/sum(denom))
      p = max(1, min(p, 5))
      results.append((U, M, p))

  ifile.close()

  if out_filename:
    ofile = open(out_filename, "w")
    for result in results:
      ofile.write(f"{result[0]} {result[1]} {result[2]}\n")
    ofile.close()

  return results

def v4(train_filename, test_filename, out_filename, K=30):
  power = 1.5

  data = get_data_dict(train_filename)

  test = defaultdict(dict)  
  results = []
  ifile = open(test_filename)
  
  for line in ifile:
    U, M, R = map(int, line.split())

    if R:
      test[U][M] = R
      continue
    
    center1 = np.average(list(test[U].values()))
    min_heap = []
    for user in data:
      if M not in data[user]:
        continue
      intersect = set(test[U].keys()) & set(data[user].keys())
      if len(intersect) > 1:
        center2 = np.average(list(data[user].values()))
        v1 = np.array([test[U][movie] for movie in intersect])
        v2 = np.array([data[user][movie] for movie in intersect])
        w = pearson_correlation(v1, center1, v2, center2)
        w = w * (abs(w)**power)
        n = w * (data[user][M] - center2)
        d = abs(w)
        if len(min_heap) < K:
          heapq.heappush(min_heap, (d, n))
        else:
          heapq.heappushpop(min_heap, (d, n))
    
    numer = [i[1] for i in min_heap]
    denom = [i[0] for i in min_heap]
    if not (numer and denom):
      print(f"{test_filename} : No user similar to {U} found with movie rating on {M}")
      results.append((U, M, 3))
    elif not sum(denom):
      print(f"{test_filename} : User {U} has sum(w) = 0")
      results.append((U, M, 3))
    else:
      p = round(center1 + sum(numer)/sum(denom))
      p = max(1, min(p, 5))
      results.append((U, M, p))

  ifile.close()

  if out_filename:
    ofile = open(out_filename, "w")
    for result in results:
      ofile.write(f"{result[0]} {result[1]} {result[2]}\n")
    ofile.close()

  return results

def v5(train_filename, test_filename, out_filename, K=30):
  power=1.5
  data = get_data_dict(train_filename)

  test = defaultdict(dict)  
  results = []
  ifile = open(test_filename)
  
  for line in ifile:
    U, M, R = map(int, line.split())

    if R:
      test[U][M] = R
      continue
    
    center1 = np.average(list(test[U].values()))
    min_heap = []
    for user in data:
      if M not in data[user]:
        continue
      intersect = set(test[U].keys()) & set(data[user].keys())
      # if len(intersect) > 1:
      if intersect:
        center2 = np.average(list(data[user].values()))
        IUF_center1 = np.average([get_movie_IUF(movie) * test[U][movie] for movie in test[U]])
        IUF_center2 = np.average([get_movie_IUF(movie) * data[user][movie] for movie in data[user]])
        IUF_v1 = np.array([get_movie_IUF(movie) * test[U][movie] for movie in intersect])
        IUF_v2 = np.array([get_movie_IUF(movie) * data[user][movie] for movie in intersect])
        w = pearson_correlation(IUF_v1, IUF_center1, IUF_v2, IUF_center2)
        w = w * (abs(w)**power)
        n = w * (data[user][M] - center2)
        d = abs(w)
        if len(min_heap) < K:
          heapq.heappush(min_heap, (d, n))
        else:
          heapq.heappushpop(min_heap, (d, n))
    
    numer = [i[1] for i in min_heap]
    denom = [i[0] for i in min_heap]
    if not (numer and denom):
      print(f"{test_filename} : No user similar to {U} found with movie rating on {M}")
      results.append((U, M, 3))
    elif not sum(denom):
      print(f"{test_filename} : User {U} has sum(w) = 0")
      results.append((U, M, 3))
    else:
      p = round(center1 + sum(numer)/sum(denom))
      p = max(1, min(p, 5))
      results.append((U, M, p))

  ifile.close()

  if out_filename:
    ofile = open(out_filename, "w")
    for result in results:
      ofile.write(f"{result[0]} {result[1]} {result[2]}\n")
    ofile.close()

  return results