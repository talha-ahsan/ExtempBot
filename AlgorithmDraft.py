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

categories = []
	
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

#Loads all keywords from GlobalWordCloud
def loadKeywords():
    saveFile = open('keywords.xdat', 'rb')
    globalWordCloud = pickle.load(saveFile)
    saveFile.close()
    return

#Saves all keyworks from globalWordCloud to a file
def saveKeywords():
    keywords = globalWordCloud
    saveFile = open('keywords.xdat', 'wb')
    pickle.dump(keywords, saveFile)
    saveFile.close()
    return


#initial calibration function for a category, takes the articles inside and sorts them
def categoryCalibrate(category):
    #TODO: create a list of articles currently in the folder using the folder path.

    #TODO: run through the list, converting each article pdf file into an html file
        #TODO: feed the article into newspaper to get the body text
        #TODO: for each article after conversion, run through the text so that it can increment or update the wordOccuranceCount dict
        #TODO: implement this https://www.binpress.com/tutorial/manipulating-pdfs-with-python/167
    return


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
    article.calculateWordRate()
    sortedWordRate = sorted(article.articleWordRate.items(), key=operator.itemgetter(1))
    for item in sortedWordRate:
        print(item)
	
