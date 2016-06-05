import os
import sys
sys.path.append(os.path.abspath(__file__ + "/../../"))

import word2vec

model = word2vec.load('training_text_clean.bin')

file = open('training_text_vectors.txt', 'w')

for word in model.vocab:
    newlist = []
    for item in model[word].tolist():
        newlist.append(str(item))

    features = ' '.join(newlist)
    file.write(str(word) + ' ' + features + '\n')

file.close()