from z3 import *

# P_expl = [[5,3,0,0,7,0,0,0,0],
#           [6,0,0,1,9,5,0,0,0],
#           [0,9,8,0,0,0,0,6,0],
#           [8,0,0,0,6,0,0,0,3],
#           [4,0,0,8,0,3,0,0,1],
#           [7,0,0,0,2,0,0,0,6],
#           [0,6,0,0,0,0,2,8,0],
#           [0,0,0,4,1,9,0,0,5],
#           [0,0,0,0,8,0,0,7,9]]

def sudoku(P):
    s = Solver()
    l = len(P)
    # -- Inicializa matriz de arrays (9x9 matriz com cada entry um array de 9 numeros)
    Prop = [[[Bool(f'p_{i}_{j}_{k}') for k in range(1,l+1)] for j in range(l)] for i in range(l)]
    #print(Prop)

    # -- Adiciona como condicoes os numeros ja presentes no tabuleiro
    for i in range(l):
        for j in range(l):
            if(P[i][j]!=0):
                s.add(Prop[i][j][ P[i][j]-1 ])

    #print(s)

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
                # if(k==1):
                #     #print([i,j])
                if(j%3 == 0 and j!=0 ):
                    c += 3
                for m in range(j+1, l):
                    s.add(Or( Not(Prop[i][j][k]), Not(Prop[i][m][k]) ))     # Linha     ~(p_i_j_k and p_i_j_k+n)
                    s.add(Or( Not(Prop[j][i][k]), Not(Prop[m][i][k]) ))     # coluna    ~(p_j_i_k and p_j_i_k+n)
                for n in range(i+1, i+(2-i%3)+1):     # por cada linha abaixo da atual dentro da regiao (+1 por causa do range do python)
                    for p in range(c, c+3):
                        if(p!= j):          #escusa de adicionar condicoes aos elementos da mesma coluna pois fe-lo antes
                            s.add(Or( Not(Prop[i][j][k]), Not(Prop[n][p][k])))
                            #print([Prop[i][j][k], Prop[n][p][k]])






    if(s.check()==sat):
       #print(s.model())
       print_board(s.model(), P)
    else:
       print("unsat")
    return
    # check = s.check()
    #
    # return unsat if check == unsat else s.model()



def well_posed(P):
    sol = sudoku(P)
    #tem_sol = sol != unsat

    return sol != unsat and sudoku(And(P, map(Not, sol))) != unsat



#esta implementação altera o valor de S, mas não deve haver problema
def remove(S, pat):
    idxs = range(len(S))
    for i in idxs:
        for j in idxs:
            if pat[i][j] == 1:
                S[i][j] = 0
    return S



def generate(S, pat):
    P = remove(S, pat)
    if well_posed(P):
        return P
    else:
        print("Remover o padrão do puzzle pedido não resulta num problema bem-posto.")



def print_board(model, P):
    props = [[p.name()[2], p.name()[4], p.name()[6]] for p in model.decls() if model[p]]
    for p in props:
        P[int(p[0])][int(p[1])] = int(p[2])
    #print(P)
    print("\n\n")
    #Imprime tabuleiro
    for i in range(len(P)):
        for j in range(len(P)):
            print(P[i][j], end=" ")
        print("")

    #print(props)


    #print("\n\n\n")
    #print(model)


    return


def main():
    Prop = [[[Bool(f'p_{i}_{j}_{k}') for k in range(1,4)] for j in range(3)] for i in range(3)]
    #print(Prop)
    #print(Prop[0][0][2])
    P = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
         [6, 0, 0, 1, 9, 5, 0, 0, 0],
         [0, 9, 8, 0, 0, 0, 0, 6, 0],
         [8, 0, 0, 0, 6, 0, 0, 0, 3],
         [4, 0, 0, 8, 0, 3, 0, 0, 1],
         [7, 0, 0, 0, 2, 0, 0, 0, 6],
         [0, 6, 0, 0, 0, 0, 2, 8, 0],
         [0, 0, 0, 4, 1, 9, 0, 0, 5],
         [0, 0, 0, 0, 8, 0, 0, 7, 9]]
    #print_board(P)
    for i in range(len(P)):
        for j in range(len(P)):
            print(P[i][j], end=" ")
        print("")
    sudoku(P)



    return



if __name__ == '__main__':
    main()
