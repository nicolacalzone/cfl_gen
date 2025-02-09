from include.SCFG_tree import TreeSynCFG
import logging as log
import random as rand
import pandas as pd
import concurrent.futures
import torch
from utils.constants import g, g1
from utils.utils import build_dataset, filter_terminals
from utils.metrics import measure_metrics

pd.set_option('future.no_silent_downcasting', True)
log.basicConfig(filename='logs/SCFG_Generator.log', 
                    filemode='a',
                    level=log.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
    
def sentence_generator(sync_cfg, num_sentences, device):
    """
        This function will generate #(num_sentences) sentences using the synchronous CFG, TreeSynCFG
        - Epsilon productions are filtered through the filter_terminals() function
        - The sentences are stored in a list of tuples
           where each tuple contains a source sentence and a target sentence
    """
    sentence_pairs = []
    cycles_counter = 0
    while len(sentence_pairs) < num_sentences:
        
        p_factor = rand.uniform(0.60, 0.75)     
        depth = rand.randint(1, 4)
        sync_cfg.set_initial_depth(depth)
        s_tree, s_sentence, t_tree, t_sentence = sync_cfg.produce(p_factor)

        source_sentence_filtered = filter_terminals(s_sentence)
        target_sentence_filtered = filter_terminals(t_sentence)
        source_sentence = ''.join(source_sentence_filtered)
        target_sentence = ''.join(target_sentence_filtered)

        #log.info(f"\nSource sentence: {source_sentence}, Target sentence: {target_sentence}")
        #log.info(f"Source tree: {s_tree}, Target tree: {t_tree}")

        # Filter out empty strings
        if source_sentence and target_sentence:
            sentence_pairs.append((source_sentence, target_sentence))

        cycles_counter += 1
        if cycles_counter % 500 == 0:
            remaining_sentences = num_sentences - len(sentence_pairs)
            print(f"Remaining sentences to produce: {remaining_sentences}")

    return sentence_pairs

def sentence_generator_threaded(sync_cfg, num_sentences, num_threads):
    log.info("cuda" if torch.cuda.is_available() else "cpu")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    sentence_pairs = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(sentence_generator, sync_cfg, num_sentences // num_threads, device) for _ in range(num_threads)]
        for future in concurrent.futures.as_completed(futures):
            sentence_pairs.extend(future.result())
    return sentence_pairs

if __name__ == '__main__':

    used_grammar = g 
    num_sentences = 10000 
    num_threads = 8
    sources = []
    targets = []

    sync_cfg = TreeSynCFG.fromstring(used_grammar)
    sentence_pairs = sentence_generator_threaded(sync_cfg, num_sentences, num_threads)

    f_src, f_tgt = build_dataset(sentence_pairs, num_sentences)
    measure_metrics(f_src)
    measure_metrics(f_tgt)