import recommend

do = 2

# -----------------
# USER-BASED COSINE
# -----------------
if do == 1:
  recommend.v1("train.txt", "test5.txt", "results/result5.txt")
  recommend.v1("train.txt", "test10.txt", "results/result10.txt")
  recommend.v1("train.txt", "test20.txt", "results/result20.txt")

# -------------------
# USER-BASED PEARSONS
# -------------------
if do == 2:
  recommend.v2("train.txt", "test5.txt", "results/result5.txt")
  recommend.v2("train.txt", "test10.txt", "results/result10.txt")
  recommend.v2("train.txt", "test20.txt", "results/result20.txt")
