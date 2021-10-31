from z3 import *


prev_model = []
# -- Inicializa matriz de arrays (9x9 matriz com cada entry um array de 9 numeros)
Prop = [[[Bool(f'p_{i}_{j}_{k}') for k in range(1,10)] for j in range(9)] for i in range(9)]
s = Solver()

def sudoku(P):
    global prev_model
    global Prop
    global s
    l = len(P)
    s.reset()

    # -- Adiciona restricoes do modelo anterior
    if(len(prev_model)>0):
        s.add(Or([Not(p) for p in prev_model]))

    # -- Adiciona como condicoes os numeros ja presentes no tabuleiro
    for i in range(l):
        for j in range(l):
            if(P[i][j]!=0):
                s.add(Prop[i][j][ P[i][j]-1 ])



    # === CONDICOES === #

    # -- Pelo menos um numero em cada célula
    for i in range(l):
        for j in range(l):
            s.add(Or(Prop[i][j]))   #Prop[i][j] = [p_i_j_1, p_i_j_2, ..., p_i_j_9]  <--> p_i_j_1 V p_i_j_2 V ...

    # -- No maximo um numero em cada celula
    for i in range(l):
        for j in range(l):
            for k in range(l-1):
                for m in range(k+1, l):
                    s.add(Or( Not(Prop[i][j][k]), Not(Prop[i][j][m]) ))     #~(p_i_j_k and p_i_j_l) , k =/= l


    # -- Um e um so dado numero por linha/coluna (numeros nao se repetem)
    c=0     # guarda o indice de coluna mais a esquerda de cada regiao
    for i in range(l):
        for k in range(l):
            c=0
            for j in range(l):
                if(j%3 == 0 and j!=0 ):
                    c += 3
                for m in range(j+1, l):
                    s.add(Or( Not(Prop[i][j][k]), Not(Prop[i][m][k]) ))     # Linha     ~(p_i_j_k and p_i_j_k+n)
                    s.add(Or( Not(Prop[j][i][k]), Not(Prop[m][i][k]) ))     # coluna    ~(p_j_i_k and p_j_i_k+n)
                for n in range(i+1, i+(2-i%3)+1):     # por cada linha abaixo da atual dentro da regiao (+1 por causa do range do python)
                    for p in range(c, c+3):
                        if(p!= j):          #escusa de adicionar condicoes aos elementos da mesma coluna pois fe-lo antes
                            s.add(Or( Not(Prop[i][j][k]), Not(Prop[n][p][k])))



    if(s.check()==sat):
        print_board(s.model())
        return [sat,s.model()]
    else:
       print("unsat")
       return [unsat, []]



def well_posed(P):
    global prev_model
    prev_model=[]
    # Corre sudoku(P) sem restricoes de modelo anterior
    result = sudoku(P)
    if(result[0] == unsat):
        return

    model = result[1]
    prev_model = [Prop[ int(p.name()[2]) ][ int(p.name()[4]) ][ int(p.name()[6])-1 ] for p in model.decls() if model[p]]
    #Se o sudoku e unsat entao nao tem mais solucoes
    if(sudoku(P)[0] == unsat):
        print("The sudoku puzzle is well_posed")
        prev_model=[]
        return True

    print("The sudoku puzzle has more than one solution")
    prev_model=[]
    return False


def remove(S, pat):
    l=len(S)
    for i in range(l):
        for j in range(l):
            S[i][j] *= pat[i][j]

    return S



def generate(S, pat):
    if not S:
        return
    P = remove(S, pat)
    print("New P:")
    print(P)
    if well_posed(P):
        return P
    else:
        print("Remover o padrão do puzzle pedido não resulta num problema bem-posto.")
    return



def print_board(model):
    board = [[0 for i in range(9)] for j in range(9)]
    props = [[p.name()[2], p.name()[4], p.name()[6]] for p in model.decls() if model[p]]
    for p in props:
        board[int(p[0])][int(p[1])] = int(p[2])
    #Imprime tabuleiro
    print("\n\n")
    for i in range(len(board)):
        for j in range(len(board)):
            print(board[i][j], end=" ")
        print("")

    return


# Transforma modelo em tabuleiro
def solution_board(model):
    if(len(model)==0):
        return
    P = [[0 for i in range(9)] for j in range(9)]
    values = [[int(p.name()[2]), int(p.name()[4]), int(p.name()[6])] for p in model.decls() if model[p]]
    for v in values:
        P[v[0]][v[1]] = v[2]
    return P



def main():

    P1 = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
         [6, 0, 0, 1, 9, 5, 0, 0, 0],
         [0, 9, 8, 0, 0, 0, 0, 6, 0],
         [8, 0, 0, 0, 6, 0, 0, 0, 3],
         [4, 0, 0, 8, 0, 3, 0, 0, 1],
         [7, 0, 0, 0, 2, 0, 0, 0, 6],
         [0, 6, 0, 0, 0, 0, 2, 8, 0],
         [0, 0, 0, 4, 1, 9, 0, 0, 5],
         [0, 0, 0, 0, 8, 0, 0, 7, 9]]

    P2 = [[0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0]]
    pat1 = [[0,0,1,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0]]
    pat2 = [[0,1,1,1,1,1,1,1,1],
           [0,1,1,1,1,1,1,1,1],
           [1,1,1,1,1,1,1,1,1],
           [0,1,1,1,1,1,1,1,1],
           [0,1,1,1,1,1,1,1,1],
           [1,1,1,1,1,1,1,1,1],
           [0,1,1,1,1,1,1,1,1],
           [0,1,1,1,1,1,1,1,1],
           [0,1,1,1,1,1,1,1,1]]

    result = sudoku(P1)
    if(result[0]==sat):
        model = result[1]
        generate(solution_board(model), pat2)
    sudoku(P1)
    well_posed(P2)
    result = sudoku(P2)
    if(result[0]==sat):
        model = result[1]
        generate(solution_board(model), pat2)
    sudoku(P1)
    sudoku(P2)


    return

if __name__ == '__main__':
    main()
