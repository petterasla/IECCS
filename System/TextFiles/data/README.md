DATA:
In this folder you will find the TCP data. It can be found in four 
different files: original (all), a trainig set, a validation set, and a 
test set. The splits are genrated by DataProcessing.split_data. 

All data splits are stratified and splitted randomly where each sample 
only occurs once. The test set consist of 25% of the data, validation 
set of 22.5% and the rest is used in the training set.