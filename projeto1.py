from z3 import *

def sudoku(P):
    s = Solver()
    l = len(P)
    #   Inicializa matriz de arrays (9x9 matriz com cada entry sendo um array de 9 numeros)
    Prop = [[[Bool('p_{i}_{j}_{k}'.format(i=i,j=j,k=k+1)) for k in range(l)] for j in range(l)] for i in range(l)]
    #print(Prop)
    for i in range(l):
        for j in range(l):
            if(P[i][j]!=0):
                s.add(Prop[i][j][ P[i][j]-1 ])

    #print(s)

    # === Conditions === #

    # -- Pelo menos um numero em cada culula
    for i in range(l):
        for j in range(l):
            s.add(Or(Prop[i][j]))   #Prop[i][j] = [p_i_j_1, p_i_j_2, ..., p_i_j_9]  <--> p_i_j_1 V p_i_j_2 V ...

    # -- No maximo um numero em cada celula
    for i in range(l):
        for j in range(l):      #por celula
            for k in range(l-1):
                for m in range(k+1, l):
                    s.add(Or( Not(Prop[i][j][k]), Not(Prop[i][j][m]) ))


    if(s.check()==sat):
        #print(s.model())
        print_board(s.model(), P)
    return



def well_posed(P):
    return



def generate(S, pat):
    return



def print_board(model, P):
    props = [[p.name()[2], p.name()[4], p.name()[6]] for p in model.decls() if model[p]]
    for p in props:
        P[int(p[0])][int(p[1])] = int(p[2])
    print(P)
    for i in range(len(P)):
        for j in range(len(P)):
            print(P[i][j]),
        print("")

    #print(props)


    print("\n\n\n")
    print(model)


    return


def main():
    Prop = [[[Bool('p_{i}_{j}_{k}'.format(i=i+1,j=j+1,k=k+1)) for k in range(3)] for j in range(3)] for i in range(3)]
    #print(Prop)
    #print(Prop[0][0][2])
    P = [[0, 1, 0], [1, 3, 2], [0, 0, 1]]
    sudoku(P)



    return



if __name__ == '__main__':
    main()
