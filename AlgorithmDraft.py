__author__ = 'talhaahsan'
import math
import re
import operator #temp for testing
from nltk.corpus import stopwords
from newspaper import Article as nArticle

stopwords = set(stopwords.words('english'))
globalWordCloud = ['Tags']
categories = ['Country or subject here']


class Country:
    # Contains total words in articles inside. Total word count inside China folder, and more!
    totalWordCount = 0
    countryFolderPath = "folderpath"
    #wordRate and wordOccuranceCount are both maps with string keys, and integer values. wordRate / 1000 * totalWordCount = the number of times the word has been seen
    wordRate = {}
    wordOccuranceCount = {}
    # Where wordRate[key] = wordTotalCount[key] * 1000 / totalWordCount

	
class Article:
    # do something to create article word rate, simply create a dictionary with toal occurences, and word count, and from there calculate per keyword the word rate
    articleWordRate = {}
    articleOccuranceCount = {}

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

		
# add an article's word data to the country's word data
def mergeWords(article, country):
	# update the occurrence count for the country as a whole, adding the occurrences from the article
    for word in article.articleOccuranceCount:
        country.wordOccuranceCount[word] = country.wordOccuranceCount[word] + article.articleOccuranceCount[word] #Can i just do += 1? ++ won't work
        country.totalWordCount += 1
	# now update the word rate
    for key in country.wordOccuranceCount.keys():
        country.wordRate[key] = country.wordOccuranceCount[key] * 1000 / country.totalWordCount
    return
	
	
if __name__ == '__main__':
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
	
