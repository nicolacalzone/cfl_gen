import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter


#####################
# MEASURES FOR DATA #
#####################
def compute_sentence_length_metrics(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        sentences = [line.strip().split()[0] for line in lines]
        frequencies = [int(line.strip().split()[1]) for line in lines]

    sentence_lengths = [len(sentence) for sentence, freq in zip(sentences, frequencies) for _ in range(freq)]

    max_sentence_length = max(sentence_lengths)
    min_sentence_length = min(sentence_lengths)
    median_sentence_length = np.median(sentence_lengths)
    mean_sentence_length = np.mean(sentence_lengths)

    print(f"Sentence Lengths Metrics:")
    print(f"Max length: {max_sentence_length}")
    print(f"Min length: {min_sentence_length}")
    print(f"Median length: {median_sentence_length}")
    print(f"Mean length: {mean_sentence_length}")

def compute_letter_counts(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        sentences = [line.strip().split()[0] for line in lines]
        frequencies = [int(line.strip().split()[1]) for line in lines]

    all_letters = "".join([sentence * freq for sentence, freq in zip(sentences, frequencies)])
    letter_counts = Counter(all_letters)
    print("\nLetter Counts:")
    for letter, count in letter_counts.items():
        print(f"{letter}: {count}")
    letters = list(letter_counts.keys())
    counts = list(letter_counts.values())
    plt.figure(figsize=(10, 6))
    plt.bar(letters, counts, color='blue', alpha=0.7)
    plt.xlabel('Letters')
    plt.ylabel('Frequency')
    plt.title('Histogram of Letter Frequencies')
    plt.show()

def compute_sentence_length_distribution(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        sentences = [line.strip().split()[0] for line in lines]
        frequencies = [int(line.strip().split()[1]) for line in lines]

    sentence_lengths = [len(sentence) for sentence, freq in zip(sentences, frequencies) for _ in range(freq)]
    sentence_length_distribution = Counter(sentence_lengths)

    # Plot the distribution of sentence lengths
    plt.figure(figsize=(8, 5))
    plt.bar(sentence_length_distribution.keys(), sentence_length_distribution.values(), color='blue', alpha=0.7)
    plt.xlabel("Sentence Length")
    plt.ylabel("Frequency")
    plt.title("Distribution of Sentence Lengths")
    plt.show()

def measure_metrics(file_path):
    compute_sentence_length_metrics(file_path)
    compute_letter_counts(file_path)
    compute_sentence_length_distribution(file_path)




#############################
# MEASURES FOR TRANSFORMERS #
#############################

# H = the tokenized Hypothesis loss
# D = the detokenized Hypothesis loss
# P = positional token loss --> H is the mean of all the P values

def plot_accuracy(loss: list[int, float]):
    x = [epoch for epoch, _ in loss]
    y = [score for _, score in loss]

    plt.figure(figsize=(8, 5))
    plt.plot(x, y, color='blue')
    plt.xlabel("Epochs")
    plt.ylabel("Accuracy")
    plt.title("Accuracy over Epochs")
    plt.show()
    

def plot_bleu(bleu: list[tuple[int, float]]): ##  list( #_epoch, bleu_score )
    
    x = [epoch for epoch, _ in bleu]
    y = [score for _, score in bleu]

    plt.figure(figsize=(8, 5))
    plt.plot(x, y, color='blue')
    plt.xlabel("Epochs")
    plt.ylabel("BLEU Score")
    plt.title("BLEU Score over Epochs")
    plt.show()



def compute_heatmap(file_path):
    pass

def measure_transformer(file_path):
    pass 














if __name__ == "__main__":
    dir = "output/freq/"
    file_path_src = f"{dir}.src"
    file_path_tgt = f"{dir}/train.tgt"
    measure_metrics(file_path_src)
    measure_metrics(file_path_tgt)
