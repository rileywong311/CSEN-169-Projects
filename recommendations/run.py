import recommend
import ensemble

do = 18

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

# -----------------------
# USER-BASED PEARSONS IUF
# -----------------------

if do == 3:
  recommend.v3("train.txt", "test5.txt", "results/result5.txt")
  recommend.v3("train.txt", "test10.txt", "results/result10.txt")
  recommend.v3("train.txt", "test20.txt", "results/result20.txt")

# --------------------------------------
# USER-BASED PEARSONS CASE AMPLIFICATION
# --------------------------------------

if do == 4:
  recommend.v4("train.txt", "test5.txt", "results/result5.txt")
  recommend.v4("train.txt", "test10.txt", "results/result10.txt")
  recommend.v4("train.txt", "test20.txt", "results/result20.txt")


# ---------------------------------------------
# USER-BASED PEARSONS IUF && CASE AMPLIFICATION
# ---------------------------------------------

if do == 5:
  recommend.v5("train.txt", "test5.txt", "results/result5.txt")
  recommend.v5("train.txt", "test10.txt", "results/result10.txt")
  recommend.v5("train.txt", "test20.txt", "results/result20.txt")


# ---------------------------------------------
# ITEM-BASED COSINE
# ---------------------------------------------

if do == 6:
  recommend.v6("train.txt", "test5.txt", "results/result5.txt")
  recommend.v6("train.txt", "test10.txt", "results/result10.txt")
  recommend.v6("train.txt", "test20.txt", "results/result20.txt")

# ---------------------------------------------
# USER-BASED COSINE IUF
# ---------------------------------------------

if do == 7:
  recommend.v7("train.txt", "test5.txt", "results/result5.txt")
  recommend.v7("train.txt", "test10.txt", "results/result10.txt")
  recommend.v7("train.txt", "test20.txt", "results/result20.txt")

# ---------------------------------------------
# USER-BASED PEARSON > ITEM BASED COSINE
# ---------------------------------------------

if do == 8:
  recommend.v8("train.txt", "test5.txt", "results/result5.txt")
  recommend.v8("train.txt", "test10.txt", "results/result10.txt")
  recommend.v8("train.txt", "test20.txt", "results/result20.txt")


# ---------------------------------------------
# AVERAGE RATING
# ---------------------------------------------

if do == 9:
  recommend.v9("train.txt", "test5.txt", "results/result5.txt")
  recommend.v9("train.txt", "test10.txt", "results/result10.txt")
  recommend.v9("train.txt", "test20.txt", "results/result20.txt")

# ---------------------------------------------
# USER-BASED PEARSON IUF > AVERAGE RATING
# ---------------------------------------------

if do == 10:
  recommend.v10("train.txt", "test5.txt", "results/result5.txt")
  recommend.v10("train.txt", "test10.txt", "results/result10.txt")
  recommend.v10("train.txt", "test20.txt", "results/result20.txt")

# ---------------------------------------------
# STD. DEV. THRESHOLD > USER-BASED PEARSON IUF
# ---------------------------------------------

if do == 11:
  recommend.v11("train.txt", "test5.txt", "results/result5.txt")
  recommend.v11("train.txt", "test10.txt", "results/result10.txt")
  recommend.v11("train.txt", "test20.txt", "results/result20.txt")


# ---------------------------------------------
# USER-BASED PEARSON IIUF > AVERAGE RATING
# ---------------------------------------------

if do == 12:
  recommend.v12("train.txt", "test5.txt", "results/result5.txt")
  recommend.v12("train.txt", "test10.txt", "results/result10.txt")
  recommend.v12("train.txt", "test20.txt", "results/result20.txt")

# ---------------------------------------------
# STD. DEV. THRESHOLD > USER-BASED COSINE
# ---------------------------------------------

if do == 13:
  recommend.v13("train.txt", "test5.txt", "results/result5.txt")
  recommend.v13("train.txt", "test10.txt", "results/result10.txt")
  recommend.v13("train.txt", "test20.txt", "results/result20.txt")


# ---------------------------------------------
# CREDITED AVERAGE RATING
# ---------------------------------------------

if do == 14:
  recommend.v14("train.txt", "test5.txt", "results/result5.txt")
  recommend.v14("train.txt", "test10.txt", "results/result10.txt")
  recommend.v14("train.txt", "test20.txt", "results/result20.txt")


# ---------------------------------------------
# USER-BASED COSINE > AVERAGE RATING
# ---------------------------------------------

if do == 15:
  recommend.v15("train.txt", "test5.txt", "results/result5.txt")
  recommend.v15("train.txt", "test10.txt", "results/result10.txt")
  recommend.v15("train.txt", "test20.txt", "results/result20.txt")


# ---------------------------------------------
# STD. DEV. THRESHOLD > USER-BASED PEARSON IIUF
# ---------------------------------------------

if do == 16:
  recommend.v16("train.txt", "test5.txt", "results/result5.txt")
  recommend.v16("train.txt", "test10.txt", "results/result10.txt")
  recommend.v16("train.txt", "test20.txt", "results/result20.txt")


# ---------------------------------------------
# ENSEMBLE
# ---------------------------------------------

if do == 17:
  # recommend.v17("train.txt", "test5.txt", "results/result5.txt", K=(1, 2, 1, 1, 1))
  # recommend.v17("train.txt", "test10.txt", "results/result10.txt", K=(1, 2, 1, 1, 1))
  # recommend.v17("train.txt", "test20.txt", "results/result20.txt", K=(1, 2, 1, 1, 1))

  recommend.v17("train.txt", "test5.txt", "results/result5_1.txt", K=(2, 2, 1, 1, 0))
  recommend.v17("train.txt", "test10.txt", "results/result10_1.txt", K=(2, 2, 1, 1, 1))
  recommend.v17("train.txt", "test20.txt", "results/result20_1.txt", K=(2, 2, 1, 1, 1))

# ---------------------------------------------
# ENSEMBLE MODIFIED
# ---------------------------------------------

if do == 18:
  print("18")
  ensemble.ensemble("train.txt", "test5.txt", "results/result5.txt", K=(2, 2, 2, 1, 1))
  ensemble.ensemble("train.txt", "test10.txt", "results/result10.txt", K=(2, 2, 2, 1, 1))
  ensemble.ensemble("train.txt", "test20.txt", "results/result20.txt", K=(2, 2, 2, 1, 1))

  # ensemble.ensemble("train.txt", "test5.txt", "results/result5_3.txt", K=(2, 2, 2, 1, 1))
  # ensemble.ensemble("train.txt", "test10.txt", "results/result10_3.txt", K=(2, 2, 2, 1, 1))
  # ensemble.ensemble("train.txt", "test20.txt", "results/result20_3.txt", K=(2, 2, 2, 1, 1))