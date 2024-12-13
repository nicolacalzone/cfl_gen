# Python implementation for the
# CYK Algorithm

class CYK:
    def __init__(self, non_terminals, source_terminals, target_terminals, translated_grammar):
        self._non_terminals = non_terminals
        self._translated_grammar = translated_grammar
        self._source_terminals = source_terminals
        self._target_terminals = target_terminals
    
    def cyk_scfg(self, w_source, w_target):
        for rule in self._translated_grammar:
            for value in self._translated_grammar[rule]:
                #print(rule, value)
                continue

        n_src = len(w_source) # Length of the source sentence
        n_tgt = len(w_target) # Length of the target sentence

        # Initialize CYK tables
        table_src = [[set() for _ in range(n_src)] for _ in range(n_src)]
        table_tgt = [[set() for _ in range(n_tgt)] for _ in range(n_tgt)]
        
        link_table = [[set() for _ in range(n_src)] for _ in range(n_src)]

        # Fill the CYK tables

        # First level of the CYK tables
        for i in range(n_src):
            for rule in self._translated_grammar:

                # *** Base cases ***
                # Axioms for Source
                if any(elem.symbol() == w_source[i] for value in self._translated_grammar[rule] for elem in value[0]):
                    print("1st if ", i, rule)
                    table_src[i][i].add(rule)
                # Axioms for Target
                if any(elem.symbol() == w_target[i] for value in self._translated_grammar[rule] for elem in value[1]):
                    print("2nd if ", i, rule)
                    table_tgt[i][i].add(rule)

        # Create links between same symbols in both tables
        for i in range(n_src):
            for j in range(n_tgt):
                for rule in table_src[i][i]:
                    if rule in table_tgt[j][j]:
                        link = (rule, (i, i+1), (j, j+1))
                        link_table[i][i].add(link)

        
        print("\nSource table:")
        for row in table_src:
            print(row)

        print("\nTarget table:")
        for row in table_tgt:
            print(row)
        
        print("\nLink table:")
        for row in link_table:
            print(row)


