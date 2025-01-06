from include.SCFG_tree import TreeSynCFG
from include.cyk_SCFG_map_reduce import parse_with_mapreduce
from nltk.grammar import Nonterminal
from collections import Counter
import logging as log
import random as rand
import pandas as pd
from collections import defaultdict
from metrics.metrics import main

"""
    MAIN TO TEST THE PARSER
"""


pd.set_option('future.no_silent_downcasting', True)
log.basicConfig(filename='logs/app.log', 
                    filemode='a',
                    level=log.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
    
g = """
S -> A{1} B{2} // B{2} A{1}

A -> A{1} B{2} // A{1} B{2}
A -> C{1} F{2} // C{1} F{2}

B -> B{1} F{2} // F{2} B{1}
B -> D{1} A{2} // D{1} A{2}

C -> C{1} D{2} // D{2} C{1}
C -> F{1} B{2} // B{2} F{1}

D -> F{1} A{2} // F{1} A{2}
D -> D{1} C{2} // D{1} C{2}

E -> E{1} D{2} // D{2} E{1}
E -> B{1} F{2} // B{1} F{2}

F -> D{1} B{2} // B{2} D{1}
F -> F{1} C{2} // C{2} F{1}

A -> a // e
A -> b // f
A -> a // g

B -> b // f
B -> a // e

C -> c // g
C -> d // h

D -> d // h
D -> c // g

E -> d // h
E -> c // g

F -> c // g
F -> a // e
"""


g1 = """
S -> A{1} B{2} // B{2} A{1}
A -> A{1} B{2} // B{2} A{1}
B -> b // d
A -> a // c
"""

sync_cfg = TreeSynCFG.fromstring(g1)
translated_grammar = sync_cfg.translate_grammar_for_parser()

#print(translated_grammar)

non_terminals = set()
for key, values in translated_grammar.items():
    non_terminals.add(key)
        
non_terminals = list(non_terminals)
ws = "a b b b b".split()
wt = "d d d d c".split()
print(f"ws: {ws}, wt: {wt}\nnon_terminals: {non_terminals}\n")

for lhs in translated_grammar:
    for rhs in translated_grammar[lhs]:
        print(lhs, rhs)

print("\n\n")
isaccepted = parse_with_mapreduce(translated_grammar, ws, wt)
print(isaccepted)