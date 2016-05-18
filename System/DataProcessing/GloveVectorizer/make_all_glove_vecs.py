import os
import sys
sys.path.append(os.path.abspath(__file__ + "/../../"))

"""
This uses Glove word vectors (http://nlp.stanford.edu/projects/glove/)
to build vector representations of all abstracts.
It simply collects the Glove vectors for all words in an abstract and
sums them.
Requires python2 with Numpy, Pandas en sklearn
"""

from codecs import open
from cStringIO import StringIO
from glob import glob
from os.path import basename, splitext

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

data1 = pd.read_csv(open("../../TextFiles/data/tcp_abstracts.txt"))
data2 = pd.read_json(open("../../TextFiles/data/related_data_correct_v1.json"))
data = pd.concat([data1, data2])

# First establish the vocabulary of all abstracts.
# lowercase because Glove terms are lowercased
# remove stopword because their vectors are probably not very meaningful
vectorizer = CountVectorizer(binary=True, lowercase=True, stop_words='english',
                             decode_error='ignore')
vectorizer.fit(data.Abstract)
abstract_vocab = set(vectorizer.get_feature_names())

# base dir for local copies of Glove vectors for different corpora & dimensions
#base_dir = '/Volumes/My Passport/glove/glove.840B.300d.txt'

# glob pattern for Glove vectors
glove_fnames = ['/Volumes/My Passport/glove/glove.840B.300d.txt']#glob(base_dir + '/.txt')# + glob(base_dir + '/*/*.txt')

out_dir = '/Users/petterasla/Desktop/Skole/9. semester/In-Depth project/IECCS/System/DataProcessing/GloveVectorizer/finalVec'

# Read the Glove vectors Slurping the whole file with pd.read_cvs does not
# work as the table gets get truncated! Presumably because of some kind of
# memory problem. Hence the complicated approach below with a first pass
# through the Glove file to collect the required vectors in an buffer.
for fname in glove_fnames:
    print 'reading', fname
    buffer = StringIO()
    shared_vocab = []

    for line in open(fname, encoding='utf8'):
        term = line.split(' ', 1)[0]
        if term in abstract_vocab:
            shared_vocab.append(term)
            buffer.write(line.encode('utf8'))

    print '# shared:', len(shared_vocab)
    buffer.seek(0)
    glove_vecs = pd.read_csv(buffer, sep=' ', header=None, index_col=0)
    buffer.close()

    # get Glove vectors as numpy.array
    glove_vecs = glove_vecs.as_matrix()

    # vectorize our abstracts with this shared vocabulary
    vectorizer = CountVectorizer(binary=True, stop_words='english',
                                 vocabulary=shared_vocab, decode_error='ignore')
    abstract_vecs = vectorizer.fit_transform(data.Abstract)
    # convert sparse matrix to numpy.array (not needed?)
    abstract_vecs = np.squeeze(np.asarray(abstract_vecs.todense()))

    # take the dot product of the matrices,
    # which amounts to summing the Glove vectors for all terms in a abstract
    abstract_glove_vecs = abstract_vecs.dot(glove_vecs)
    print abstract_vecs.shape
    print glove_vecs.shape
    print abstract_glove_vecs.shape

    # save vector as DataFrame with abstracts as index
    abstract_glove_df = pd.DataFrame(abstract_glove_vecs, index=data.Abstract)
    out_fname = out_dir + '/' + splitext(basename(fname))[0] + '_tcp_abstracts.pkl'
    print 'writing', out_fname
    abstract_glove_df.to_pickle(out_fname)