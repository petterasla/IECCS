import os
import sys
sys.path.append(os.path.abspath(__file__ + "/../../"))

import re
import pandas as pd

data = pd.read_csv('../../TextFiles/data/tcp_abstracts.txt', sep=',')

file = open("training_text.txt", 'w')
for abstract in data.Abstract:
    clean_abstract = re.sub('[^a-zA-Z \n]', ' ', abstract)
    file.write(str(clean_abstract) + "\t")

file.close()