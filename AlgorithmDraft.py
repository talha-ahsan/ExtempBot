__author__ = 'talhaahsan and benpankow'
import math
import re
import operator #temp for testing
import pickle
from nltk.corpus import stopwords
from newspaper import Article as nArticle

nextArticleID = 1

stopwords = set(stopwords.words('english'))
globalWordCloud = ['Tags']

categories = []

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

    # add an article's word data to the category's word data
    def addArticle(self, article):
        self.articles.append(article)
        # update the occurrence count for the category as a whole, adding the occurrences from the article
        for word in article.articleOccuranceCount:
            if word not in self.wordOccuranceCount:
                self.wordOccuranceCount[word] = 0
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
            
    def save(self):
        ids = []
        for article in self.articles:
            article.save()
            ids.append(article.id)
            
        saveFile = open(self.name + '.xcat', 'wb')
        data = [self.name, self.totalWordCount, self.categoryFolderPath, self.wordRate, self.wordOccuranceCount, ids]
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
        ids = data[5]
        for id in ids:
            article = Article.loadFromFile(id)
            cat.articles.append(article)
            id = id

        return cat
        

class Article:
    id = 0
    articleWordRate = {}
    articleOccuranceCount = {}
    articleURL = ""
    articleBody = ""

    def __init__ (self, id, url, text):
        self.id = id
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
    
    def save(self):
        saveFile = open('article' + str(self.id) + '.xart', 'wb')
        data = [self.id, self.articleWordRate, self.articleOccuranceCount, self.articleURL, self.articleBody]
        pickle.dump(data, saveFile)
        saveFile.close()

    @classmethod
    def loadFromFile(cls, id):
        loadFile = open('article' + str(id) + '.xart', 'rb')
        data = pickle.load(loadFile)
        loadFile.close()
        art = cls(id, data[3], data[4])
        art.articleWordRate = data[1]
        art.articleOccuranceCount = data[2]

        return art

#Syncs article text with both global word cloud and the category's word cloud to make sure both have all possible keywords
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
    
#Loads a variety of misc information, right now just the next article ID
def loadMisc():
    global nextArticleID
    saveFile = open('misc.xdat', 'rb')
    miscItems = pickle.load(saveFile)
    nextArticleID = miscItems[0]
    saveFile.close()
    return
    
#Saves a variety of misc information, right now just the next article ID
def saveMisc():
    list = [ nextArticleID ]
    saveFile = open('misc.xdat', 'wb')
    pickle.dump(list, saveFile)
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
    
    
def getNextArticleID():
    global nextArticleID
    nextArticleID += 1
    return nextArticleID

def testMethod():
    loadMisc()
    loadCategories()
    
    print("\n" + categories[0].name + "\n-Word Rate for 'republican': " + str(categories[0].wordRate["republican"]) + "/1000\n-Word Occurance for 'republican': " + str(categories[0].wordOccuranceCount["republican"]) + "/" + str(categories[0].totalWordCount))
    print("\nArticle no." + str(categories[0].articles[0].id) + "\n-Word Rate for 'republican': " + str(categories[0].articles[0].articleWordRate["republican"]) + "/1000\n-Word Occurance for 'republican': " + str(categories[0].articles[0].articleOccuranceCount["republican"]) + "\n")

    saveCategories()
    saveMisc()

def testMethod2():
    cat = Category("2016 Election", "")
    # create a newspaper Article object
    url = 'http://www.nytimes.com/2015/09/02/us/politics/cnn-alters-debate-criteria-which-could-help-carly-fiorina.html'
    narticle = nArticle(url)
    # download and parse the article (this gives us the clean text and info like author, date etc)
    narticle.download()
    narticle.parse()
    text = narticle.text

    # create an article object and calculate the word rate
    id = getNextArticleID()
    article = Article(id, url, text)
    article.calculateWordRate()
    sortedWordRate = sorted(article.articleWordRate.items(), key=operator.itemgetter(1))
    cat.addArticle(article)
    categories.append(cat)

if __name__ == '__main__':
    testMethod()