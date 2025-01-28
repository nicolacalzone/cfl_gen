from SCFG_tree import ProductionElement
from colorama import Fore, Style


def find_non_empty_cells(table):
    non_empty = []
    for i, layer1 in enumerate(table):
        for j, layer2 in enumerate(layer1):
            for i_prime, layer3 in enumerate(layer2):
                for j_prime, cell in enumerate(layer3):
                    if cell:
                        non_empty.append({
                            "source_span": (i, j),
                            "target_span": (i_prime, j_prime),
                            "symbols": cell
                        })
    return non_empty

def print_parse_table(c, source, target):
    SPAN_COLOR = Fore.CYAN
    SYMBOL_COLOR = Fore.YELLOW
    TEXT_COLOR = Fore.GREEN
    RESET = Style.RESET_ALL

    non_empty = []
    for i in range(len(c)):
        for j in range(len(c[i])):
            for i_prime in range(len(c[i][j])):
                for j_prime in range(len(c[i][j][i_prime])):
                    if c[i][j][i_prime][j_prime]:
                        non_empty.append((
                            (i, j), (i_prime, j_prime),
                            c[i][j][i_prime][j_prime]
                        ))

    non_empty.sort(key=lambda x: ((x[0][1]-x[0][0]), (x[1][1]-x[1][0])))

    print(f"\n{SPAN_COLOR}Parse Table Contents:{RESET}")
    print(f"{TEXT_COLOR}Source: {source}\nTarget: {target}{RESET}\n")
    print(f"{TEXT_COLOR}Source [i-j] = tokens from position i (inclusive) to j (exclusive){RESET}\n" 
          f"{TEXT_COLOR}Target [i'-j'] = tokens from position i' (inclusive) to j' (exclusive){RESET}")
    
    for (i,j), (i_p,j_p), symbols in non_empty:
        src_span = " ".join(source[i:j]) or "∅"
        tgt_span = " ".join(target[i_p:j_p]) or "∅"
        print(
            f"{SPAN_COLOR}Source [{i:2d}-{j:2d}]{RESET}: {TEXT_COLOR}'{src_span:5s}'{RESET} | "
            f"{SPAN_COLOR}Target [{i_p:2d}-{j_p:2d}]{RESET}: {TEXT_COLOR}'{tgt_span:5s}'{RESET} | "
            f"{SYMBOL_COLOR}Symbols: {', '.join(symbols)}{RESET}"
        )


def bitext_parsing(grammar, source, target, non_terminals):
    n = len(source)
    n_prime = len(target)

    DEBUG_COLOR = Fore.RED


    c = [[[[[] for _ in range(n_prime+1)] for _ in range(n+1)] for _ in range(n_prime+1)] for _ in range(n+1)]

    # AXIOMS - BASE CASE
    for i in range(n):
        for i_prime in range(n_prime):
            for lhs, productions in grammar.items():
                for src_rhs, tgt_rhs in productions:
                    if len(src_rhs) == 1 and len(tgt_rhs) == 1:
                        src_elem = src_rhs[0]
                        tgt_elem = tgt_rhs[0]
                        if (not src_elem.isnonterminal() and src_elem.symbol() == source[i]) and \
                           (not tgt_elem.isnonterminal() and tgt_elem.symbol() == target[i_prime]):
                            c[i][i+1][i_prime][i_prime+1].append(lhs)

    print_parse_table(c, source, target)

    # Main CKY loop
    for span in range(1, n + n_prime + 1): 
        for i in range(n + 1): 
            for i_prime in range(n_prime + 1):  
                for i_k in range(span + 1):

                    i_prime_k_prime = span - i_k
                    k = i + i_k
                    k_prime = i_prime + i_prime_k_prime
                    j = k
                    j_prime = k_prime

                    if (k-i+k_prime-i_prime) != span:
                        print(f"{DEBUG_COLOR}ERROR: k-i+k_prime-i_prime != span")
                        continue
                    if i < 0 or i > k or i_prime < 0 or i_prime > k_prime:
                        print(f"{DEBUG_COLOR}ERROR: i, k, i_prime, k_prime out of bounds")
                        continue

                    # Check if [A, i, k, i', k'] can be derived
                    for A in non_terminals:  # Iterate over all non-terminals
                        for (src_rhs, tgt_rhs) in grammar.get(A, []):  # Check all productions of A
                            
                            if len(src_rhs) == 2 and len(tgt_rhs) == 2:
                                B, C = src_rhs[0], src_rhs[1]       # Binary Rule splitting source
                                D, E = tgt_rhs[0], tgt_rhs[1]       # Binary Rule splitting target
                                
                                # Check all possible splits q, q_prime
                                for q in range(i + 1, k + 1):
                                    for q_prime in range(i_prime + 1, k_prime + 1):
                                        # Ensure q and q_prime are within bounds
                                        if q >= len(c) or q_prime >= len(c[0]):
                                            continue
                                        # Check if B spans (i, q) and D spans (i', q_prime)
                                        # Check if C spans (q, k) and E spans (q_prime, k_prime)
                                        if (B.symbol() in c[i][q][i_prime][q_prime] and 
                                            C.symbol() in c[q][k][q_prime][k_prime] and 
                                            D.symbol() in c[i][q][i_prime][q_prime] and 
                                            E.symbol() in c[q][k][q_prime][k_prime]):
                                            # Add A to c[i][k][i_prime][k_prime] (line 9)
                                            if A not in c[i][k][i_prime][k_prime]:
                                                c[i][k][i_prime][k_prime].append(A)
                                            break  # No need to check for other splits

    print_parse_table(c, source, target)

    if "S" in c[0][n][0][n_prime]:
        print("Accepted: The input strings are in the language.")
        print(f"Accepted Parse tree: {c[0][n][0][n_prime]}")
    else:
        print("Rejected: The input strings are not in the language.")
        print(f"Rejected Parse tree: {c[0][n][0][n_prime]}")


# Example usage
grammar = {
"S": [([ProductionElement("A", 1), ProductionElement("B", 2)], 
        [ProductionElement("B", 2), ProductionElement("A", 1)])],      # S -> A{1} B{2} // B{2} A{1}
"A": [
    ([ProductionElement("a", 0)], [ProductionElement("c", 0)]),        # A -> a // c
    ([ProductionElement("A", 1), ProductionElement("B", 2)],           # A -> A{1} B{2} // B{2} A{1}
        [ProductionElement("B", 2), ProductionElement("A", 1)])
],
"B": [([ProductionElement("b", 0)], [ProductionElement("d", 0)])]       # B -> b // d
}

source = "a b b b b".split()
target = "d d d d c".split()

bitext_parsing(grammar, source, target, non_terminals=["S", "A", "B"])