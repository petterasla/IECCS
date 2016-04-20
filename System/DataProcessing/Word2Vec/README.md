*System error is resolved by running training the code on server (ocean).*

This goes for:
    - train.py
    - create_word_vectors.py

Order to perform operations (if new data):
- run create_training_data.py 
- run train.py
- run create_word_vectors.py
- run run create_all_word2vec_vecs.py

Usage:
Just like glove vectors.
    
Explanation of files:
- training_text.txt consists of all abstract where special characters 
and numbers have been removed.
- training_text_vectors.txt consists of the word vectors trained on 
training_text.txt.
- vectors.txt is word2vec vectors created using the data set text8.

- word2vec_tcp_abstracts.pkl are the features generated using the text8
data set.
- word2vec_tcp_tcp_abstracts.pkl are the features generated using the 
tcp abstracts.
