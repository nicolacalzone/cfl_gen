from include.SCFG_tree import TreeSynCFG
from include.cyk import CYK
from nltk.grammar import Nonterminal
from collections import Counter
import logging as log
import random as rand
import pandas as pd
from collections import defaultdict
from metrics.metrics import main


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


sync_cfg = TreeSynCFG.fromstring(g)
rules = sync_cfg.translate_grammar_for_parser()

for key, values in rules.items():
    for value in values:
        print(key, "->", value)

non_terminals = ["S", "A", "B", "C", "D", "E", "F"]
source_terminals = ["a", "b", "c", "d"]
target_terminals = ["e", "f", "g", "h"]

# Given string
w = "a very heavy orange book".split()

cyk = CYK(non_terminals, source_terminals, target_terminals, rules)
cyk.cykParse(w)