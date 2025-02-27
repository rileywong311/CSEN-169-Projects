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


def get_data_matrix(filename):
  data = np.empty((200, 1000))
  ifile = open(filename)
  for line in ifile:
    U, M, R = map(int, line.split())
    data[U-1][M-1] = R
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