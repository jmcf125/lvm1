def well_posed(P):
    return sudoku(P) and sudoku(P and not sudoku(P))
