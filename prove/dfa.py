from collections import defaultdict
from include.SCFG_tree import TreeSynCFG


class DFA:
    def __init__(self, states, start_state, accept_states, transitions):
        self.states = states
        self.start_state = start_state
        self.accept_states = accept_states
        self.transitions = transitions

    def __repr__(self):
        return f"DFA(start_state={self.start_state}, accept_states={self.accept_states}, transitions={self.transitions})"

def build_dfa_from_treesyncfg(cfg):
    # Convert productions into a dictionary format
    grammar = defaultdict(list)

    for source_elements, target_elements in cfg.list_productions():
        source_rhs = [
            (e.symbol(), e.index()) for e in source_elements
        ]
        target_rhs = [
            (e.symbol(), e.index()) for e in target_elements
        ]
        grammar[source_elements[0].symbol()].append((source_rhs, target_rhs))

    # Store constructed DFAs
    dfa_definitions = {}

    def build_dfa(nonterminal, grammar, memo={}):
        if nonterminal in memo:
            return memo[nonterminal]

        rules = grammar.get(nonterminal, [])
        dfa_list = []

        for source_rule, _ in rules:  # Only process source for DFA creation
            current_dfa = None
            for symbol, index in source_rule:
                if isinstance(symbol, str) and not symbol.isupper():
                    # Terminal symbol
                    terminal_dfa = create_terminal_dfa(symbol)
                    current_dfa = concatenate_dfa(current_dfa, terminal_dfa)
                elif isinstance(symbol, str):
                    # Nonterminal symbol
                    sub_dfa = build_dfa(symbol, grammar, memo)
                    current_dfa = concatenate_dfa(current_dfa, sub_dfa)
            dfa_list.append(current_dfa)

        # Combine all rules into a single DFA using union
        final_dfa = union_dfa_list(dfa_list)
        memo[nonterminal] = final_dfa
        return final_dfa

    def create_terminal_dfa(symbol):
        # Create a simple DFA for a terminal
        start_state = f"{symbol}_start"
        accept_state = f"{symbol}_accept"
        transitions = {start_state: {symbol: accept_state}}
        return DFA(
            states={start_state, accept_state},
            start_state=start_state,
            accept_states={accept_state},
            transitions=transitions
        )

    def concatenate_dfa(dfa1, dfa2):
        if dfa1 is None:
            return dfa2
        # Concatenate two DFAs
        new_states = dfa1.states | dfa2.states
        new_transitions = {**dfa1.transitions}
        for state in dfa1.accept_states:
            new_transitions[state] = {**new_transitions.get(state, {}), **dfa2.transitions[dfa2.start_state]}
        return DFA(
            states=new_states,
            start_state=dfa1.start_state,
            accept_states=dfa2.accept_states,
            transitions=new_transitions
        )

    def union_dfa_list(dfa_list):
        if not dfa_list:
            return None
        if len(dfa_list) == 1:
            return dfa_list[0]
        # Combine multiple DFAs using union
        new_start_state = "union_start"
        new_states = {new_start_state}
        new_transitions = {}
        new_accept_states = set()
        for dfa in dfa_list:
            new_states |= dfa.states
            new_transitions.update(dfa.transitions)
            new_transitions[new_start_state] = {None: dfa.start_state}  # Epsilon transition
            new_accept_states |= dfa.accept_states
        return DFA(
            states=new_states,
            start_state=new_start_state,
            accept_states=new_accept_states,
            transitions=new_transitions
        )

    # Generate DFA for all nonterminals
    for nonterminal in grammar:
        dfa_definitions[nonterminal] = build_dfa(nonterminal, grammar)

    return dfa_definitions


g = """
S -> A{1} B{2} A{3} // A{3} B{2} A{1}
A -> a A{1} // c A{1} 
B -> b B{1} // d B{1}
A -> a // c
B -> b // d
"""

sync_cfg = TreeSynCFG.fromstring(g)

dfa_definitions = build_dfa_from_treesyncfg(sync_cfg)
for nonterminal, dfa in dfa_definitions.items():
    print(f"{nonterminal} -> {dfa}")
