DATA:
In this folder you will find the TCP data, including meta data and related record associated with TCP data. 
It can be found in four different files: original (all), a trainig set, a validation set, and a 
test set. The splits are genrated by DataProcessing.split_data. 

All data splits are stratified and splitted randomly where each sample 
only occurs once. The test set consist of 25% of the data, validation 
set of 22.5% and the rest is used in the training set.

It was observed 10-04-2016 that tcp_abstracts.txt contained two
identical samples with IDs=

[10320, 11546], [12148, 12839] 

This created problems when working with pandas Dataframe (among other), 
so sample with ID = 11546 and 12839 was removed from the following files:
- tcp_abstracts.txt
- tcp_test.csv

Information about the sample removed is: 
11546,2010,2,4,CLIMATE CHANGE| AGRICULTURAL INSURANCE AND GOVERNMENTAL SUPPORT,Global warming has contributed to a greater frequency of extreme weather events represented by heat waves| severe drought or floods. Agriculture is exposed to such events more than many other economic sectors. Agriculture is not only one of the most exposed sector to climate change triggered risks| but it also faces sever difficulties in addressing those risks. The paper aims to provide an argument for more intense governmental involvement in agricultural risk management| based upon several factual and theoretical reasons. There were identified some theoretical reasons (market failure| co-responsibility| economics) that support a better governmental intervention through an insurance scheme with governmental support. Romania's agricultural insurance market is in its infancy| but there are signals that competition could lower premiums below the technical level. Governmental measures| such as subsidized credits and damage scheme for natural hazards produced losses impacted significantly the agricultural insurance market. However| delayed payments lowered farmers' trust in insurance as a risk management option.
12839,2011,3,2,Smart film actuators using biomass plastic,This paper presents a novel smart film actuator based on the use of a biomass plastic as a piezoelectric film. Conventional polymeric smart sensors and actuators have been based upon synthetic piezoelectric polymer films such as PVDF. Almost all synthetic polymers are made from nearly depleted oil resources. In addition combustion of their materials releases carbon dioxide| thereby contributing to global warming. Thus at least two important sustainability principles are violated when employing synthetic polymers: avoiding depletable resources and avoiding ecosystem destruction. To overcome such problems| industrial plastic products made from synthetic polymers were developed to replace oil-based plastics with biomass plastics. This paper applies a biomass plastic with piezoelectricity such as poly-L-lactic acid (PLLA). As a result| PLLA film becomes a distributed parameter actuator per se| hence an environmentally conscious smart film actuator is developed. Firstly| this paper overviews the fundamental properties of piezoelectric synthetic polymers and biopolymers. The concept of carbon neutrality using biopolymers is mentioned. Then a two-dimensional modal actuator for exciting a specific structural mode is proposed. Furthermore| a biomass plastic-based cantilever beam with the capability of modal actuation is developed| the validity of the proposed smart film actuator based upon a biomass plastic being analytically as well as experimentally verified.

IF THIS HAPPENS AGAIN, REMEMBER TO DELETE IN "meta_data.json" and in the mongoDB too.. FML.
In MongoDB console, type this command (and remove #ID# with actual id):
db.Data_wos.remove({_id:#ID#} ,{justOne:1})