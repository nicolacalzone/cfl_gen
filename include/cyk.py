# Python implementation for the
# CYK Algorithm

class CYK:
    def __init__(self, non_terminals, terminals, rules):
        self._non_terminals = non_terminals
        self._rules = rules
        self._terminals = terminals

    def cykParse(self, w):
        n = len(w)
        
        # Initialize the table (triangular) to store Non-Terminals for substrings in input
        # T[i][j] = set of non-terminals that can generate the substring of w,
        #           starting at index i and ending at index j
        T = [[set([]) for j in range(n)] for i in range(n)]

        # Filling in the table
        
        # FOR each word in the input w[j]
        for j in range(0, n):
            for lhs, rule in self._rules.items():
                for rhs in rule:
                    for elem in rhs:
                        print(elem)
                    # If the rule is of the form A -> w[j]
                    if len(rhs) == 1 and rhs[0].symbol() == w[j]:
                        T[j][j].add(lhs)

            for i in range(j, -1, -1): 
                for k in range(i, j + 1):	 
                    for lhs, rule in self._rules.items():
                        for rhs in rule:
                            print(rhs[0])
                            if len(rhs) == 2 and rhs[0].symbol() in T[i][k] and rhs[1].symbol() in T[k + 1][j]:
                                T[i][j].add(lhs)

        if len(T[0][n-1]) != 0:
            print("True")
        else:
            print("False")


