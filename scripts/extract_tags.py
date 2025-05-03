import argparse

def preprocess(string:str):
    string = string.strip()
    return string[string.find('[') + 1:string.find(' ')]


parser = argparse.ArgumentParser(description='''
Program for extracting all possible tags from pgn files
''')

parser.add_argument('input', help='Name of a file to open')
parser.add_argument('output', help='Name of output file')

args = parser.parse_args()

tags = set()

with open(args.input) as fi:
    while True:
        while (line:=fi.readline()).strip() != '':
            tags.add(preprocess(line))
        
        fi.readline()
        fi.readline()

        if line == '':
            break

with open(args.output, 'w') as fo:
    for elem in tags:
        print(f'"{elem}",', file=fo)