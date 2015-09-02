__author__ = 'talhaahsan'
import math
import re
import operator #temp for testing
import pickle
from nltk.corpus import stopwords
from newspaper import Article as nArticle

stopwords = set(stopwords.words('english'))
globalWordCloud = ['Tags']

class Category:
    name = ""
    # Contains total words in articles inside. Total word count inside China folder, and more!
    totalWordCount = 0
    categoryFolderPath = "folderpath"
    #wordRate and wordOccuranceCount are both maps with string keys, and integer values. wordRate / 1000 * totalWordCount = the number of times the word has been seen
    wordRate = {}
    wordOccuranceCount = {}
    # Where wordRate[key] = wordTotalCount[key] * 1000 / totalWordCount
    
    def __init__ (self, name, path):
        self.name = name
        self.categoryFolderPath = path
    
    def save(self):
        saveFile = open(self.name + '.xcat', 'wb')
        data = [self.name, self.totalWordCount, self.categoryFolderPath, self.wordRate, self.wordOccuranceCount]
        pickle.dump(data, saveFile)
        saveFile.close()

    @classmethod
    def loadFromFile(cls, name):
        loadFile = open(name + '.xcat', 'rb')
        data = pickle.load(loadFile)
        loadFile.close()
        cat = cls(data[0], data[2])
        cat.totalWordCount = data[1]
        cat.wordRate = data[3]
        cat.wordOccuranceCount = data[4]
        return cat

categories = []
	
class Article:
    articleWordRate = {}
    articleOccuranceCount = {}
    articleURL = ""
    articleBody = ""

    def __init__ (self, url, text):
        self.articleURL = url
        self.articleBody = text

		
def updateClouds(article, category):
    # takes article keywords, and adds them to the grand list if necessary
    testwords = article.articleWordRate.keys()
    for word in testwords:
        if word not in globalWordCloud:
            globalWordCloud.append(word)
    # syncs total word cloud with category setups, this then ensures that each keyword in the article will be globally available, and also the category will have it before a test occurs.
    for word in globalWordCloud:
        if word not in category.wordRate.keys():
            category.wordRate[word] = 0
    return

	
# compares article rate with category rate, returning the distance
def distance(article, category):
    # make sure errors are minimized
    updateClouds(article, category)

    articleWords = article.articleWordRate.keys()
    distancesquare = 0
    for key in articleWords:
        termdifference = category.wordRate[key] - article.articleWordRate[key]
        distancesquare += (termdifference ** 2)
    return math.sqrt(distancesquare)
	
	
# makes lowercase. returns a list of words in the article
def sanitize(text):
    # first, make lowercase
    text = text.lower()
    # make a list of every word
    list = re.compile('\w+').findall(text)
    return list

	
# counts occurrence of each word in the article (this number is saved for category calculation later) and used to determine the word rate
def calculateWordRate(article):
	# get a list of words in the article
    words = sanitize(article.articleBody)
	
    totalWords = 0
    for word in words:
	# ignore all stopwords
        if word not in stopwords:
            if word not in article.articleOccuranceCount.keys():
                article.articleOccuranceCount[word] = 0
			
	    # count each word and count the total amount of words
            article.articleOccuranceCount[word] = article.articleOccuranceCount[word] + 1
            totalWords += 1
			
	# calculate the rate
    for word in article.articleOccuranceCount.keys(): 
        article.articleWordRate[word] = (article.articleOccuranceCount[word] * 1000) / totalWords

		
# add an article's word data to the category's word data
def mergeWords(article, category):
	# update the occurrence count for the category as a whole, adding the occurrences from the article
    for word in article.articleOccuranceCount:
        category.wordOccuranceCount[word] = category.wordOccuranceCount[word] + article.articleOccuranceCount[word] #Can i just do += 1? ++ won't work
        category.totalWordCount += 1
	# now update the word rate
    for key in category.wordOccuranceCount.keys():
        category.wordRate[key] = category.wordOccuranceCount[key] * 1000 / category.totalWordCount
    return


# saves all categories
def saveCategories():
    names = []
    for category in categories:
        category.save()
        names.append(category.name)
        print('Now saving ' + category.name + '.xcat...')
    saveFile = open('categories.xdat', 'wb')
    pickle.dump(names, saveFile)
    saveFile.close()

# loads all categories
def loadCategories():
    saveFile = open('categories.xdat', 'rb')
    catNames = pickle.load(saveFile)
    saveFile.close()
    for catName in catNames:
        cat = Category.loadFromFile(catName)
        categories.append(cat)
	
if __name__ == '__main__':
    loadCategories()
    saveCategories()
    
    # create a newspaper Article object
    url = 'http://www.nytimes.com/2015/09/02/us/politics/cnn-alters-debate-criteria-which-could-help-carly-fiorina.html'
    narticle = nArticle(url)
    # download and parse the article (this gives us the clean text and info like author, date etc)
    narticle.download()
    narticle.parse()
    text = narticle.text
    
    # create an article object and calculate the word rate
    article = Article(url, text)
    calculateWordRate(article)
    sortedWordRate = sorted(article.articleWordRate.items(), key=operator.itemgetter(1))
    for item in sortedWordRate:
        print(item)
	
