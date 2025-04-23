# Protocol

## 23.04.2025

### Data preparation

```
wget https://database.lichess.org/standard/lichess_db_standard_rated_2013-01.pgn.zst
unzstd lichess_db_standard_rated_2013-01.pgn.zst
```

### Environment preparation
[Selected from here](https://wiki.python.org/moin/PythonGraphLibraries)

For now my (Denys) choice is to use graph-tool as the fastest method (maybe rustworkx will be faster).

```
mamba create -n scinet
mamba install networkx python-igraph numpy pandas matplotlib graph-tool 
```