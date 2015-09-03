__author__ = 'talhaahsan'
import math
import re
import operator #temp for testing
import pickle
from nltk.corpus import stopwords
from newspaper import Article as nArticle
import Category.py

class Article:
    id = 0
    articleWordRate = {}
    articleOccuranceCount = {}
    articleURL = ""
    articleBody = ""

    def __init__ (self, url, text):
        self.articleURL = url
        self.articleBody = text

    # counts occurrence of each word in the article (this number is saved for category calculation later) and used to determine the word rate
    def calculateWordRate(self):
        # get a list of words in the article
        words = sanitize(self.articleBody)

        totalWords = 0
        for word in words:
        # ignore all stopwords
            if word not in stopwords:
                if word not in self.articleOccuranceCount.keys():
                    self.articleOccuranceCount[word] = 0
                # count each word and count the total amount of words
                self.articleOccuranceCount[word] = self.articleOccuranceCount[word] + 1
                totalWords += 1
        # calculate the rate
        for word in self.articleOccuranceCount.keys():
            self.articleWordRate[word] = (self.articleOccuranceCount[word] * 1000) / totalWords