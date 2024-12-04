import re

# Regular expression for A
A_regex_src = r'(a)+'
A_regex_tgt = r'(c)+'


# Regular expression for B
B_regex_src = r'(b)+'
B_regex_tgt = r'(d)+'


# Regular expression for S
S_regex = r'(' + A_regex_src + B_regex_src + A_regex_src + r')|(' + A_regex_tgt + B_regex_tgt + A_regex_tgt + r')'


def read_file(file_path):
    words = []
    counter = 0

    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 1:
                word = parts[0]
                cnt = 1  # Default count if not provided
            else:
                word, cnt = parts

            #print(word, cnt)
            words.append(word)
            counter += int(cnt)

    return words, counter


sources, counter_src = read_file('db/train/sr')
targets, counter_tgt = read_file('db/train/tg')

print(counter_src, counter_tgt)

with open('db/train/sr_acceptor', 'w') as sr_acceptor, open('db/train/tg_acceptor', 'w') as tg_acceptor:
    print("Matching words from sr:")
    ln = 0
    for word in sources:
        if re.fullmatch(S_regex, word):
            sr_acceptor.write(f"{word}\tyes\n")
        else:
            sr_acceptor.write(f"{word}\tno\n")
        ln += 1

    print("\nTarget words from tg:")
    for word in targets:
        if re.fullmatch(S_regex, word):
            tg_acceptor.write(f"{word} yes\n")
            continue
        else:
            tg_acceptor.write(f"{word} no\n")
            print(f"{word} does not match regex")