import random
from nltk import CFG
from nltk.parse.generate import generate
import pandas as pd

df = pd.read_csv('word_database.csv') 

root_db     = []
prefix_db   = []
suffix_db   = []

for index, row in df.iterrows():
    if row['type'] == 'root':
        root_db.append(row['value'])
    elif row['type'] == 'prefix':
        prefix_db.append(row['value'])
    elif row['type'] == 'suffix':
        suffix_db.append(row['value'])


# Random selection functions
def random_select_prefix_db():
    return random.choice(prefix_db)
def random_select_root_db():
    return random.choice(root_db)
def random_select_suffix_db():
    return random.choice(suffix_db)

# Helper function for random value between Min and Max
def random_choice(min_val, max_val):
    prob = random.randint(0, 100) 
    if prob <= 60 and max_val-1 > min_val:
        return random.randint(min_val, max_val-1)
    else:
        return max_val


# GENERATION FUNCTIONS
def generate_word(min_prefixes=0, max_prefixes=2, min_roots=1, max_roots=2, min_suffixes=0, max_suffixes=2):
    num_prefixes = random_choice(min_prefixes, max_prefixes)
    num_roots = random_choice(min_roots, max_roots)
    num_suffixes = random_choice(min_suffixes, max_suffixes)

    prefixes = ''.join([random_select_prefix_db() for _ in range(num_prefixes)])
    roots = ''.join([random_select_root_db() for _ in range(num_roots)])
    suffixes = ''.join([random_select_suffix_db() for _ in range(num_suffixes)])

    return f"{prefixes}{roots}{suffixes}"


##########################################################################################################
##                                          MAIN
##########################################################################################################

## ASSUMING THAT:
#   Nomi: 40-50% 
#   Verbi: 20-30%
#   Aggettivi: 10-20%
#   Avverbi/Preposizioni/Determinativi/Pronomi: 10%

def generate_language_database():
    num_nouns = random.randint(2000, 3000)
    num_verbs = random.randint(1200, 2000)
    num_adj = random.randint(700, 1000)
    num_adv = random.randint(300, 600)
    num_prep = random.randint(10, 30)
    num_det = random.randint(20, 60)
    num_pron = random.randint(10, 70)

    dictionary = {
        'nouns': [],
        'verbs': [],
        'adjectives': [],
        'adverbs': [],
        'prepositions': [],
        'determiners': [],
        'pronouns': []
    }

    # Generate nouns
    for _ in range(num_nouns):
        generated_noun = generate_word(min_prefixes=0, max_prefixes=2, 
                                        min_roots=1, max_roots=2, 
                                        min_suffixes=0, max_suffixes=1)
        dictionary['nouns'].append(generated_noun)

    # Generate verbs
    for _ in range(num_verbs):
        generated_verb = generate_word(min_prefixes=0, max_prefixes=2, 
                                        min_roots=1, max_roots=2, 
                                        min_suffixes=1, max_suffixes=2)
        dictionary['verbs'].append(generated_verb)

    # Generate adjectives
    for _ in range(num_adj):
        generated_adjective = generate_word(min_prefixes=0, max_prefixes=2, 
                                             min_roots=1, max_roots=2, 
                                             min_suffixes=1, max_suffixes=2)
        dictionary['adjectives'].append(generated_adjective)

    # Generate adverbs
    for _ in range(num_adv):
        generated_adverb = generate_word(min_prefixes=0, max_prefixes=2, 
                                          min_roots=1, max_roots=2, 
                                          min_suffixes=1, max_suffixes=2)
        dictionary['adverbs'].append(generated_adverb)

    # Generate prepositions
    for _ in range(num_prep):
        generated_preposition = generate_word(min_prefixes=0, max_prefixes=0, 
                                              min_roots=1, max_roots=1, 
                                              min_suffixes=0, max_suffixes=0)
        dictionary['prepositions'].append(generated_preposition)

    # Generate determiners
    for _ in range(num_det):
        generated_determiner = generate_word(min_prefixes=0, max_prefixes=0, 
                                              min_roots=1, max_roots=1, 
                                              min_suffixes=0, max_suffixes=0)
        dictionary['determiners'].append(generated_determiner)

    # Generate pronouns
    for _ in range(num_pron):
        generated_pronoun = generate_word(min_prefixes=0, max_prefixes=0, 
                                           min_roots=1, max_roots=1, 
                                           min_suffixes=0, max_suffixes=0)
        dictionary['pronouns'].append(generated_pronoun)

    return dictionary


# Generate two language databases
dictionary1 = generate_language_database()
dictionary2 = generate_language_database()

# Create DataFrames for both dictionaries
df1 = pd.DataFrame({'nouns': pd.Series(dictionary1['nouns']),
    'verbs': pd.Series(dictionary1['verbs']),
    'adjectives': pd.Series(dictionary1['adjectives']),
    'adverbs': pd.Series(dictionary1['adverbs']),
    'prepositions': pd.Series(dictionary1['prepositions']),
    'determiners': pd.Series(dictionary1['determiners']),
    'pronouns': pd.Series(dictionary1['pronouns'])})

df2 = pd.DataFrame({'nouns': pd.Series(dictionary2['nouns']),
    'verbs': pd.Series(dictionary2['verbs']),
    'adjectives': pd.Series(dictionary2['adjectives']),
    'adverbs': pd.Series(dictionary2['adverbs']),
    'prepositions': pd.Series(dictionary2['prepositions']),
    'determiners': pd.Series(dictionary2['determiners']),
    'pronouns': pd.Series(dictionary2['pronouns'])})

df1.fillna('', inplace=True)
df2.fillna('', inplace=True)
df1.to_csv('generated_words_lang1.csv', index=False)
df2.to_csv('generated_words_lang2.csv', index=False)

