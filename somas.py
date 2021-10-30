from z3 import *

def excepto(R,E):
    R2 = list(R).copy()

    for r in E:
        try:
            R2.remove(r)
        except ValueError:  # ignorar remoção de valores ausentes
            pass

    return R2

def partes(R):
    ps = [partes(excepto(R,[r])) for r in R]
    return [R] + [S for P in ps for S in P]

def sums(R,t):
    s = Solver()
    p = {r: Bool('p_'+str(r)) for r in R}

    #print(partes(R))
    for S in partes(R):
        if sum(S) == t:
            s.add(And([p[r] for r in S]))
            break
        #else:
            #s.add(Not(And([p[r] for r in excepto(R,S)])))

    check = s.check()

    return False if check == unsat else s.model().decls()



def main():
    R = range(1,9)
    t = 30

    S = sums(R,t)

    if S == False:
        print("O problema dado não tem solução.")
    else:
        print(S)

    return

if __name__ == '__main__':
    main()
