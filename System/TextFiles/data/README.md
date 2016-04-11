DATA:
In this folder you will find the TCP data, including meta data and related record associated with TCP data. 
It can be found in four different files: original (all), a trainig set, a validation set, and a 
test set. The splits are genrated by DataProcessing.split_data. 

All data splits are stratified and splitted randomly where each sample 
only occurs once. The test set consist of 25% of the data, validation 
set of 22.5% and the rest is used in the training set.

It was observed 10-04-2016 that tcp_abstracts.txt contained two
identical samples with IDs=[10320, 11546]. This created problems
when working with pandas Dataframe (among other), so sample with
ID = 11546 was removed from the following files:
- tcp_abstracts.txt
- tcp_test.csv

Information about the sample removed is: 
11546,2010,2,4,CLIMATE CHANGE| AGRICULTURAL INSURANCE AND GOVERNMENTAL SUPPORT,Global warming has contributed to a greater frequency of extreme weather events represented by heat waves| severe drought or floods. Agriculture is exposed to such events more than many other economic sectors. Agriculture is not only one of the most exposed sector to climate change triggered risks| but it also faces sever difficulties in addressing those risks. The paper aims to provide an argument for more intense governmental involvement in agricultural risk management| based upon several factual and theoretical reasons. There were identified some theoretical reasons (market failure| co-responsibility| economics) that support a better governmental intervention through an insurance scheme with governmental support. Romania's agricultural insurance market is in its infancy| but there are signals that competition could lower premiums below the technical level. Governmental measures| such as subsidized credits and damage scheme for natural hazards produced losses impacted significantly the agricultural insurance market. However| delayed payments lowered farmers' trust in insurance as a risk management option.