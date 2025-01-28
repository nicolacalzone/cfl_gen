from SCFG_tree import TreeSynCFG, ProductionElement
import logging as log
import random as rand
import pandas as pd
from parser import SynchronousCFGParser

"""
    MAIN TO TEST THE PARSER
"""

pd.set_option('future.no_silent_downcasting', True)
log.basicConfig(filename='logs/parser_test.log', 
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

sync_cfg = TreeSynCFG.fromstring(g)
translated_grammar = sync_cfg.translate_grammar_for_parser()
parser = SynchronousCFGParser(translated_grammar)

#ws = "aacccccca"
#wt_false = "ggfggeeeg"
#wt_true = "gggggggeg"
#result1 = parser.parse(ws, wt_false)  # False
#result2 = parser.parse(ws, wt_true)  # True
#print(result1, result2)
