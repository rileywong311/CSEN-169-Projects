from parse import get_data_dict, get_data_dict_T, get_data_stddev, get_data_averages, get_data_IUFs, get_data_Inverse_IUFs, get_data_credited_averages
from collections import defaultdict
import numpy as np
import heapq

averages = get_data_averages('train.txt')
def get_movie_average(movie):
  result = averages[movie-1]
  if not result:
    return 3
  # return round(result)
  return result

IUFs = get_data_IUFs('train.txt')
def get_movie_IUF(movie):
  result = IUFs[movie-1]
  return result

IIUFs = get_data_Inverse_IUFs('train.txt')
def get_movie_IIUF(movie):
  result = IIUFs[movie-1]
  return result

stddevs = get_data_stddev('train.txt')
def get_movie_stddev(movie):
  result = stddevs[movie-1]
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
  return w
  

def cosine_model(train_filename, test_filename, out_filename, K=30):
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
      if intersect:
        v1 = np.array([test[U][movie] for movie in intersect])
        v2 = np.array([data[user][movie] for movie in intersect])
        sim = cosine_similarity(v1, v2)
        if len(min_heap) < K:
          heapq.heappush(min_heap, (sim, user))
        else:
          heapq.heappushpop(min_heap, (sim, user))
    
    if not min_heap:
      results.append((U, M, get_movie_average(M)))
    else:
      weighted_average = sum([neighbor[0] * data[neighbor[1]][M] for neighbor in min_heap]) / sum([neighbor[0] for neighbor in min_heap])
      results.append((U, M, weighted_average))

  ifile.close()

  if out_filename:
    ofile = open(out_filename, "w")
    for result in results:
      ofile.write(f"{result[0]} {result[1]} {result[2]}\n")
    ofile.close()

  return results


def pearson_IUF_model(train_filename, test_filename, out_filename, K=30):
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
      if intersect:
        center2 = np.average(list(data[user].values()))
        IUF_center1 = np.average([get_movie_IUF(movie) * test[U][movie] for movie in test[U]])
        IUF_center2 = np.average([get_movie_IUF(movie) * data[user][movie] for movie in data[user]])
        IUF_v1 = np.array([get_movie_IUF(movie) * test[U][movie] for movie in intersect])
        IUF_v2 = np.array([get_movie_IUF(movie) * data[user][movie] for movie in intersect])
        w = pearson_correlation(IUF_v1, IUF_center1, IUF_v2, IUF_center2)
        w = w * np.sqrt(len(intersect))
        n = w * (data[user][M] - center2)
        d = abs(w)
        if len(min_heap) < K:
          heapq.heappush(min_heap, (d, n))
        else:
          heapq.heappushpop(min_heap, (d, n))
    
    numer = [i[1] for i in min_heap]
    denom = [i[0] for i in min_heap]
    if not (numer and denom):
      results.append((U, M, get_movie_average(M)))
    elif not sum(denom):
      results.append((U, M, get_movie_average(M)))
    else:
      p = center1 + sum(numer)/sum(denom)
      p = max(1, min(p, 5))
      results.append((U, M, p))

  ifile.close()

  if out_filename:
    ofile = open(out_filename, "w")
    for result in results:
      ofile.write(f"{result[0]} {result[1]} {result[2]}\n")
    ofile.close()

  return results


def cosine_item_model(train_filename, test_filename, out_filename, K=100):
  data = get_data_dict_T(train_filename)

  test = defaultdict(dict)
  results = []
  ifile = open(test_filename)
  for line in ifile:
    U, M, R = map(int, line.split())

    if R:
      test[U][M] = R
      continue
    
    item_similarities = []
    for movie in test[U]:
      v1 = []
      v2 = []
      for user in data[movie]:
        if user in data[M]:
          v1.append(data[movie][user])
          v2.append(data[M][user])
      if len(v1) == 0:
        sim = 0
      else:
        sim = cosine_similarity(np.array(v1), np.array(v2))
      item_similarities.append((sim, movie))

    
    item_similarities = sorted(item_similarities, reverse=True)[:K]
    if sum([i[0] for i in item_similarities]) == 0:
      results.append((U, M, get_movie_average(M)))
    else:
      weighted_average = sum([i[0] * test[U][i[1]] for i in item_similarities]) / sum([i[0] for i in item_similarities])
      results.append((U, M, weighted_average))

  ifile.close()

  if out_filename:
    ofile = open(out_filename, "w")
    for result in results:
      ofile.write(f"{result[0]} {result[1]} {result[2]}\n")
    ofile.close()

  return results


def averages_model(train_filename, test_filename, out_filename, K=None):
  results = []
  ifile = open(test_filename)
  for line in ifile:
    U, M, R = map(int, line.split())

    if R:
      continue

    results.append((U, M, get_movie_average(M)))

  ifile.close()

  if out_filename:
    ofile = open(out_filename, "w")
    for result in results:
      ofile.write(f"{result[0]} {result[1]} {result[2]}\n")
    ofile.close()
  return results


def do_pearson_IIUF(U, M, data, test, K):
  center1 = np.average(list(test[U].values()))
  min_heap = []
  for user in data:
    if M not in data[user]:
      continue
    intersect = set(test[U].keys()) & set(data[user].keys())
    if intersect:
      center2 = np.average(list(data[user].values()))
      IIUF_center1 = np.average([get_movie_IIUF(movie) * test[U][movie] for movie in test[U]])
      IIUF_center2 = np.average([get_movie_IIUF(movie) * data[user][movie] for movie in data[user]])
      IIUF_v1 = np.array([get_movie_IIUF(movie) * test[U][movie] for movie in intersect])
      IIUF_v2 = np.array([get_movie_IIUF(movie) * data[user][movie] for movie in intersect])
      w = pearson_correlation(IIUF_v1, IIUF_center1, IIUF_v2, IIUF_center2)
      w = w * np.sqrt(len(intersect))
      n = w * (data[user][M] - center2)
      d = abs(w)
      if len(min_heap) < K:
        heapq.heappush(min_heap, (d, n))
      else:
        heapq.heappushpop(min_heap, (d, n))
  
  numer = [i[1] for i in min_heap]
  denom = [i[0] for i in min_heap]

  if not (numer and denom):
    return None
  if not sum(denom):
    return None
  p = round(center1 + sum(numer)/sum(denom))
  p = max(1, min(p, 5))
  return p


def pearson_IIUF_model(train_filename, test_filename, out_filename, K=40):
  data = get_data_dict(train_filename)
  test = defaultdict(dict)  

  results = []
  ifile = open(test_filename)
  
  for line in ifile:
    U, M, R = map(int, line.split())

    if R:
      test[U][M] = R
      continue
    
    rating = do_pearson_IIUF(U, M, data, test, K)
    if not rating:
      rating = get_movie_average(M)
    results.append((U, M, rating))

  ifile.close()

  if out_filename:
    ofile = open(out_filename, "w")
    for result in results:
      ofile.write(f"{result[0]} {result[1]} {result[2]}\n")
    ofile.close()

  return results


def ensemble(train_filename, test_filename, out_filename, K=(1, 1, 1, 1, 1)):
  results1 = averages_model(train_filename, test_filename, out_filename, K=None) # just averages
  results2 = pearson_IIUF_model(train_filename, test_filename, out_filename, K=50) # pearson IIUF and SQRT(intersect)
  results3 = cosine_model(train_filename, test_filename, out_filename, K=30) # user-based cosine
  results4 = cosine_item_model(train_filename, test_filename, out_filename, K=20) # item-based cosine
  results5 = pearson_IUF_model(train_filename, test_filename, out_filename, K=30) # pearson IUF
  

  assert(len(results1) == len(results2) == len(results3) == len(results4) == len(results5))
  results = []
  for i in range(len(results1)):
    rating = sum([K[0] * results1[i][2], 
                  K[1] * results2[i][2], 
                  K[2] * results3[i][2], 
                  K[3] * results4[i][2]], 
                  K[4] * results5[i][2]) / sum(K)

    results.append((results1[i][0], results1[i][1], round(rating)))

  if out_filename:
    ofile = open(out_filename, "w")
    for result in results:
      ofile.write(f"{result[0]} {result[1]} {result[2]}\n")
    ofile.close()

  return results