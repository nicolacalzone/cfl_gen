import nltk
from nltk import CFG
import random as rand
import pandas as pd

def safejoin(pos_tag):
    return ' | '.join(f"'{elem}'" for elem in pos_tag) if pos_tag else ''

def random_generate(grammar, start_symbol=None):
    if start_symbol is None:
        start_symbol = grammar.start()
        structure_tree = []
    
    # Function to expand the symbol recursively
    def expand(symbol):
        # If the symbol is terminal, just return it
        if isinstance(symbol, str):
            return [symbol]
        
        # Otherwise, randomly choose a production for this non-terminal
        productions = grammar.productions(lhs=symbol)
        production = rand.choice(productions)
        
        # Recursively expand the symbols on the right-hand side of the production
        result = []
        for sym in production.rhs():
            if symbol == 'None':
                structure_tree.append(symbol)
            else:
                structure_tree.append(sym)

            symbol = result.extend(expand(sym))
        return result

    return ' '.join(expand(start_symbol)), structure_tree

def grammar(param):
    grammar1 = CFG.fromstring(f"""
                                S -> {param[0]}
                                NP -> Det N | Det N Adj | PP
                                PP -> P N
                                V -> {safejoin(verbs1)}
                                P -> {safejoin(prepositions1)} 
                                Det -> {safejoin(determiners1)} 
                                Adj -> {safejoin(adjectives1)}
                                N -> {safejoin(nouns1)} 
                                """)
    grammar2 = CFG.fromstring(f"""
                                S -> {param[1]}
                                NP -> N | N PP | N Adj | Adj N PP
                                PP -> P N
                                V -> {safejoin(verbs2)}
                                P -> {safejoin(prepositions2)}
                                Adj -> {safejoin(adjectives2)}
                                N -> {safejoin(nouns2)}
                                """)
    
    return grammar1, grammar2


df = pd.read_csv('generated_words_lang1.csv')  
df2 = pd.read_csv('generated_words_lang2.csv') 
df = df.dropna()
df2 = df2.dropna()
nouns1 = df['nouns'].tolist() 
verbs1 = df['verbs'].tolist() 
adjectives1 = df['adjectives'].tolist() 
adverbs1 = df['adverbs'].tolist() 
prepositions1 = df['prepositions'].tolist() 
determiners1 = df['determiners'].tolist() 
pronouns1 = df['pronouns'].tolist() 
nouns2 = df2['nouns'].tolist() 
verbs2 = df2['verbs'].tolist() 
adjectives2 = df2['adjectives'].tolist() 
adverbs2 = df2['adverbs'].tolist() 
prepositions2 = df2['prepositions'].tolist() 
determiners2 = df2['determiners'].tolist() 
pronouns2 = df2['pronouns'].tolist() 

num_sentences = 10

grammars1 = []
grammars2 = []
for i in range(num_sentences):

    r = rand.choice([0,1])

    if r == 1:
        grammar1, grammar2 = grammar(['NP V NP','NP NP V'])
    else:
        grammar1, grammar2 = grammar(['NP V PP','NP PP V'])

    grammars1.append(grammar1)
    grammars2.append(grammar2)

sentences_grammar1 = []
sentences_grammar2 = []

for i in range(len(grammars1)):
    sentences_grammar1.append(random_generate(grammars1[i]))
    sentences_grammar2.append(random_generate(grammars2[i]))


for grammar in zip(sentences_grammar1, sentences_grammar2):
    for sentence, structure_tree in grammar:
        print("Generated Sentence:", sentence)
        print()
        print("Structure Tree:", structure_tree)
        print()
        print()