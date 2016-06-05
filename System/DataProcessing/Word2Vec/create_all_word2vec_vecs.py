import os
import sys
sys.path.append(os.path.abspath(__file__ + "/../../"))

"""
This uses word2vec word vectors trained on the abstract data
to build vector representations of all abstracts.
It simply collects the word2vec vectors for all words in an abstract and
sums them.
Requires python2 with Numpy, Pandas en sklearn
"""

from codecs import open
from cStringIO import StringIO

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

data = pd.read_csv(open("../../TextFiles/data/tcp_abstracts.txt"))

# First establish the vocabulary of all abstracts.
# lowercase because Glove terms are lowercased
# remove stopword because their vectors are probably not very meaningful
vectorizer = CountVectorizer(binary=True, lowercase=True, stop_words='english',
                             decode_error='ignore')
vectorizer.fit(data.Abstract)
abstract_vocab = set(vectorizer.get_feature_names())

# base dir for local copies of Glove vectors for different corpora & dimensions
word2vec_file = '/Users/Henrik/Documents/Datateknikk/Prosjektoppgave/IECCS/System/DataProcessing/Word2Vec/training_text_vectors.txt'

out_dir = '/Users/Henrik/Documents/Datateknikk/Prosjektoppgave/IECCS/System/DataProcessing/Word2Vec/vectors'

# Read the Glove vectors Slurping the whole file with pd.read_cvs does not
# work as the table gets get truncated! Presumably because of some kind of
# memory problem. Hence the complicated approach below with a first pass
# through the Glove file to collect the required vectors in an buffer.
print 'reading', word2vec_file
buffer = StringIO()
shared_vocab = []

for line in open(word2vec_file, encoding='utf8'):
    term = line.split(' ', 1)[0]
    if term in abstract_vocab:
        shared_vocab.append(term)
        buffer.write(line.encode('utf8'))

print '# shared:', len(shared_vocab)
buffer.seek(0)
word2vec_vecs = pd.read_csv(buffer, sep=' ', header=None, index_col=0)
buffer.close()

# get Glove vectors as numpy.array
word2vec_vecs = word2vec_vecs.as_matrix()

# vectorize our abstracts with this shared vocabulary
vectorizer = CountVectorizer(binary=True, stop_words='english',
                             vocabulary=shared_vocab, decode_error='ignore')
abstract_vecs = vectorizer.fit_transform(data.Abstract)
# convert sparse matrix to numpy.array (not needed?)
abstract_vecs = np.squeeze(np.asarray(abstract_vecs.todense()))

# take the dot product of the matrices,
# which amounts to summing the Glove vectors for all terms in a abstract
abstract_word2vec_vecs = abstract_vecs.dot(word2vec_vecs)
print abstract_vecs.shape
print word2vec_vecs.shape
print abstract_word2vec_vecs.shape

# save vector as DataFrame with abstracts as index
abstract_word2vec_df = pd.DataFrame(abstract_word2vec_vecs, index=data.Abstract)
out_fname = out_dir + '/' + 'word2vec_tcp' + '_tcp_abstracts.pkl'
print 'writing', out_fname
abstract_word2vec_df.to_pickle(out_fname)