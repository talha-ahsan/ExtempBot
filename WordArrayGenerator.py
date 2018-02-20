import pickle

# This generator essentially takes in a BUNCH of special words that we are interested in searching for in the article text
# The goal is an output file that is the pickled dictionary where each word is a key, and the value at that key is the numberof times
# that word is shown in the article. This then is unpickled by the Article.py Article object to hopefully save time

wordCountDict = {}
wordsOfInterest = [
    "correctional"
]