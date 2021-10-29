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

def sudoku(P):
    s = Solver()
    s.add(...)
    check = s.check()

    return unsat if check == unsat else s.model()

def well_posed(P):
    sol = sudoku(P)
    #tem_sol = sol != unsat

    return sol != unsat and sudoku(And(P, map(Not, sol))) != unsat

# esta implementação altera o valor de S, mas não deve haver problema
def remove(S, pat):
    idxs = range(len(S))
    for i in idxs:
        for j in idxs:
            if pat[i][j] == 1
                S[i][j] = 0
    return S

def generate(S, pat):
    P = remove(S, pat)
    return P if well_posed(P)
             else error "Remover o padrão do puzzle pedido não resulta num problema bem-posto."
