import os
import sys
sys.path.append(os.path.abspath(__file__ + "/../../"))

import pandas as pd
import word2vec as w2v

#w2v.word2phrase('text8.txt', 'text8-phrases', verbose=True)

w2v.word2vec('training_text.txt', 'training_text_clean.bin', size=100, verbose=True)

#w2v.word2clusters('/Users/Henrik/Downloads/test/text8', '/Users/Henrik/Downloads/test/text8-clusters.txt', 100, verbose=True)