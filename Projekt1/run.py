import argparse


# example usage:
# python needleman_wunsh.py -a seq1.txt -b seq2.txt -c config.txt -o output.txt

parser = argparse.ArgumentParser()

#-db DATABSE -u USERNAME -p PASSWORD -size 20
parser.add_argument("-a", "--seq1", help="Sekwencja nr 1")
parser.add_argument("-b", "--seq2", help="Sekwencja nr 2")
parser.add_argument("-c", "--config", help="Plik konfiguracyjny")
parser.add_argument("-o", "--output", help="Plik wyjsciowy")

args = parser.parse_args()

print( "Hostname {} User {} Password {} size {} ".format(
        args.seq1,
        args.seq2,
        args.config,
        args.output
        ))