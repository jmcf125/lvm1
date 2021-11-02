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

# Somas com uma redução exponencial para SAT
def sums_red_exp(R,t):
    s = Solver()
    p = {r: Bool('p_'+str(r)) for r in R}
    ok = False

    #print(partes(R))
    for S in partes(R):
        if sum(S) == t:
            s.add(And([p[r] for r in S]))
            ok = True
            break
        #else:
            #s.add(Not(And([p[r] for r in excepto(R,S)])))
    
    if not ok:
        s.add(And([And(p[r], Not(p[r])) for r in R]))
    
    check = s.check()

    return False if check == unsat else s.model().decls()


# Esta é que é a redução polinomial de SUM para SAT
def sums(R,t):
    s = Solver()
    # p_u_r significa que o último símbolo adicionado foi u para faltar r para
    # a soma atingir t (i.e. a soma atual está em t - r)
    p = {u: [Bool('p_'+str(u)+'_'+str(r)) for r in range(t+1)] for u in R}

    # Se o último aparece numa posição, não aparece em nenhuma outra.
    # Isto é, os últimos são únicos.
    for u in R:
     for r in range(t+1):
      for w in range(t+1):
        if r != w:
            s.add(Implies(p[u][r], Not(p[u][w])))

    # Tem de haver algum último número que difira em 0 de t.
    # Ou seja, atingimos t com algum último número.
    s.add(Or([p[u][0] for u in R]))

    # Queremos exatamente uma maneira de somar para chegar a um qualquer resto r
    # Pode-se ver isto como cortando todos os galhos excepto um na árvore de
    # procura por somas que dão r.
    for u in R:
     for w in R:
      if u != w:
       for r in range(t+1):
        s.add(Implies(p[u][r], Not(p[w][r])))

    # Precisamos de uma condição para encadear as coisas a partir de p_u_0:
    # para cada par (último,resto) deve haver exatamente um antecessor
    # (isto já é possìvelmente consequência das conds. anteriores)
    for r in range(t+1):
     for u in R:
      if r + u <= t:
        #p[r][0] => existe u t.q. p[u][r]
        # no geral:
        # cada (u,r) veio de algum (w,r+u):
        s.add(Implies(p[u][r], Or([p[w][r+u] for w in R])))
        # cada (u,r), vindo de (w,r+u), não veio de (v,r+u) para v != w:
        for w in R:
         s.add(Implies(p[u][r], And([
             Implies(p[w][r+u], Not(p[v][r+u]))
             for v in R if v != w])))

    check = s.check()

    return False if check == unsat else s.model().decls()


def main():
    #R = range(1,9)
    #t = 30

    R = range(5)
    t = 10

    S = sums(R,t)

    if S == False:
        print("O problema dado não tem solução.")
    else:
        print(S)

    return

if __name__ == '__main__':
    main()
