import random

words = ['lorem', 'ipsum', 'dolor', 'sit', 'amet', 'consectetur', 'adipiscing', 'elit']

with open("lorem.txt", "w") as f:
    for i in range(1000):
        sentence = ' '.join(random.choices(words, k=10))
        f.write(sentence + "\n")