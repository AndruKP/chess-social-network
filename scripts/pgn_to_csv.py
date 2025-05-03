import argparse
import csv

def tag(string:str):
    string = string.strip()
    return string[string.find('[') + 1:string.find(' ')]
    # return string[:string.find('"') + 1]

def preprocess(string:str):
    string = string.strip()
    return string[string.find('"') + 1:string.rfind('"')]
    # return string[:string.find('"') + 1]

FIELDNAMES = [
    "White",
    "Black",
    "Result",
    "BlackElo",
    "BlackRatingDiff",
    "BlackTitle",
    "ECO",
    "Event",
    "Opening",
    "Site",
    "Termination",
    "TimeControl",
    "UTCDate",
    "UTCTime",
    "WhiteElo",
    "WhiteRatingDiff",
    "WhiteTitle"
] 

parser = argparse.ArgumentParser(description='''
Program for converting pgn files into csv with only relevant information.
                                 
Data format: 
    "White","Black","Result","BlackElo","BlackRatingDiff","BlackTitle","ECO","Event","Opening","Site","Termination","TimeControl","UTCDate","UTCTime","WhiteElo","WhiteRatingDiff","WhiteTitle"
''')

parser.add_argument('input', help='Name of a file to open')
parser.add_argument('output', help='Name of csv output')

args = parser.parse_args()

with open(args.output, 'w') as fo:
    writer = csv.DictWriter(fo, fieldnames = FIELDNAMES, restval = 'None', delimiter = ';')
    with open(args.input) as fi:
        while True:
            row = {}
            while (line:=fi.readline()).strip() != '':
                row[tag(line)] = preprocess(line)

            if len(row) == 0:
                break
            
            writer.writerow(row)
            game = fi.readline()
            empty = fi.readline()

    