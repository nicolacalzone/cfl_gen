# recogniser.py
# Translation of Lua code for an Earley parser

class EarleyItem:
    def __init__(self, rule, next, start):
        self.rule = rule 
        self.next = next 
        self.start = start 

    def __repr__(self):
        return f"EarleyItem({self.rule}, {self.next}, {self.start})"

    def __eq__(self, other):
        return self.rule == other.rule and self.next == other.next and self.start == other.start


class Grammar:
    def __init__(self, start_rule_name, rules):
        self.start_rule_name = start_rule_name # Name of the start rule
        self.rules = rules # List of rules


def char(c):
    def predicate(input, index=None):
        if input is None:
            return f"'{c}'"  # Pretty print
        return index < len(input) and input[index] == c
    return predicate

def range_char(r):
    def predicate(input, index=None):
        if input is None:
            return f"[{r[0]}-{r[1]}]"
        return index < len(input) and r[0] <= input[index] <= r[1]
    return predicate


def class_chars(chars):
    def predicate(input, index=None):
        if input is None:
            return f"[{chars}]"
        return index < len(input) and input[index] in chars
    return predicate


def next_symbol(grammar, item):

    ## PROBABLY HERE I NEED TO ADD SOURCE_RHS AND TARGET_RHS

    return grammar.rules[item.rule][item.next] if item.next < len(grammar.rules[item.rule]) else None


def name(grammar, item):

    ## PROBABLY HERE I NEED TO ADD SOURCE_RHS AND TARGET_RHS

    return grammar.rules[item.rule][0]


def append(set_, item):
    ## RULE: no duplicates otherwise it will loop forever
    if item not in set_:
        set_.append(item)


## COMPLETION OPERATION
## Nothing on the right of the DOT? --> YES --> add to state set all parent Early Items
def complete(S, i, j, grammar):
    item = S[i][j]

    for old_item in S[item.start]:
        if next_symbol(grammar, old_item) == name(grammar, item):
            append(S[i], EarleyItem(old_item.rule, old_item.next + 1, old_item.start))

            method_name = "complete()"
            print(method_name, item)


## SCAN OPERATION
## symbol at the right of the DOT is a terminal? --> does it match the symbol? --> YES --> move the DOT to the right
def scan(S, i, j, symbol, input):
    item = S[i][j]

    if symbol(input, i):
        if len(S) <= i + 1:
            S.append([])
        append(S[i + 1], EarleyItem(item.rule, item.next + 1, item.start))
 
        method_name = "scan()"
        print(method_name, item)

## PREDICTION OPERATION
## symbol at the right of the DOT is a non-terminal? --> YES --> add all rules that start with that non-terminal
def predict(S, i, symbol, grammar):
    method_name = "predict()"
    for rule_index, rule in enumerate(grammar.rules):
        if rule[0] == symbol:
            append(S[i], EarleyItem(rule_index, 1, i))
            print(method_name, S[i])


def build_items(grammar, input):
    S = [[]]
    for rule_index, rule in enumerate(grammar.rules):
        if rule[0] == grammar.start_rule_name:
            append(S[0], EarleyItem(rule_index, 1, 0))

    i = 0
    while i < len(S):
        j = 0
        while j < len(S[i]):
            symbol = next_symbol(grammar, S[i][j])
            if symbol is None:
                complete(S, i, j, grammar)
            elif callable(symbol):
                scan(S, i, j, symbol, input)
            elif isinstance(symbol, str):
                predict(S, i, symbol, grammar)
            else:
                raise ValueError("Invalid symbol in grammar")
            j += 1
        i += 1
    return S


def has_partial_parse(S, i, grammar):
    for item in S[i]:
        rule = grammar.rules[item.rule]
        if rule[0] == grammar.start_rule_name and item.next > len(rule) - 1 and item.start == 0:
            return True
    return False


def has_complete_parse(S, grammar):
    return has_partial_parse(S, len(S) - 1, grammar)


def last_partial_parse(S, grammar):
    for i in range(len(S) - 1, -1, -1):
        if has_partial_parse(S, i, grammar):
            return i
    return None


def diagnose(S, grammar, input_):
    if has_complete_parse(S, grammar):
        print("The input has been recognized. Congratulations!")
    else:
        if len(S) == len(input_) + 1:
            print("The whole input made sense. Maybe it is incomplete?")
        else:
            print(f"The input stopped making sense at character {len(S)}")
        lpp = last_partial_parse(S, grammar)
        if lpp is not None:
            print(f"This beginning of the input has been recognized: {input_[:lpp]}")
        else:
            print("The beginning of the input couldn't be parsed.")


def print_items(S, grammar):
    for i, set_ in enumerate(S):
        print(f"=== {i} ===")
        for item in set_:
            rule = grammar.rules[item.rule]
            print(f"{rule[0]} ->", end=" ")
            for k, symbol in enumerate(rule[1:], start=1):
                if k == item.next:
                    print("•", end=" ")
                # Only print the description of callable symbols
                print(symbol(None) if callable(symbol) else symbol, end=" ")
            if item.next > len(rule) - 1:
                print("•", end=" ")
            print(f"  ({item.start})")
        print()



# Example Usage
if __name__ == "__main__":
    example_grammar = Grammar(
        "Sum",
        [
            ("Sum", "Sum", class_chars("+-"), "Product"),
            ("Sum", "Product"),
            ("Product", "Product", class_chars("*/"), "Factor"),
            ("Product", "Factor"),
            ("Factor", char("("), "Sum", char(")")),
            ("Factor", "Number"),
            ("Number", range_char("09"), "Number"),
            ("Number", range_char("09")),
        ],
    )


    input_string = "1+2*3+8"
    S = build_items(example_grammar, input_string)
    print(f"Input: {input_string}")
    print_items(S, example_grammar)
    diagnose(S, example_grammar, input_string)
