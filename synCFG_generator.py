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
from metrics.metrics import main
import os

pd.set_option('future.no_silent_downcasting', True)
log.basicConfig(filename='logs/app.log', 
                    filemode='a',
                    level=log.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
    

def filter_terminals(sentence):
    sentence_str = ''.join(str(symbol) for symbol in sentence)
    
    return [symbol for symbol in sentence_str.split() if symbol != 'eps' and not isinstance(symbol, Nonterminal)]


## a - d 1a gramm
## e - h 2a gramm

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

F -> c // g
F -> a // e
"""

g1 = """
S -> A{1} B{2} // B{2} A{1}
A -> A{1} B{2} // B{2} A{1}
B -> b // d
A -> a // c
"""

used_grammar = g


def generate_sentences(sync_cfg, num_sentences, device):
    sentence_pairs = []
    cycles_counter = 0
    while len(sentence_pairs) < num_sentences:

        #decay_factor = rand.uniform(0.01, 0.99)  ## (0.01, 0.99)

        depth = rand.randint(4, 10)              ## (1, 1000)
        p_factor = rand.uniform(0.55, 0.73)      

        s_tree, s_sentence, t_tree, t_sentence = sync_cfg.produce(p_factor, depth)

        source_sentence_filtered = filter_terminals(s_sentence)
        target_sentence_filtered = filter_terminals(t_sentence)
        source_sentence = ''.join(source_sentence_filtered)
        target_sentence = ''.join(target_sentence_filtered)

        #print(f"\nSource sentence: {source_sentence}")
        #print(f"Source tree: {s_tree}")
        #print(f"\nTarget sentence: {target_sentence}")
        #print(f"Target tree: {t_tree}")

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
sync_cfg = TreeSynCFG.fromstring(used_grammar)

num_sentences = 100000
num_threads = 8
sentence_pairs = generate_sentences_threaded(sync_cfg, num_sentences, num_threads)

source_counter = Counter(pair[0] for pair in sentence_pairs)
target_counter = Counter(pair[1] for pair in sentence_pairs)


## TRAIN / VALID / TEST
# 60% train sentences, 20% valid sentences, 20% test sentences
train_sentences = int(num_sentences * 0.7)
valid_sentences = int(num_sentences * 0.2)  
test_sentences = int(num_sentences * 0.1)

## Write to files - Strings
dir = "output"
freq_dir = f"{dir}/freq"
parallel_dir = f"{dir}/parallel"
os.makedirs(dir         , exist_ok=True)
os.makedirs(freq_dir    , exist_ok=True)
os.makedirs(parallel_dir, exist_ok=True)
train_file = f"{dir}/train"
valid_file = f"{dir}/valid"
test_file = f"{dir}/test"


#############   Write clean parallel files
# train
with open(f'{parallel_dir}/train.src', 'w') as parallel_file:
    # from 0 to train_sentences
    for source, target in sentence_pairs[:train_sentences]:
        parallel_file.write(f"{source}\t{target}\n")

# valid
with open(f'{parallel_dir}/valid', 'w') as parallel_file:
    # from train_sentences to train_sentences + valid_sentences
    for source, target in sentence_pairs[train_sentences:train_sentences + valid_sentences]:
        parallel_file.write(f"{source}\t{target}\n")

# test
with open(f'{parallel_dir}/test', 'w') as parallel_file:
    # from train_sentences + valid_sentences to END
    for source, target in sentence_pairs[train_sentences + valid_sentences:]:
        parallel_file.write(f"{source}\t{target}\n")


### Write clean non-parallel files

# train from 0 to train_sentences
with open(f"{train_file}.src", 'w') as src_file:
    for source, target in sentence_pairs[:train_sentences]:
        src_file.write(f"{source}\n")
with open(f"{train_file}.tgt", 'w') as tgt_file:
    for source, target in sentence_pairs[:train_sentences]:
        tgt_file.write(f"{target}\n")

# valid from train_sentences to train_sentences + valid_sentences
with open(f"{valid_file}.src", 'w') as src_file:
    for source, target in sentence_pairs[train_sentences:train_sentences + valid_sentences]:
        src_file.write(f"{source}\n")
with open(f"{valid_file}.tgt", 'w') as tgt_file:
    for source, target in sentence_pairs[train_sentences:train_sentences + valid_sentences]:
        tgt_file.write(f"{target}\n")

# test from train_sentences + valid_sentences to END
with open(f"{test_file}.src", 'w') as src_file:
    for source, target in sentence_pairs[train_sentences + valid_sentences:]:
        src_file.write(f"{source}\n")

with open(f"{test_file}.tgt", 'w') as tgt_file:
    for source, target in sentence_pairs[train_sentences + valid_sentences:]:
        tgt_file.write(f"{target}\n")