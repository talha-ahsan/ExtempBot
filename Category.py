__author__ = 'talhaahsan and benpankow'
import math
import re
import operator #temp for testing
import pickle
from nltk.corpus import stopwords
from newspaper import Article as nArticle
import Article

class Category:
    name = ""
    # Contains total words in articles inside. Total word count inside China folder, and more!
    totalWordCount = 0
    categoryFolderPath = "folderpath"
    #wordRate and wordOccuranceCount are both maps with string keys, and integer values. wordRate / 1000 * totalWordCount = the number of times the word has been seen
    wordRate = {}
    wordOccuranceCount = {}
    # Where wordRate[key] = wordOccuranceCount[key] * 1000 / totalWordCount

    # All the articles contained in this category
    articles = []

    def __init__ (self, name, path):
        self.name = name
        self.categoryFolderPath = path

    def save(self):
        ids = []
        for article in articles:
            # article.save() TODO
            ids.append(article.id)

        saveFile = open(self.name + '.xcat', 'wb')
        data = [self.name, self.totalWordCount, self.categoryFolderPath, self.wordRate, self.wordOccuranceCount, ids]
        pickle.dump(data, saveFile)
        saveFile.close()

    # add an article's word data to the category's word data
    def addArticle(self, article):
        articles.append(article)
        # update the occurrence count for the category as a whole, adding the occurrences from the article
        for word in article.articleOccuranceCount:
            self.wordOccuranceCount[word] = self.wordOccuranceCount[word] + article.articleOccuranceCount[word]
            self.totalWordCount += article.articleOccuranceCount[word]
        # now update the word rate
        for key in self.wordOccuranceCount.keys():
            self.wordRate[key] = self.wordOccuranceCount[key] * 1000 / self.totalWordCount

    # remove an article from this category
    def removeArticle(self, article):
        articles.remove(article)
        # update the occurrence count for the category as a whole, subtracting the occurrences from the article
        for word in article.articleOccuranceCount:
            self.wordOccuranceCount[word] = self.wordOccuranceCount[word] - article.articleOccuranceCount[word]
            self.totalWordCount -= article.articleOccuranceCount[word]
        # now update the word rate
        for key in self.wordOccuranceCount.keys():
            self.wordRate[key] = self.wordOccuranceCount[key] * 1000 / self.totalWordCount

    @classmethod
    def loadFromFile(cls, name):
        loadFile = open(name + '.xcat', 'rb')
        data = pickle.load(loadFile)
        loadFile.close()
        cat = cls(data[0], data[2])
        cat.totalWordCount = data[1]
        cat.wordRate = data[3]
        cat.wordOccuranceCount = data[4]
        ids = data[5]
        for id in ids:
            # article = Article.loadFromFile(id)
            # cat.articles.append(article)
            id = id

        return cat