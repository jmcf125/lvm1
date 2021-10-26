from z3 import *

def sudoku(P):
    s = Solver()
    s.add(...)
    s.check()

    return unsat if s

def well_posed(P):
    sol = sudoku(P)
    tem_sol = sol != unsat
    return sol != unsat and sudoku(P and not sudoku(P))
