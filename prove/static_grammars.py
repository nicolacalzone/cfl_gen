from nltk.grammar import PCFG, CFG, Nonterminal, Production
from nltk.parse.generate import generate
import pandas as pd
import random
import logging
from datetime import datetime

# f'logs/app_{datetime.now().strftime("%Y-%m-%d_%H:%M:%S")}.log'

logging.basicConfig(filename='logs/app.log', 
                    filemode='a',
                    level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

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
        production = random.choice(productions)
        
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


def safejoin(pos_tag):
    return ' | '.join(f"'{elem}'" for elem in pos_tag) if pos_tag else ''

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



##  Yes determiners
##  SVO
grammar1 = CFG.fromstring(f"""
                            S -> NP V NP | NP V PP
                            NP -> Det N | Det N Adj | PP
                            PP -> P N
                            V -> {safejoin(verbs1)}
                            P -> {safejoin(prepositions1)} 
                            Det -> {safejoin(determiners1)} 
                            Adj -> {safejoin(adjectives1)}
                            N -> {safejoin(nouns1)} 
                            """)

##  No determiners
##  SOV
grammar2 = CFG.fromstring(f"""
                            S -> NP NP V  | NP PP V 
                            NP -> N | N PP | N Adj | Adj N PP
                            PP -> P N
                            V -> {safejoin(verbs2)}
                            P -> {safejoin(prepositions2)}
                            Adj -> {safejoin(adjectives2)}
                            N -> {safejoin(nouns2)}
                            """)


sentences_grammar1 = [random_generate(grammar1) for _ in range(1)]
sentences_grammar2 = [random_generate(grammar2) for _ in range(1)]

for sentence, structure_tree in sentences_grammar1:
    print("Generated Sentence:", sentence)
    print("Structure Tree:", structure_tree)
    logging.info(f"Generated Sentence: {sentence}")
    logging.info(f"Structure Tree: {structure_tree}")


print()

for sentence, structure_tree in sentences_grammar2:
    print("Generated Sentence:", sentence)
    print("Structure Tree:", structure_tree)
    logging.info(f"Generated Sentence: {sentence}")
    logging.info(f"Structure Tree: {structure_tree}")

logging.info("END\n")

parallel_corpus = list(zip(sentences_grammar1, sentences_grammar2))

df_parallel = pd.DataFrame(parallel_corpus, columns=['Grammar1_Sentence', 'Grammar2_Sentence'])
df_parallel.to_csv('parallel_corpus_without_meanings.csv', index=False)