from parse import get_data_dict
import numpy as np
import random

random.seed(69)
steps = [int(random.uniform(50, 250)) for _ in range(30)]
print(f"Seeded Steps: {steps}")

def generate_train_test_split(train_filename, sections):
  data = get_data_dict(train_filename)
  ofile1 = open(f"train_test/train.txt", "w")
  ofile2 = open(f"train_test/test5.txt", "w")
  ofile3 = open(f"train_test/test10.txt", "w")
  ofile4 = open(f"train_test/test20.txt", "w")
  ofile5 = open(f"train_test/ans5.txt", "w")
  ofile6 = open(f"train_test/ans10.txt", "w")
  ofile7 = open(f"train_test/ans20.txt", "w")
  for user in data:
    to_test = False
    for section in sections:
      if section[0] <= user <= section[1]:
        to_test = True
        break

    if not to_test:
      for movie in data[user]:
        ofile1.write(f"{user} {movie} {data[user][movie]}\n")
      continue

    start = user % 30
    movies_used = set()
    movies = list(data[user].keys())
    for i in range(20):
      if 20 > len(movies):
        print(f"Skipping user {user} as they only have {len(movies)} movies")
        break

      movie = movies[(start + steps[i]) % len(movies)]
      if movie in movies_used:
        j = 1
        while movie in movies_used:
          movie = movies[(start + steps[i] + j) % len(movies)]
          j += 1
      movies_used.add(movie)

      if i < 5:
        ofile2.write(f"{user} {movie} {data[user][movie]}\n")
      if i < 10:
        ofile3.write(f"{user} {movie} {data[user][movie]}\n")
      if i < 20:
        ofile4.write(f"{user} {movie} {data[user][movie]}\n")
    
    for movie in data[user]:
      if movie not in movies_used:
        ofile2.write(f"{user} {movie} 0\n")
        ofile3.write(f"{user} {movie} 0\n")
        ofile4.write(f"{user} {movie} 0\n")
        ofile5.write(f"{user} {movie} {data[user][movie]}\n")
        ofile6.write(f"{user} {movie} {data[user][movie]}\n")
        ofile7.write(f"{user} {movie} {data[user][movie]}\n")

  ofile1.close()
  ofile2.close()
  ofile3.close()
  ofile4.close()
  ofile5.close()
  ofile6.close()
  ofile7.close()


def train_test(func, K=30):
  def get_mae(results, ans):
    diffs = []
    for i, line in enumerate(ans):
      U, M, R = map(int, line.split())
      ans = (U, M, R)
      if U != results[i][0] or M != results[i][1]:
        print("Alignment Error")
      diff = abs(results[i][2] - ans[2])
      diffs.append(diff)
    return np.average(diffs)

  results5 = func("train_test/train.txt", "train_test/test5.txt", None, K=K)
  ifile = open("train_test/ans5.txt")
  mae5 = get_mae(results5, ifile.readlines())
  ifile.close()

  results10 = func("train_test/train.txt", "train_test/test10.txt", None, K=K)
  ifile = open("train_test/ans5.txt")
  mae10 = get_mae(results10, ifile.readlines())
  ifile.close()

  results20 = func("train_test/train.txt", "train_test/test20.txt", None, K=K)
  ifile = open("train_test/ans5.txt")
  mae20 = get_mae(results20, ifile.readlines())
  ifile.close()

  return mae5, mae10, mae20