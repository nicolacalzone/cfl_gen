from nltk.grammar import Nonterminal
import os
from collections import Counter

def filter_terminals(sentence):
    sentence_str = ' '.join(str(symbol) for symbol in sentence)
    return [symbol for symbol in sentence_str.split() if symbol != 'eps' and not isinstance(symbol, Nonterminal)]

def build_dataset(sentence_pairs, num_sentences, depth_str, grammar_str) -> tuple[str, str]:

        source_counter = Counter(pair[0] for pair in sentence_pairs)
        target_counter = Counter(pair[1] for pair in sentence_pairs)

        ## TRAIN / VALID / TEST
        # 60% train sentences, 20% valid sentences, 20% test sentences
        train_sentences = int(num_sentences * 0.6)
        valid_sentences = int(num_sentences * 0.2)  
        #test_sentences = int(num_sentences * 0.2)   # no need to compute test_sentences

        ## Write to files - Strings
        dir = "output"
        freq_dir = f"{dir}/freq"
        single_dir = f"{dir}/single"
        parallel_dir = f"{dir}/parallel"

        os.makedirs(dir         , exist_ok=True)
        os.makedirs(freq_dir    , exist_ok=True)
        os.makedirs(parallel_dir, exist_ok=True)

        train_file = f"/train" + depth_str + grammar_str
        valid_file = f"/valid" + depth_str + grammar_str
        test_file = f"/test" + depth_str + grammar_str
        ext_src = ".src"
        ext_tgt = ".tgt"
        ext_parallel = ".parallel"

        #############   Write clean parallel files
        # train -> from 0 to train_sentences
        with open(f'{parallel_dir}{train_file}{ext_parallel}', 'w') as parallel_file:
            for source, target in sentence_pairs[:train_sentences]: 
                parallel_file.write(f"{source}\t{target}\n")

        # valid -> from train_sentences to train_sentences + valid_sentences
        with open(f'{parallel_dir}{valid_file}{ext_parallel}', 'w') as parallel_file:
            for source, target in sentence_pairs[train_sentences:train_sentences + valid_sentences]:
                parallel_file.write(f"{source}\t{target}\n") 

        # test  -> from train_sentences + valid_sentences to END
        with open(f'{parallel_dir}{test_file}{ext_parallel}', 'w') as parallel_file:
            for source, target in sentence_pairs[train_sentences + valid_sentences:]:
                parallel_file.write(f"{source}\t{target}\n") 

        #############   Write single files
        # train from 0 to train_sentences
        with open(f"{single_dir}{train_file}{ext_src}", 'w') as src_file:
            for source, target in sentence_pairs[:train_sentences]:
                src_file.write(f"{source}\n")
        with open(f"{single_dir}{train_file}{ext_tgt}", 'w') as tgt_file:
            for source, target in sentence_pairs[:train_sentences]:
                tgt_file.write(f"{target}\n")

        # valid from train_sentences to train_sentences + valid_sentences
        with open(f"{single_dir}{valid_file}{ext_src}", 'w') as src_file:
            for source, target in sentence_pairs[train_sentences:train_sentences + valid_sentences]:
                src_file.write(f"{source}\n")
        with open(f"{single_dir}{valid_file}{ext_tgt}", 'w') as tgt_file:
            for source, target in sentence_pairs[train_sentences:train_sentences + valid_sentences]:
                tgt_file.write(f"{target}\n")

        # test from train_sentences + valid_sentences to END
        with open(f"{single_dir}{test_file}{ext_src}", 'w') as src_file:
            for source, target in sentence_pairs[train_sentences + valid_sentences:]:
                src_file.write(f"{source}\n")
        with open(f"{single_dir}{test_file}{ext_tgt}", 'w') as tgt_file:
            for source, target in sentence_pairs[train_sentences + valid_sentences:]:
                tgt_file.write(f"{target}\n")


        ### Write single files frequencies
        with open(f"{freq_dir}{train_file}.src", 'w') as src_file:
            for source, freq in source_counter.items():
                src_file.write(f"{source} {freq}\n")
        with open(f"{freq_dir}{train_file}.tgt", 'w') as tgt_file:
            for target, freq in target_counter.items():
                tgt_file.write(f"{target} {freq}\n")

        with open(f"{freq_dir}{valid_file}.src", 'w') as src_file:
            for source, freq in source_counter.items():
                src_file.write(f"{source} {freq}\n")
        with open(f"{freq_dir}{valid_file}.tgt", 'w') as tgt_file:
            for target, freq in target_counter.items():
                tgt_file.write(f"{target} {freq}\n")

        with open(f"{freq_dir}{test_file}.src", 'w') as src_file:
            for source, freq in source_counter.items():
                src_file.write(f"{source} {freq}\n")
        with open(f"{freq_dir}{test_file}.tgt", 'w') as tgt_file:
            for target, freq in target_counter.items():
                tgt_file.write(f"{target} {freq}\n")

        print("Dataset built successfully!")

        return f"{freq_dir}{train_file}.src", f"{freq_dir}{train_file}.tgt"