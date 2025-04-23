# Protocol

## 23.04.2025

### Data preparation

```
wget https://database.lichess.org/standard/lichess_db_standard_rated_2013-01.pgn.zst
unzstd lichess_db_standard_rated_2013-01.pgn.zst

# resp. wget https://database.lichess.org/standard/lichess_db_standard_rated_2016-01.pgn.zst
# unzstd lichess_db_standard_rated_2016-01.pgn.zst
```

```
python scripts/pgn_to_csv.py lichess_db_standard_rated_2016-01.pgn lichess_db_standard_rated_2016-01.csv
```

### Environment preparation
[Selected from here](https://wiki.python.org/moin/PythonGraphLibraries)

For now my (Denys) choice is to use graph-tool as the fastest method (maybe rustworkx will be faster).

```
mamba create -n scinet
mamba install networkx python-igraph graph-tool numpy pandas matplotlib
```