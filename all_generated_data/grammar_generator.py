import random
from nltk.grammar import CFG, Nonterminal, Production

def generate_non_terminals(num_non_terminals):
    """Generate a list of non-terminals as strings 'nt1', 'nt2', ..., 'ntN'."""
    return [Nonterminal(f'nt{i}') for i in range(1, num_non_terminals + 1)]

def random_symbol(terminals, non_terminals):
    """Select a random terminal or non-terminal."""
    #rand = random.randint(1, 100)
    #if rand > 80:
    return random.choice(terminals + non_terminals)


def random_rule(terminals, non_terminals, max_symbols=10):
    """Generate a random rule with a random number of symbols (terminals or non-terminals)."""
    num_symbols = random.randint(1, max_symbols)
    return [random_symbol(terminals, non_terminals) for _ in range(num_symbols)]

def random_production_set(non_terminal, terminals, non_terminals):
    """Generate a set of random productions for a non-terminal."""
    rules = []
    for _ in range(random.randint(1, 10)):  # Random number of production rules
        rule = random_rule(terminals, non_terminals)
        rules.append(Production(non_terminal, rule))
    return rules
    

def generate_productions(non_terminals, terminals):
    """Generate random productions for all non-terminals."""
    productions = []
    for nt in non_terminals:
        productions += random_production_set(nt, terminals, non_terminals)
    return productions

def generate_grammar(terminals, num_non_terminals):
    """Generate a random grammar."""
    non_terminals = generate_non_terminals(num_non_terminals)
    productions = generate_productions(non_terminals, terminals)
    return CFG(non_terminals[0], productions)



##########################################################################################################
##                                          MAIN
##########################################################################################################

terminals = ['a', 'b', 'c']
num_non_terminals = 2

random_cfg = generate_grammar(terminals, num_non_terminals)
print(random_cfg)
