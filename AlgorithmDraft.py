__author__ = 'talhaahsan'
import math
import re
import operator #temp for testing
from nltk.corpus import stopwords
from newspaper import Article as nArticle

stopwords = set(stopwords.words('english'))
globalWordCloud = ['Tags']
categories = ['Country or Subject insert here']

class Country:
    # Contains total words in articles inside. Total word count inside China folder, and more!
    totalWordCount = 0
    countryFolderPath = "folderpath"
    # WordRate gives a probability out of 1000 words how many instances of the word which is the key will be present
    #wordRate and wordOccuranceCount are both maps with string keys, and integer values. wordRate / 1000 * totalWordCount = the number of times the word has been seen
    wordRate = {}
    # We need to make sure that wordRate's keys are part of wordCloud, so we need a method to sync these repeatedly.
    wordOccuranceCount = {}
    # Where wordRate[key] = wordTotalCount[key] * 1000 / totalWordCount

class Article:
    # do something to create article word rate, simply create a dictionary with toal occurences, and word count, and from there calculate per keyword the word rate
    articleWordRate = {}
    
    def __init__ (self, url, text):
        self.articleURL = url
        self.articleBody = text

def updateClouds(article, country):
    # takes article keywords, and adds them to the grand list if necessary
    testwords = article.articleWordRate.keys()
    for word in testwords:
        if word not in globalWordCloud:
            globalWordCloud.append(word)
    # syncs total word cloud with country setups, this then ensures that each keyword in the article will be globally available, and also the country will have it before a test occurs.
    for word in globalWordCloud:
        if word not in country.wordRate.keys():
            country.wordRate[word] = 0
    return

# compares article rate with country rate, returning the distance
def distance(article, country):
    # make sure errors are minimized
    updateClouds(article, country)

    articleWords = article.articleWordRate.keys()
    distancesquare = 0
    for key in articleWords:
        termdifference = country.wordRate[key] - article.articleWordRate[key]
        distancesquare += (termdifference ** 2)
    return math.sqrt(distancesquare)
	
# removes stop words, makes lowercase. returns a list of words in the article
def sanitize(text):
	# first, make lowercase
	text = text.lower()
	# make a list of every word
	list = re.compile('\w+').findall(text)
	# lambda function that removes all stopwords
	list = filter(lambda w: not w in stopwords, list)
	return list

def calculateWordRate(article):
    words = sanitize(article.articleBody)
    articleOccuranceCount = {}
    totalWords = 0
    for word in words:
        if word not in articleOccuranceCount.keys():
            articleOccuranceCount[word] = 0
            
        articleOccuranceCount[word] = articleOccuranceCount[word] + 1
        totalWords += 1

    for word in articleOccuranceCount.keys(): 
        article.articleWordRate[word] = (articleOccuranceCount[word] * 1000) / totalWords

def mergeText(article, country):
    wordsToAdd = sanitize(article.articleBody)
    for word in wordsToAdd:
        country.wordOccuranceCount[word] = country.wordOccuranceCount[word] + 1 #Can i just do += 1? ++ won't work
        country.totalWordCount += 1
    for key in country.wordOccuranceCount.keys():
        country.wordRate[key] = country.wordOccuranceCount[key] * 1000 / country.totalWordCount
    return
	
if __name__ == '__main__':
    url = 'http://www.nytimes.com/2015/09/02/us/politics/ben-carson-advancing-in-polls-is-a-sharp-contrast-to-donald-trump.html'
    narticle = nArticle(url)
    narticle.download()
    narticle.parse()
    text = narticle.text
    
    article = Article(url, text)
    calculateWordRate(article)
    sortedWordRate = sorted(article.articleWordRate.items(), key=operator.itemgetter(1))
    for item in sortedWordRate:
        print(item)