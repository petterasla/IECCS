#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Fix path for use in terminal ###
import sys
import os
sys.path.append(os.path.abspath(__file__ + "/../../../"))
###

import time
start_time = time.time()

import System.DataProcessing.process_data as ptd
import System.DataProcessing.process_meta_data as meta
import System.Utilities.helper_feature as helper

from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.metrics import classification_report
from sklearn.cross_validation import cross_val_predict, StratifiedKFold
from sklearn.metrics import fbeta_score
from sklearn.svm import LinearSVC
from sklearn.preprocessing import FunctionTransformer
import math
import pandas as pd

# ***** SETTINGS   *****
use_upsample = 0
use_downsample = 0

downsample_rate_favor = 0.3
downsample_rate_none  = 0.3

strength = 'soft'

# ***** LOAD DATA   *****
if use_downsample:
    data = ptd.getTrainingData()
    sub_none = ptd.getDownsample2_0(data, "NONE", strength, downsample_rate_none)
    sub_favor = ptd.getDownsample2_0(data, "FAVOR", strength, downsample_rate_favor)
    against = data[data.Stance == "AGAINST"]

    data = pd.concat([sub_favor, sub_none, against])

else:
    data = ptd.getTrainingData()

if use_upsample:
    data = pd.concat([data, data[data.Stance == "AGAINST"]])

print "None: ", len(data[data.Stance == "NONE"])
print "Against: ", len(data[data.Stance == "AGAINST"])
print "FAVOR: ", len(data[data.Stance == "FAVOR"])

cv = StratifiedKFold(data.Stance, n_folds=10, shuffle=True, random_state=1)


# List of feature keys:
# ["id-idf", "count-vect", "year-feat", "category-feat", "language-feat"]

feature_keys = ["year-feat"]
# NOTE: can also use helper.getFeatureKeys() and set list in getFeatureKeys() method.
#data2 = pd.DataFrame(data).set_index("Abstract")
ind = -1
for i, ab in enumerate(data.Abstract.tolist()):
    if ab.startswith("One analysis considers how to allocate effort"):
        print("index {}".format(i))
        ind = i

#print data.iloc[ind].Abstract
#print data.iloc[ind].Id
# id = 2762
#a = "One analysis considers how to allocate effort within a portfolio of mitigation and adaptation alternatives in addressing the possible catastrophic impacts of climate change. 7 The most recent IPCC Working Group II report suggests a possible impact threshold somewhere in the range of a global average temperature change between 2 and 3°C| 8 above which impacts are likely to be more serious and widespread globally. It also is possible that| if the rate of increase in GHG emissions is not moderated in the coming decades| the likelihood of abrupt climate changes will increase| such as a change in the ocean chemistry that causes the Atlantic Gulf Stream to warm| which could indeed be catastrophic for Northwestern Europe. The analysis indicates a need for additional attention to several characteristics of the climate-societal system when integrating mitigation and adaptation strategies| such as the assumed level of cooperation across countries in mitigation efforts and the strength of the interaction across the response measures. As an example of interaction effects| if new agricultural cultivation practices are pursued to sequester carbon more fully (a type of mitigation effort)| the rotation length and choice of agricultural crop could differ from the rotation length and crop most accommodating to changing climatic conditions (types of adaptation strategies). Moreover| the analysis indicates that mitigation becomes less effective as the time horizon for catastrophic impact approaches| because the benefits of mitigation take some time to be realized| making collective adaptation increasingly important by default. In other words| mitigation is inherently anticipatory rather than reactive| while the ability of adaptation to handle possible impact damages through near-term (or after-the-fact) reaction is limited in many cases. Preliminary findings suggest that comparisons of adaptation and mitigation strategies are dependent on geographic scale as well as on the assumed magnitude of climate change. As illustrated conceptually by the solid lines in Figure 2 on page 35| mitigation pathways show higher net benefits at a global scale than a local scale because so many benefits from mitigation investments are external to a local area. By contrast| adaptation pathways show higher net benefits at a local scale| at least in industrialized countries| because significant potential impacts at a global scale are difficult to address through adaptation| such as problems of low-lying coastal areas with sea-level rise. One implication of this pattern is that comparisons of possible responses at a global scale will tend to favor mitigation| while comparisons at the scale of a region within an industrialized country will tend to favor adaptation as the approach that makes the most economic sense for the area itself. This suggests challenges in assuring that mitigation gets a substantial share of the total investment by democratic| industrialized countries where localities have a say in climate change responses. Comparisons| however| also depend on the magnitude and rate of climate change assumed in modeling scenarios. If the solid lines represent moderate change| the dotted lines in the figure represent more substantial climate change. In that case| the net benefits of mitigation pathways tend to rise and the net benefits of adaptation pathways tend to drop. The reason is that the ability of adaptation investments to accommodate higher impacts is relatively smaller| increasing the relative value of mitigation in avoiding impact costs. This strongly suggests that mitigation and adaptation are not necessarily competitors in climate change impact response strategies. In many cases| they are instead complements. If mitigation is successful in keeping climate change impacts to a moderate level| then adaptation can handle a larger share of the resulting impacts.".decode("utf-8")
#print data2.loc[a].Id
#exit()
# Select classifiers to use
classifiers = [
    LinearSVC(C=0.00017782794100389227),
    #SVC(decision_function_shape='ovo', kernel='linear', shrinking=True)
    #MultinomialNB(alpha=0.5)
]


# ***** TRAIN CLASSIFIERS   *****
for clf in classifiers:
    print 80 * "="
    print clf
    print 80 * "="

    # Use optimized parameters from grid_search_improved
    pipeline = Pipeline([
        ('features', FeatureUnion(helper.getFeatures(feature_keys))),
        ('clf', clf)
    ])

    pred_stances = cross_val_predict(pipeline, data.Abstract, data.Stance, cv=cv)

    print classification_report(data.Stance, pred_stances, digits=4)

    macro_f = fbeta_score(data.Stance, pred_stances, 1.0,
                          labels=['AGAINST', 'FAVOR', 'NONE'],
                          average='macro')

    print 'macro-average of F-score(FAVOR), F-score(AGAINST) and F-score(NONE): {:.4f}\n'.format(macro_f)


print("Time used {:.1f} in minutes ".format((time.time()-start_time)/60.0))

