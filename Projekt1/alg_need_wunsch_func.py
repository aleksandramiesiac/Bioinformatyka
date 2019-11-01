import networkx as nx 

def read_fasta_file(filename, max_seq_length):
    seq=''
    with open(filename, "r") as conf_file:
        for idx, line in enumerate(conf_file):
            if idx==0:
                continue
            seq = seq.join(line.replace("\n", ""))
            #sprawdzam warunek na długośc sekwencji
            if len(seq)>= max_seq_length:
                print('Too long sequence, sequence will be cut.')
                seq = seq[:max_seq_length]
                break
    return seq


def create_matrix_and_graph(seq1,seq2, gp, same,diff):
    n = len(seq1)
    m = len(seq2)
    matrix = [[0]*(n+1) for i in range(m+1)]
#     stworz graf
    DG = nx.DiGraph()
    for i in range(n+1):
        for j in range(m+1):
            DG.add_node(str(j)+','+str(i))
            
#     wypełnij wartości macierzy i dodaj odpowiednie krawędzie w grafie
    for j in range(1,m+1):
        matrix[j][0]=matrix[j-1][0]+gp
        DG.add_edge(str(j)+',0',str(j-1)+',0')
        for i in range(1,n+1):
            matrix[0][i]=matrix[0][i-1]+gp
            DG.add_edge('0,'+str(i),'0,'+str(i-1))
            
            val1 = matrix[j-1][i]+gp
            val2 = matrix[j][i-1]+gp
            if seq1[i-1] == seq2[j-1]:
                val3 = matrix[j-1][i-1]+same
            else:
                val3 = matrix[j-1][i-1]+diff
            #oblicz max z trzech wartości
            val_max = max([val1,val2,val3])
            #przepisz max'a i dodaj krawedz odpowiednia
            matrix[j][i] = val_max
            if val1 == val_max:
                DG.add_edge(str(j)+','+str(i), str(j-1)+','+str(i))
            if val2 == val_max:
                DG.add_edge(str(j)+','+str(i), str(j)+','+str(i-1))
            if val3 == val_max: 
                DG.add_edge(str(j)+','+str(i), str(j-1)+','+str(i-1))
    return matrix, DG

def paths_in_graph(DG,m,n,max_number_paths):
    x = []
    #znajdz mozliwe sciezki w grafie zczytaj je
    for num, i in enumerate(nx.all_simple_paths(DG,str(m)+','+str(n),'0,0')):
        if num == max_number_paths:
            break
        x.append([])
        for j in i:
            x[num].append(j.split(','))
    return x

def change_str_to_int(x):
    #zamien liste strigow na wektory
    for idx_x, lists in enumerate(x):
        for idx_lists, node in enumerate(lists):
            for idx_node, number in enumerate(node):
                x[idx_x][idx_lists][idx_node] = int(number)
        x[idx_x] = x[idx_x][::-1]
    return x

def modifications_to_file(paths, seq1, seq2, filename, matrix):
    file = open(filename,'w')
    #oblicz score modyfikacji
    sums=0
    for idx in paths[0]:
        sums+=matrix[idx[0]][idx[1]]   
    file.write('SCORE = '+str(sums)+'\n\n')
    #przepisz modefikacje do pliku
    for path in paths:
        line1, line2 = modification(path, seq1, seq2)
        file.write(line1+'\n')
        file.write(line2+'\n')
        file.write("\n")
    file.close()
        
def modification(path, seq1, seq2):
    line1 = ""
    line2 = ""
    for idx_node, node in enumerate(path[1:],1):
        if sum(path[idx_node-1])+2==sum(path[idx_node]):
            #wtedy obie są dobre
            line1+=seq1[path[idx_node-1][1]]
            line2+=seq2[path[idx_node-1][0]]
        elif path[idx_node-1][0]==path[idx_node][0]:
            #wtedy w drugim seq jest gap
            line1+=seq1[path[idx_node-1][1]]
            line2+='-'
        else:
            line1+='-'
            line2+=seq2[path[idx_node-1][0]]
    return line1, line2