from z3 import *

P_expl = [[5,3,0,0,7,0,0,0,0],
          [6,0,0,1,9,5,0,0,0],
          [0,9,8,0,0,0,0,6,0],
          [8,0,0,0,6,0,0,0,3],
          [4,0,0,8,0,3,0,0,1],
          [7,0,0,0,2,0,0,0,6],
          [0,6,0,0,0,0,2,8,0],
          [0,0,0,4,1,9,0,0,5],
          [0,0,0,0,8,0,0,7,9]]

def restrs_usuais(P):
    s = Solver()
    l = len(P)
    #   Inicializa matriz de arrays (9x9 matriz com cada entry sendo um array
    #   de 9 números):
    Prop = [[[Bool(f'p_{i}_{j}_{k}') for k in range(l)]
                                     for j in range(l)]
                                     for i in range(l)]

    for i in range(l):
        for j in range(l):
            if(P[i][j]!=0):
                s.add(Prop[i][j][ P[i][j]-1 ])

    # === Conditions === #

    # -- Pelo menos um numero em cada célula
    for i in range(l):
        for j in range(l):
            s.add(Or(Prop[i][j]))
            #Prop[i][j] = [p_i_j_1, p_i_j_2, ..., p_i_j_9]
            #                      <-->
            #              p_i_j_1 V p_i_j_2 V ...

    # -- No maximo um numero em cada celula
    for i in range(l):
        for j in range(l):      #por celula
            for k in range(l-1):
                for m in range(k+1, l):
                    s.add(Or( Not(Prop[i][j][k]), Not(Prop[i][j][m]) ))

    return (s, l, Prop)

def sudoku(P):
    (s, l, Prop) = restrs_usuais(P)
    #if(s.check()==sat):
    #    #print(s.model())
    #    print_board(s.model(), P)
    #return
    check = s.check()

    return unsat if check == unsat else s.model()

P_sudoku_var_expl = [4,0,0, 7,0,6, 0,0,9,
                     0,0,6, 1,5,9, 4,0,0,
                     1,5,0, 0,8,0, 0,2,6,

                     0,0,7, 0,6,0, 5,0,0,
                     2,0,1, 0,0,0, 8,0,7,
                     0,0,4, 0,3,0, 2,0,0,

                     3,7,0, 0,1,0, 0,4,8,
                     0,0,5, 9,4,8, 3,0,0,
                     9,0,0, 3,0,2, 0,0,5]

def sudoku_var(P, variantes):
    (s, l, Prop) = restrs_usuais(P)

    # Função que garante que as células a deltas de distância específicos não
    # têm deltas de valor prescritos. Por expl., p/ deltas_vals = [0], garante
    # que as células são diferentes.
    def diferentes(deltas_dist, deltas_vals):
        for i in range(l):
            for j in range(l):
                for n in range(1,l+1):
                    # ps -- possibilidades de (i,j) + (delta-i, delta-j)
                    ps = [(i+di, j+dj) for (di,dj) in deltas
                                        if 8 >= i + di >= 0 and
                                           8 >= j + dj >= 0]

                    # Se a célula (i,j) vale n, as que estão a delta de
                    # distância não podem valer o mesmo:
                    s.add(And([Implies(
                        Prop[i][j][n-1],
                        Not[Prop[p[0]][p[1]][m-1]])
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
    elif 2 in variantes:
        diferentes([(-1,  0), ( 0, 1), ( 1,-1), ( 1, 1),
                    ( 1,  0), ( 0,-1), (-1, 1), (-1,-1)]
                  ,[0])

    # Células ortogonalmente adjacentes não podem ter números adjacentes
    elif 3 in variantes:
        diferentes([(-1,0), (0,1), (1,0), (-1,0)]
                  ,[-1,+1])

def well_posed(P):
    sol = sudoku(P)
    #tem_sol = sol != unsat

    return sol != unsat and sudoku(And(P, map(Not, sol))) != unsat

# esta implementação altera o valor de S, mas não deve haver problema
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
        raise ValueError("Remover o padrão do puzzle pedido não resulta num problema bem-posto.")

def print_board(model, P):
    props = [[p.name()[2], p.name()[4], p.name()[6]] for p in model.decls() if model[p]]
    for p in props:
        P[int(p[0])][int(p[1])] = int(p[2])
    print(P)

    #Imprime tabuleiro
    for i in range(len(P)):
        for j in range(len(P)):
            print(P[i][j], end=" ")
        print("")

    print(props)


    print("\n\n\n")
    print(model)


    return


def main():
    Prop = [[[Bool(f'p_{i}_{j}_{k}') for k in range(1,4)] for j in range(3)] for i in range(3)]
    #print(Prop)
    #print(Prop[0][0][2])
    P = [[1, 2, 3], [0, 3, 0], [2, 0, 1]]
    modelo = sudoku(P)

    if modelo != unsat:
        print_board(modelo, P)

    return

if __name__ == '__main__':
    main()
