# Protocol

## 23.04.2025 (Denys)

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

## Night 24/25.04.2025 (Denys)
Just for fun: 
```
perl -F";" -lane 'print $F[9]' test.csv | sort | uniq > term.txt
perl -F, -lane 'print $F[2]' data/lichess_db_standard_rated_2016-01.csv > whites.txt
perl -F, -lane 'print $F[3]' data/lichess_db_standard_rated_2016-01.csv > blacks.txt

cat whites.txt blacks.txt | sort | uniq | wc -l
```
Output: `92506`.

New scripts were added: `csv_to_graphml.py` and `visualize_xml.py`. (For now only edges, without info)
*Idea*:  using of unique code we can add to any game, so in worst case we only need node-edge-node-elo-unique_code information (so we do not need to use a lot of space...)

For `2013-01`:
```
python scripts/csv_to_graphml.py data/csv/lichess_db_standard_rated_2013-01.csv data/std1301.xml
```
runs `583 ms`.

```
python scripts/visualize_xml.py data/std1301.xml data/std1301.png
```

runs ~`30 s` (depends on resolution and filetype).

For `2016-01`:
```
python scripts/csv_to_graphml.py data/csv/lichess_db_standard_rated_2016-01.csv data/std1601.xml
python scripts/visualize_xml.py data/std1601.xml data/std1601.png
```
The first runs in `~45 s`.
The second runs in `~15 m`.

Conclusion: TODO: rewrite visualize_xml.py into 2 several files: we can save in gt format position of vertices, so there will be no need to recalculate this funny positions over and over again (pretty complex for computer...)