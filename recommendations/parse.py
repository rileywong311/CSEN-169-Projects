import numpy as np
from collections import defaultdict

# train.txt
#  200 users
#  1000 movies
#  1-5 rating 


def get_data_dict(filename):
  data = defaultdict(dict)
  ifile = open(filename)
  for line in ifile:
    U, M, R = map(int, line.split())
    data[U][M] = R
  ifile.close()
  return data


def get_data_dict_T(filename):
  data = defaultdict(dict)
  ifile = open(filename)
  for line in ifile:
    U, M, R = map(int, line.split())
    data[M][U] = R
  ifile.close()
  return data


def get_data_matrix(filename):
  data = np.empty((200, 1000))
  ifile = open(filename)
  for line in ifile:
    U, M, R = map(int, line.split())
    data[U-1][M-1] = R
  ifile.close()
  return data


def get_data_matrix_T(filename):
  data = np.empty((1000, 200))
  ifile = open(filename)
  for line in ifile:
    U, M, R = map(int, line.split())
    data[M-1][U-1] = R
  ifile.close()
  return data
  

def get_data_averages(filename):
  def avg(lst):
    if not lst:
      return None
    return np.average(lst)
  
  data = get_data_matrix(filename)
  rows, cols = data.shape
  averages = [avg([data[row][col] for row in range(rows) if data[row][col] != 0]) for col in range(cols)]
  return averages


def get_data_credited_averages(filename):
  data = get_data_dict_T(filename)
  data2 = get_data_dict(filename)
  credited_averages = []
  for movie in range(1, 1001):
    if movie not in data:
      credited_averages.append(None)
      continue

    denom = 0
    numer = 0
    for user in data[movie]:
        # credit = np.sqrt(len(data[user]))
        # credit = len(data[user])
        # credit = np.log2(200/len(data[user]))
        stddev = np.std(list(data2[user].values()))
        # print(stddev)
        if stddev == 0:
          credit = 0.5
        else:
          credit = stddev**2
      
        denom += credit
        numer += data[movie][user] * credit
    if not denom:
      new_avg = None
    else:
      new_avg = numer/denom
    credited_averages.append(new_avg)
  return credited_averages


def get_data_stddev(filename):
  def avg(lst):
    if not lst:
      return None
    return np.average(lst)
  
  averages = get_data_averages(filename)
  data = get_data_dict_T(filename)
  stddevs = []
  for movie in range(1, 1001):
    if movie in data:
      numer = 0
      for user in data[movie]:
        numer += (data[movie][user] - averages[movie-1])**2
      # numer = sum([(data[movie][user] - averages[movie-1])**2 for user in data[movie]])
      denom = len(data[movie])
      stddev =  np.sqrt(numer/denom)
      # print(movie, ":", data[movie].values(), "=", numer, "/", denom, "=>", numer/denom, "and stddev =", stddev)
      stddevs.append(stddev)
    else:
      stddevs.append(None)
  return stddevs


def get_data_IUFs(filename):
  data = get_data_matrix(filename)
  rows, cols = data.shape
  counts = [len([data[row][col] for row in range(rows) if data[row][col] != 0]) for col in range(cols)]
  IUFs = list(map(lambda count: np.log2(rows/count) if count else np.log2(rows), counts))
  return IUFs


def get_data_Inverse_IUFs(filename):
  data = get_data_matrix(filename)
  rows, cols = data.shape
  counts = [len([data[row][col] for row in range(rows) if data[row][col] != 0]) for col in range(cols)]
  # IIUFs = list(map(lambda count: np.sqrt(count)/rows, counts))
  IIUFs = list(map(lambda count: count/rows, counts))
  return IIUFs
