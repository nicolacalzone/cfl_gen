# Python implementation for the
# CYK Algorithm

class CYK:
    def __init__(self, non_terminals, source_terminals, target_terminals, rules):
        self._non_terminals = non_terminals
        self._rules = rules
        self._source_terminals = source_terminals
        self._target_terminals = target_terminals

    def cykParse(self, w):
        n = len(w)
        
        # Initialize the table
        T = [[set([]) for j in range(n)] for i in range(n)]

        # Filling in the table
        for j in range(0, n):
            for lhs, rule in self._rules.items():
                for rhs in rule:
                    if len(rhs) == 1 and rhs[0] == w[j]:
                        T[j][j].add(lhs)

            for i in range(j, -1, -1): 
                for k in range(i, j + 1):	 
                    for lhs, rule in self._rules.items():
                        for rhs in rule:
                            if len(rhs) == 2 and rhs[0] in T[i][k] and rhs[1] in T[k + 1][j]:
                                T[i][j].add(lhs)

        if len(T[0][n-1]) != 0:
            print("True")
        else:
            print("False")


