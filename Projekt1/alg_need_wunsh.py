import numpy as np
import networkx as nx 
import argparse
import alg_need_wunch_func as fa


#wczytanie z plików za pomocą argparse
parser = argparse.ArgumentParser()

#-a seq1.txt -b seq2.txt -c config.txt -o output.txt
parser.add_argument("-a", "--seq1", help="Sekwencja nr 1")
parser.add_argument("-b", "--seq2", help="Sekwencja nr 2")
parser.add_argument("-c", "--config", help="Plik konfiguracyjny")
parser.add_argument("-o", "--output", help="Plik wyjsciowy")
args = parser.parse_args()

#wczytuje konfiguracje
print('Wczytuje konfiguracje')
config = {}
with open("config.txt", "r") as conf_file:
    for line in conf_file:
        name, val = line.split("=")
        #sprawdzam nazwy paramerow
        if name.strip() not in ['GAP_PENALTY','SAME','DIFF','MAX_SEQ_LENGTH','MAX_NUMBER_PATHS']:
            raise Exception(name +' is wrong name, it shoud name one of :[GAP_PENALTY, SAME, DIFF, MAX_SEQ_LENGTH, MAX_NUMBER_PATHS]')
        #Rzutuje na int'a, jeżeli będzie float, wurzuci błąd
        config[name.strip()] = int(val.replace("\n", "").strip())

#wczytaj sekwencje z plikow
print('Wczytuje sekwencje')
seq1 = fa.read_fasta_file(args.seq1,config['MAX_SEQ_LENGTH'])
seq2 = fa.read_fasta_file(args.seq2,config['MAX_SEQ_LENGTH'] )


#Algorytm needleman-wunsch
print('Tworze macierz zapisuje przejscia')
matrix, graph = fa.create_matrix_and_graph(seq1,seq2, config['GAP_PENALTY'], config['SAME'], config['DIFF'])
print("Wczytuje "+str(config['MAX_NUMBER_PATHS'])+" mozliwych sciezek")
my_paths = fa.paths_in_graph(graph, len(seq2), len(seq1), config['MAX_NUMBER_PATHS'])
my_order_paths = fa.change_str_to_int(my_paths)
print("Zapisuje do pliku")
fa.modifications_to_file(my_order_paths, seq1, seq2, args.output, matrix)


