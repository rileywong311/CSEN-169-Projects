from parse import get_data_dict, get_data_dict_T, get_data_stddev, get_data_averages, get_data_IUFs, get_data_Inverse_IUFs, get_data_credited_averages
from collections import defaultdict
import numpy as np
import heapq

averages = get_data_averages('train.txt')
def get_movie_average(movie):
  result = averages[movie-1]
  if not result:
    return 3
  return round(result)

credited_averages = get_data_credited_averages('train.txt')
def get_movie_credited_average(movie):
  result = credited_averages[movie-1]
  if not result:
    return 3
  return round(result)

# print(averages[:5])
# print(credited_averages[:5])

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
      # if len(intersect) > 1:
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


def v6(train_filename, test_filename, out_filename, K=100):
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
      # print(movie)
      v1 = []
      v2 = []
      for user in data[movie]:
        if user in data[M]:
          # print(f"{user} rated {movie} and {M}")
          v1.append(data[movie][user])
          v2.append(data[M][user])
      if len(v1) == 0:
        sim = 0
      else:
        sim = cosine_similarity(np.array(v1), np.array(v2))
      item_similarities.append((sim, movie))

    
    item_similarities = sorted(item_similarities, reverse=True)[:K]
    # print(f"user {U} on movie {M} has {item_similarities}")
    if sum([i[0] for i in item_similarities]) == 0:
      print(f"{test_filename} : User {U} with on rating for movie {M} has no item similarities")
      results.append((U, M, 3))
    else:
      weighted_average = sum([i[0] * test[U][i[1]] for i in item_similarities]) / sum([i[0] for i in item_similarities])
      results.append((U, M, round(weighted_average)))

  ifile.close()

  if out_filename:
    ofile = open(out_filename, "w")
    for result in results:
      ofile.write(f"{result[0]} {result[1]} {result[2]}\n")
    ofile.close()

  return results


def v7(train_filename, test_filename, out_filename, K=30):
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
        v1 = np.array([get_movie_IUF(movie) * test[U][movie] for movie in intersect])
        v2 = np.array([get_movie_IUF(movie) * data[user][movie] for movie in intersect])
        sim = cosine_similarity(v1, v2)
        if len(min_heap) < K:
          heapq.heappush(min_heap, (sim, user))
        else:
          heapq.heappushpop(min_heap, (sim, user))
    
    if not min_heap:
      print(f"{test_filename} : No user similar to {U} found with movie rating on {M}")
      results.append((U, M, 3))
    else:
      weighted_average = sum([neighbor[0] * data[neighbor[1]][M] for neighbor in min_heap]) / sum([neighbor[0] for neighbor in min_heap])
      results.append((U, M, round(weighted_average)))

  ifile.close()

  if out_filename:
    ofile = open(out_filename, "w")
    for result in results:
      ofile.write(f"{result[0]} {result[1]} {result[2]}\n")
    ofile.close()

  return results




def do_pearson(U, M, data, test, K):
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
    # print(f"{test_filename} : No user similar to {U} found with movie rating on {M}")
    return None
  if not sum(denom):
    # print(f"{test_filename} : User {U} has sum(w) = 0")
    return None
  p = round(center1 + sum(numer)/sum(denom))
  p = max(1, min(p, 5))
  return p

def do_item_cosine(U, M, data, test, K):
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
    # print(f"{test_filename} : User {U} with on rating for movie {M} has no item similarities")
    return None
  result = sum([i[0] * test[U][i[1]] for i in item_similarities]) / sum([i[0] for i in item_similarities])
  return result


def v8(train_filename, test_filename, out_filename, K=(40, 20)):
  data = get_data_dict(train_filename)
  test = defaultdict(dict)  

  results = []
  ifile = open(test_filename)
  
  for line in ifile:
    U, M, R = map(int, line.split())

    if R:
      test[U][M] = R
      continue
    
    rating = do_pearson(U, M, data, test, K[0])
    if not rating:
      print(f"{test_filename} : Pearson Correlation fail on user {U} and movie {M}")
      rating = do_item_cosine(U, M, data, test, K[1])
    if not rating:
      print(f"{test_filename} : Item-Based Cosine fail on user {U} and movie {M}")
      rating = 3
    results.append((U, M, rating))

  ifile.close()

  if out_filename:
    ofile = open(out_filename, "w")
    for result in results:
      ofile.write(f"{result[0]} {result[1]} {result[2]}\n")
    ofile.close()

  return results


def v9(train_filename, test_filename, out_filename, K=None):
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


def v10(train_filename, test_filename, out_filename, K=40):
  data = get_data_dict(train_filename)
  test = defaultdict(dict)  

  results = []
  ifile = open(test_filename)
  
  for line in ifile:
    U, M, R = map(int, line.split())

    if R:
      test[U][M] = R
      continue
    
    rating = do_pearson(U, M, data, test, K)
    if not rating:
      print(f"{test_filename} : Pearson Correlation fail on user {U} and movie {M} ", end="")
      rating = get_movie_average(M)
      print(f"setting rating to average = {rating}")
    results.append((U, M, rating))

  ifile.close()

  if out_filename:
    ofile = open(out_filename, "w")
    for result in results:
      ofile.write(f"{result[0]} {result[1]} {result[2]}\n")
    ofile.close()

  return results


def v11(train_filename, test_filename, out_filename, K=40):
  data = get_data_dict(train_filename)
  test = defaultdict(dict)  

  results = []
  ifile = open(test_filename)
  
  for line in ifile:
    U, M, R = map(int, line.split())

    if R:
      test[U][M] = R
      continue
    
    stddev = get_movie_stddev(M)
    rating = None
    if stddev is not None and stddev < 1.2:
      rating = get_movie_average(M)
    if not rating:
      # print(f"{test_filename} : Bad stddev => doing pearson on user {U} and movie {M}")
      rating = do_pearson(U, M, data, test, K=K)
    if not rating:
      # print(f"\tBad pearson => defaulting to 3")
      rating = 3
    results.append((U, M, rating))

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
    # if len(intersect) > 1:
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
    # print(f"{test_filename} : No user similar to {U} found with movie rating on {M}")
    return None
  if not sum(denom):
    # print(f"{test_filename} : User {U} has sum(w) = 0")
    return None
  p = round(center1 + sum(numer)/sum(denom))
  p = max(1, min(p, 5))
  return p


def v12(train_filename, test_filename, out_filename, K=40):
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
      print(f"{test_filename} : Pearson Correlation fail on user {U} and movie {M} ", end="")
      rating = get_movie_average(M)
      print(f"setting rating to average = {rating}")
    results.append((U, M, rating))

  ifile.close()

  if out_filename:
    ofile = open(out_filename, "w")
    for result in results:
      ofile.write(f"{result[0]} {result[1]} {result[2]}\n")
    ofile.close()

  return results


def do_cosine(U, M, data, test, K):
  min_heap = []
  for user in data:
    if M not in data[user]:
      continue
    intersect = set(test[U].keys()) & set(data[user].keys())
    if intersect:
      v1 = np.array([test[U][movie] for movie in intersect])
      v2 = np.array([data[user][movie] for movie in intersect])
      sim = cosine_similarity(v1, v2)
      sim = sim * np.sqrt(len(intersect))
      if len(min_heap) < K:
        heapq.heappush(min_heap, (sim, user))
      else:
        heapq.heappushpop(min_heap, (sim, user))
  if not min_heap:
    return None
  else:
    return round(sum([neighbor[0] * data[neighbor[1]][M] for neighbor in min_heap]) / sum([neighbor[0] for neighbor in min_heap]))


def v13(train_filename, test_filename, out_filename, K=40):
  data = get_data_dict(train_filename)
  test = defaultdict(dict)  

  results = []
  ifile = open(test_filename)
  
  for line in ifile:
    U, M, R = map(int, line.split())

    if R:
      test[U][M] = R
      continue
    
    stddev = get_movie_stddev(M)
    rating = None
    if stddev is not None and stddev < 1.2:
      rating = get_movie_average(M)
    if not rating:
      # print(f"{test_filename} : Bad stddev => doing correlation on user {U} and movie {M}")
      rating = do_cosine(U, M, data, test, K=K)
    if not rating:
      # print(f"\tBad correlation => defaulting to average")
      rating = get_movie_average(M)
    results.append((U, M, rating))

  ifile.close()

  if out_filename:
    ofile = open(out_filename, "w")
    for result in results:
      ofile.write(f"{result[0]} {result[1]} {result[2]}\n")
    ofile.close()

  return results


def v14(train_filename, test_filename, out_filename, K=None):
  results = []
  ifile = open(test_filename)
  for line in ifile:
    U, M, R = map(int, line.split())

    if R:
      continue

    results.append((U, M, get_movie_credited_average(M)))

  ifile.close()

  if out_filename:
    ofile = open(out_filename, "w")
    for result in results:
      ofile.write(f"{result[0]} {result[1]} {result[2]}\n")
    ofile.close()
  return results


def v15(train_filename, test_filename, out_filename, K=50):
  data = get_data_dict(train_filename)
  test = defaultdict(dict)  

  results = []
  ifile = open(test_filename)
  
  for line in ifile:
    U, M, R = map(int, line.split())

    if R:
      test[U][M] = R
      continue
      
    rating = do_cosine(U, M, data, test, K=K)
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


def v16(train_filename, test_filename, out_filename, K=40):
  data = get_data_dict(train_filename)
  test = defaultdict(dict)  

  results = []
  ifile = open(test_filename)
  
  for line in ifile:
    U, M, R = map(int, line.split())

    if R:
      test[U][M] = R
      continue
    
    stddev = get_movie_stddev(M)
    rating = None
    if stddev is not None and stddev < 0.7:
      rating = get_movie_average(M)
    if not rating:
      rating = do_pearson(U, M, data, test, K=K)
    if not rating:
      rating = 3
    results.append((U, M, rating))

  ifile.close()

  if out_filename:
    ofile = open(out_filename, "w")
    for result in results:
      ofile.write(f"{result[0]} {result[1]} {result[2]}\n")
    ofile.close()

  return results



def v17(train_filename, test_filename, out_filename, K=(1, 1, 1, 1, 1)):
  results1 = v9(train_filename, test_filename, out_filename, K=None) # just averages
  results2 = v12(train_filename, test_filename, out_filename, K=50) # pearson IIUF and SQRT(intersect)
  results3 = v1(train_filename, test_filename, out_filename, K=40) # user-based cosine
  results4 = v6(train_filename, test_filename, out_filename, K=20) # item-based cosine
  results5 = v3(train_filename, test_filename, out_filename, K=50) # pearson IUF
  

  assert(len(results1) == len(results2) == len(results3) == len(results4) == len(results5))
  results = []
  for i in range(len(results1)):
    rating = sum([K[0] * results1[i][2], 
                  K[1] * results2[i][2], 
                  K[2] * results3[i][2], 
                  K[3] * results4[i][2]], 
                  K[4] * results5[i][2]) / sum(K)

    results.append((results1[i][0], results1[i][1], round(rating)))
    # print(results[i])

  if out_filename:
    ofile = open(out_filename, "w")
    for result in results:
      ofile.write(f"{result[0]} {result[1]} {result[2]}\n")
    ofile.close()

  return results