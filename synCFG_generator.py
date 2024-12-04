from include.SCFG_tree import TreeSynCFG
from nltk.grammar import Nonterminal
from collections import Counter
import logging as log
import random as rand
import pandas as pd
import re
from collections import defaultdict
import concurrent.futures
import torch

pd.set_option('future.no_silent_downcasting', True)
log.basicConfig(filename='logs/app.log', 
                    filemode='a',
                    level=log.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
    

def filter_terminals(sentence):
    sentence_str = ''.join(str(symbol) for symbol in sentence)
    
    return [symbol for symbol in sentence_str.split() if symbol != 'eps' and not isinstance(symbol, Nonterminal)]

g = """
S -> A{1} B{2} A{3} // A{3} B{2} A{1}
A -> a A{1} // c A{1} 
B -> b B{1} // d B{1}
A -> a // c
B -> b // d
"""

g1 = """
S -> NP{1} VP{2} // NP{1} VP{2} 
NP -> DET{1} N{2} // DET{1} N{2}
DET -> the // eps
N -> cat // kot
VP -> runs // begaet
VP -> sleeps // spit
VP -> eats // edet
VP -> drinks // pyot
"""

def generate_sentences(sync_cfg, num_sentences, device):
    sentence_pairs = []
    cycles_counter = 0
    while len(sentence_pairs) < num_sentences:

        depth = rand.randint(1, 1000)
        decay_factor = rand.uniform(0.01, 0.99)

        s_tree, s_sentence, t_tree, t_sentence = sync_cfg.produce(depth=depth, decay_factor=decay_factor)

        source_sentence_filtered = filter_terminals(s_sentence)
        target_sentence_filtered = filter_terminals(t_sentence)
        source_sentence = ''.join(source_sentence_filtered)
        target_sentence = ''.join(target_sentence_filtered)

        # Filter out empty strings
        if source_sentence and target_sentence:
            sentence_pairs.append((source_sentence, target_sentence))

        cycles_counter += 1

        if cycles_counter % 500 == 0:
            remaining_sentences = num_sentences - len(sentence_pairs)
            print(f"Remaining sentences to produce: {remaining_sentences}")

    return sentence_pairs

def generate_sentences_threaded(sync_cfg, num_sentences, num_threads):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    sentence_pairs = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(generate_sentences, sync_cfg, num_sentences // num_threads, device) for _ in range(num_threads)]
        for future in concurrent.futures.as_completed(futures):
            sentence_pairs.extend(future.result())

    return sentence_pairs

sources = []
targets = []

log.info("\n\n\t*** GRAMMAR ***\n")
sync_cfg = TreeSynCFG.fromstring(g)

num_sentences = 25000
num_threads = 4  

sentence_pairs = generate_sentences_threaded(sync_cfg, num_sentences, num_threads)

source_counter = Counter(pair[0] for pair in sentence_pairs)
target_counter = Counter(pair[1] for pair in sentence_pairs)

with open('db/train/sr', 'w') as source_file:
    for word, freq in source_counter.items():
        source_file.write(f"{word} {freq}\n")

with open('db/train/tg', 'w') as target_file:
    for word, freq in target_counter.items():
        target_file.write(f"{word} {freq}\n")


