from z3 import *

prev_model = []
# -- Inicializa matriz de arrays (9x9 matriz com cada entry um array de 9 numeros)
#Prop = [[[Bool(f'p_{i}_{j}_{k}') for k in range(1,10)] for j in range(9)] for i in range(9)]
#s = Solver()


def restrs_usuais(P):
    s = Solver()
    l = len(P)
    #   Inicializa matriz de arrays (9x9 matriz com cada entry sendo um array
    #   de 9 números):
    Prop = [[[Bool(f'p_{i}_{j}_{k}') for k in range(1,l+1)]
                                     for j in range(l)]
                                     for i in range(l)]

    # -- Adiciona como condicoes os numeros ja presentes no tabuleiro
    for i in range(l):
        for j in range(l):
            if(P[i][j]!=0):
                s.add(Prop[i][j][ P[i][j]-1 ])


    # -- Adiciona restricoes do modelo anterior
        if(len(prev_model)>0):
            s.add(Or([Not(p) for p in prev_model]))


    # === CONDICOES === #

    # -- Pelo menos um numero em cada célula
    for i in range(l):
        for j in range(l):
            s.add(Or(Prop[i][j]))
            #Prop[i][j] = [p_i_j_1, p_i_j_2, ..., p_i_j_9]
            #                      <-->
            #              p_i_j_1 V p_i_j_2 V ...

    # -- No maximo um numero em cada celula
    for i in range(l):
        for j in range(l):
            for k in range(l-1):
                for m in range(k+1, l):
                    s.add(Or( Not(Prop[i][j][k]), Not(Prop[i][j][m]) ))
                    #~(p_i_j_k and p_i_j_l) , k =/= l


    # -- Um e um so dado numero por linha/coluna (numeros nao se repetem)
    c=0 #---> guarda o indice de coluna mais a esquerda de cada regiao
    for i in range(l):
        for k in range(l):
            c=0
            for j in range(l):
                if(j%3 == 0 and j!=0 ):
                    c += 3
                for m in range(j+1, l):
                    s.add(Or( Not(Prop[i][j][k]), Not(Prop[i][m][k]) ))
                    # Linha     ~(p_i_j_k and p_i_j_k+n)
                    s.add(Or( Not(Prop[j][i][k]), Not(Prop[m][i][k]) ))
                    # coluna    ~(p_j_i_k and p_j_i_k+n)

                for n in range(i+1, i+(2-i%3)+1):     # por cada linha abaixo
                # da atual dentro da regiao (+1 por causa do range do python)
                    for p in range(c, c+3):
                        if(p!= j):          # escusa de adicionar condicoes aos
                            # elementos da mesma coluna pois fe-lo antes
                            s.add(Or( Not(Prop[i][j][k]), Not(Prop[n][p][k])))

                # i + (2 - i%3) :  i=0 vai ate i=2,  quando i=1 vai ate i=2, quando i=2 salta pq nao e preciso
                # analogo para qualquer i multiplo de 3

                # Note-se que apenas é preciso adicionar a condição para as linhas inferiores
                # da regiao pois a mesma linha ja foi adicionada, e as linhas superiores foram
                # adicionadas quando se iterou pelos simbolos anteriores e se adicionou as condicoes
                # para a regiao


    # if(s.check()==sat):
    #     print_board(s.model())
    #     return [sat,s.model()]
    # else:
    #    print("unsat")
    #    return [unsat, []]
                            #print([Prop[i][j][k], Prop[n][p][k]])

    return (s, l, Prop)

def sudoku(P):
    (s, l, Prop) = restrs_usuais(P)
    #if(s.check()==sat):
    #    #print(s.model())
    #    print_board(s.model(), P)
    #return
    check = s.check()

    # funciona porque os índices são dígitos
    props = [[p.name()[2], p.name()[4], p.name()[6]]
                for p in model.decls() if model[p]]
    for p in props:
        P[int(p[0])][int(p[1])] = int(p[2]) + 1

    if (check == sat):
       print_board(P)
    else:
       print("unsat")
    return (check, s, l, Prop)


P_sudoku_var_expl = [4,0,0, 7,0,6, 0,0,9,
                     0,0,6, 1,5,9, 4,0,0,
                     1,5,0, 0,8,0, 0,2,6,

                     0,0,7, 0,6,0, 5,0,0,
                     2,0,1, 0,0,0, 8,0,7,
                     0,0,4, 0,3,0, 2,0,0,

                     3,7,0, 0,1,0, 0,4,8,
                     0,0,5, 9,4,8, 3,0,0,
                     9,0,0, 3,0,2, 0,0,5]



# == NOTE: Recebe um argumento "a mais". Se apenas puder receber P então
# 'variantes' pode ser global
def sudoku_var(P, variantes = [1,2]):
    (s, l, Prop) = restrs_usuais(P)

    # Função que garante que as células a deltas de distância específicos não
    # têm deltas de valor prescritos. Por expl., p/ deltas_vals = [0], garante
    # que as células são diferentes.
    def diferentes(deltas_dist, deltas_vals):
        for i in range(l):
            for j in range(l):
                for n in range(1,l+1):
                    # ps -- possibilidades de (i,j) + (delta-i, delta-j)
                    ps = [(i+di, j+dj) for (di,dj) in deltas_dist
                                        if 8 >= i + di >= 0 and
                                           8 >= j + dj >= 0]

                    # Se a célula (i,j) vale n, as que estão a delta de
                    # distância não podem valer o mesmo:
                    s.add(And([Implies(
                        Prop[i][j][n-1],
                        Not(Prop[p[0]][p[1]][m-1]))
                            for p in ps
                            for m in [n + dn for dn in deltas_vals]
                                if 1 <= m <= 9]))

    # Nota: nestas duas primeiras variantes, podemos optimizar as restrições
    #       -- por expl. se a != b, então b!= a -- contudo, estas optimizações
    #       ainda não estão implementadas.

    # Células a passo-de-cavalo têm de ser diferentes
    if 1 in variantes:
        diferentes([(1,  2), ( 1,-2), ( 2, 1), ( 2,-1),
                    (-1,-2), (-1, 2), (-2,-1), (-2, 1)]
                  ,[0])

    # Células a passo-de-rei têm de ser diferentes
    if 2 in variantes:
        diferentes([(-1,  0), ( 0, 1), ( 1,-1), ( 1, 1),
                    ( 1,  0), ( 0,-1), (-1, 1), (-1,-1)]
                  ,[0])

    # Células ortogonalmente adjacentes não podem ter números adjacentes
    if 3 in variantes:
        diferentes([(-1,0), (0,1), (1,0), (-1,0)]
                  ,[-1,+1])
    if(s.check()==sat):
        print_board(s.model())
    else:
        print("unsat")
    return



def well_posed(P):
    global prev_model
    prev_model=[]
    # Corre sudoku(P) sem restricoes de modelo anterior
    (check, s, l, Prop) = sudoku(P)
    if(check == unsat):
        return

    model = s.model()
    prev_model = [Prop[ int(p.name()[2]) ][ int(p.name()[4]) ][ int(p.name()[6])-1 ] for p in model.decls() if model[p]]
    #Se o sudoku e unsat entao nao tem mais solucoes
    #(s, l, Prop) = sudoku(P)
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
    for i in range(len(board)):
        for j in range(len(board)):
            print(board[i][j], end=" ")
        print("")
    print("\n\n")
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

    P3 = [[0,0,0,0,0,0,4,0,0],
          [0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,3],
          [0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0]]
    pat1 = [[0,0,1,0,0,0,1,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,1,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,1,0,0,0,0,0,0],
            [0,0,0,0,0,0,1,0,0],
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

    # sudoku(P1)
    # sudoku(P2)
    # well_posed(P1)
    # well_posed(P2)
    # (check1, s1, l1, Prop1) = sudoku(P1)
    # (check2, s2, l2, Prop2) = sudoku(P2)
    #
    # if(check1 == sat):
    #      model = s1.model()
    #      generate(solution_board(model), pat1)
    #
    # if(check2 == sat):
    #      model = s2.model()
    #      generate(solution_board(model), pat1)
    #
    # sudoku(P1)
    # sudoku(P2)
    # well_posed(P1)
    # well_posed(P2)
    #sudoku(P1)
    sudoku_var(P2,[1,2,3])

    #P = P_expl
    #Prop = [[[Bool(f'p_{i}_{j}_{k}') for k in range(l)]
    #                                 for j in range(l)]
    #                                 for i in range(l)]
    #print(Prop)
    #print(Prop[0][0][2])

    #print_board(P)
    # for i in range(len(P)):
    #     for j in range(len(P)):
    #         print(P[i][j], end=" ")
    #     print("")
    # sudoku(P)

    return

if __name__ == '__main__':
    main()
