__author__ = 'talhaahsan and benpankow'
import math
import re
import operator #temp for testing
import pickle
from nltk.corpus import stopwords
from newspaper import Article as nArticle
import Category
import Article

stopwords = set(stopwords.words('english'))
globalWordCloud = ['Tags']

categories = []

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


#initial calibration function for a category, takes the articles inside and sorts them
def categoryCalibrate(category):
    #TODO: create a list of articles currently in the folder using the folder path.

    #TODO: run through the list, converting each article pdf file into an html file
        #TODO: feed the article into newspaper to get the body text
        #TODO: for each article after conversion, run through the text so that it can increment or update the wordOccuranceCount dict
        #TODO: implement this https://www.binpress.com/tutorial/manipulating-pdfs-with-python/167
    return

def testMethod():
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
