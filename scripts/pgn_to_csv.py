import argparse
import csv

def preprocess(string:str):
    string = string.strip()
    return string[string.find('"') + 1:string.rfind('"')]
    # return string[:string.find('"') + 1]


parser = argparse.ArgumentParser(description='''
Program for converting pgn files into csv with only relevant information.
                                 
Data format: 
Event,Site,White,Black,Result,UTCDate,UTCTime,WhiteElo,BlackElo,WhiteRatingDiff,BlackRatingDiff,ECO,Opening,TimeControl,Termination
''')

parser.add_argument('input', help='Name of a file to open')
parser.add_argument('output', help='Name of csv output')

args = parser.parse_args()

with open(args.output, 'w') as fo:
    writer = csv.writer(fo)
    with open(args.input) as fi:
        while True:
            row = []
            while (line:=fi.readline()).strip() != '':
                row.append(preprocess(line))

            if len(row) == 0:
                break
            
            writer.writerow(row)
            game = fi.readline()
            empty = fi.readline()

    