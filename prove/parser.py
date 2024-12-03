from nltk import Nonterminal

class REG_Lang_Parser:
    def __init__(self, grammar, source_tokens, target_tokens):
        self._grammar = grammar
        self._source_tokens = source_tokens
        self._target_tokens = target_tokens
        self._start_state = "S"

    def parse_grammar(grammar_string):
        # empty dictionary
        grammar = {}

        for line in grammar_string.strip().split("\n"):
            if not line.strip():
                continue

            # Split line into (LHS) and (RHS)
            lhs, rhs = line.split("->")
            lhs = lhs.strip()

            # Split the synchronous RHS rules
            rules = rhs.split("//")
            if lhs not in grammar:
                grammar[lhs] = []

            # Add each synchronous rule pair to the grammar
            grammar[lhs].append(tuple(r.strip() for r in rules))

        return grammar
        












class CFG_Lang_Parser:
    def __init__(self, grammar, source_tokens, target_tokens):
        self._source_tokens = source_tokens
        self._target_tokens = target_tokens
        self._grammar = grammar

        self._start_state = "S"


    