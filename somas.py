from z3 import *

def excepto(R,E):
    R2 = list(R).copy()

    for r in E:
        try:
            R2.remove(r)
        except ValueError:  # ignorar remoção de valores ausentes
            pass

    return R2

#Cria powerset do set inicial
def partes(R):
    ps = [partes(excepto(R,[r])) for r in R]
    return [R] + [S for P in ps for S in P]

# Somas com uma redução exponencial para SAT
def sums_red_exp(R,t):
    s = Solver()
    p = {r: Bool('p_'+str(r)) for r in R}
    ok = False

    print(partes(R))
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
    R = [r for r in R if r != 0]
    s = Solver()
    # p_u_r significa que o último símbolo adicionado foi u para faltar r para
    # a soma atingir t (i.e. a soma atual está em t - r)
    p = {u: [Bool('p_'+str(u)+'_'+str(r)) for r in range(t+1)] for u in R}

    # Se o último aparece numa posição, não aparece em nenhuma outra.
    # Isto é, os últimos são únicos.
    for u in R:             # u de último (em R)
     for r in range(t+1):   # r de resto (em [0,t], não nec. em R)
      for w in range(t+1):
        if r != w:
         s.add(Implies(p[u][r], Not(p[u][w])))

    # Começamos em alguma coisa (já que não podemos ter p_0_t)
    s.add(Or([p[u][t-u] for u in R if u in range(t+1)]))

    # Não podemos exceder t (mas isto chega?)
    for u in R:
     for r in range(t+1):
      if u + r > t:
        s.add(Not(p[u][r]))

    # Tem de haver algum último número que difira em 0 de t.
    # Ou seja, atingimos t com algum último número.
    s.add(Or([p[u][0] for u in R]))

    # Queremos exatamente uma maneira de somar para chegar a um qualquer resto r
    # Pode-se ver isto como cortando todos os galhos excepto um na árvore de
    # procura por somas que dão r.
    # (até podemos querer isto, mas não corresponde ao código)
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
      if r + u <= t and r != 0:
      # justificar isto!
      #if r - u > 0: # hmm...
         #if r + u <= t:# and r != 0:
        #p[r][0] => existe u t.q. p[u][r]
        # no geral:
        # cada (u,r) veio de algum (w,r+u):
        # (pois esta não pode dar, u não inclui o valor de r)
        #s.add(Implies(p[u][r], Or([p[w][r+u] for w in R])))
        s.add(Implies(p[u][r],
            Or([p[w][r-w] for w in R
                          if r-w in range(t+1)])))
        #s.add(Implies(Or([p[w][r+u] for w in R]), p[u][r]))
        # cada (u,r), vindo de (w,r+u), não veio de (v,r+u) para v != w:
        # (isto parece desnecessário)
        #for w in R:
         #s.add(Implies(p[u][r], And([
             ##Implies(p[w][r+u], Not(p[v][r+u]))
             #for v in R if v != w])))
        # cada (u,r) vai para um (w,r-w):
        # (isto não dá o mesmo do que a restr. acima?)
        #s.add(Implies(p[u][r], Or([p[w][r-w] for w in R])))

    check = s.check()

    print(s)

    def S():
        props = [q for q in s.model().decls() if s.model()[q]]
        print(props)
        # isto só funciona p/ u < 10
        return [int(str(prop).split("_")[1]) for prop in props]

    return False if check == unsat else S()


def main():
    R = [2**i for i in range(7)]
    R.append(0)
    t = 74

    S = sums(R,t)

    if S == False:
        print("O problema dado não tem solução.")
    else:
        print(S)
        print(sum(S))

    return

if __name__ == '__main__':
    main()
