import json

with open("abstracts_with_meta", "r") as articleJson:
    articles = json.load(articleJson)
    articleJson.close()

counter = 0
for article in articles:

    #if article["abstract"] != "[No abstract available]":
    #   counter += 1

    if article["Status"]["isMetaTitleEqualToOriginal"] == "True":
        counter += 1

print counter