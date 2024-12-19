from SCFG_tree import ProductionElement
import torch


def bitext_parsing(grammar, source, target):
    """
        Bitext CKY Algorithm for Synchronous CFGs

        ** Args: ** 
            grammar: A dictionary of grammar rules
            source: Source string (list of tokens)
            target: Target string (list of tokens)
        
        ** Returns: ** 
            Boolean indicating whether the input is accepted
    """

    n = len(source)  # Length of source string
    m = len(target)  # Length of target string

    # Initialize a 5D table c[i][j][i'][j'] to store nonterminal symbols
    c = [[[[[] for _ in range(m+1)] for _ in range(n+1)] for _ in range(m+1)] for _ in range(n+1)]

    # AXIOMS - BASE CASE
    # Fill the table with the terminals.

    # for all i, j, i', j' 
    for i in range(n):
        for i_prime in range(m):

            for lhs, productions in grammar.items():
                #   lhs:         S
                #   productions: [([A, 1, False, B, 2, False], [B, 2, False, A, 1, False])]
                for src_rhs, tgt_rhs in productions:
                    #   src_rhs: [A, 1, False, B, 2, False]
                    #   tgt_rhs: [B, 2, False, A, 1, False]

                    # Single terminal
                    if len(src_rhs) == 1 and len(tgt_rhs) == 1:  
                        if (not src_rhs[0].isnonterminal() and source[i] == src_rhs[0].symbol()) and \
                           (not tgt_rhs[0].isnonterminal() and target[i_prime] == tgt_rhs[0].symbol()):
                            print(f"source: {source[i]}, target: {target[i_prime]}")
                            c[i][i+1][i_prime][i_prime+1].append(lhs)

    #print(c)

    # Main CKY loop
    for span in range(2, n+1):  # Source span length
        for span_prime in range(2, m+1):  # Target span length
            for i in range(n - span + 1):  # Source start
                j = i + span
                for i_prime in range(m - span_prime + 1):  # Target start
                    j_prime = i_prime + span_prime

                    for lhs, productions in grammar.items():
                        for src_rhs, tgt_rhs in productions:
                            if len(src_rhs) == 2 and len(tgt_rhs) == 2:  # Binary productions
                                # Split the spans for both source and target
                                for k in range(i+1, j):  # Source split
                                    for k_prime in range(i_prime+1, j_prime):  # Target split
                                        B, C = src_rhs[0], src_rhs[1]
                                        B_prime, C_prime = tgt_rhs[0], tgt_rhs[1]

                                        if B.symbol() in c[i][k][i_prime][k_prime] and \
                                           C.symbol() in c[k][j][k_prime][j_prime]:
                                            c[i][j][i_prime][j_prime].append(lhs)

    #print(c)

    # Check if the start symbol 'S' spans the entire input strings
    if "S" in c[0][n][0][m]:
        print("Accepted: The input strings are in the language.")
        print(f"Accepted Parse tree: {c[0][n][0][m]}")
    else:
        print("Rejected: The input strings are not in the language.")
        print(f"Rejected Parse tree: {c[0][n][0][m]}")

# Example usage
if __name__ == "__main__":
    # Example Grammar
    grammar = {
        "S": [([ProductionElement("A", 1), ProductionElement("B", 2)], 
               [ProductionElement("B", 2), ProductionElement("A", 1)])],

        "A": [
            ([ProductionElement("a", 0)], [ProductionElement("c", 0)]),
            ([ProductionElement("A", 1), ProductionElement("B", 2)],
              [ProductionElement("B", 2), ProductionElement("A", 1)])
        ],

        "B": [([ProductionElement("b", 0)], [ProductionElement("d", 0)])]
    }

    # Example input strings
    source = "a b b b".split()
    target = "d d d c".split()

    bitext_parsing(grammar, source, target)
