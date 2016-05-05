# IECCS
Is global warming caused by humans? The Consensus Project collected thousands of peer-reviewed publications related to global warming and manually labeled them as "Skeptic", "Neutral" or "Pro" (www.skepticalscience.com/tcp.php). They arguably concluded that 97% of the papers upto 2011 agree that global warming is real and due to human factors. Their data is publicly available and can be explored through a nice online visualisation: www.skepticalscience.com/tcp.php
  
What happened after 2011? We don't know, because there is no data! Labelling thousands of articles by hand is expensive and time consuming. However, labelling documents is a task that can be automated. 
It is called "document classification" in Natural Language Processing (NLP) and it is typically implemented using supervised classification, a machine learning technique. One part of this project is therefore building a document classification system, trained on the data from the Consensus Project, predicting the labels "Skeptic", "Neutral" or "Pro". 
This task has in fact a lot in common with another popular NLP task: opinion mining/sentiment analysis. 

Such a classifier requires features extracted from the text. How do we get the abstracts, or even better, the full-text of articles? T
his involves searching for articles (search &amp; information retrieval), downloading the source documents (crawling websites) and filtering out the text (text extraction from HTML or PDF). Data collection therefore forms a second major part of this project. 

The third part of this project concerns interactive visualisation. 
The visualisation mentioned above is nice, but so much more is possible. Provided that we can also extract the affiliation of authors, we can plot the distribution of climate skepticism on a world map, contrasting e.g. USA vs. Europe. What if we take the impact factors of journals into account? 
Is there more or less skepticism in high-impact journals (e.g. Nature, Science) then in low-impact journals (Chinese Journal of Oceanology and Limnology). Many interesting options to explore (for some inspiration, see www.creativebloq.com/design-tools/data-visualization-712402).

# ieccs-server
https://github.com/djick/ieccs-server
