__author__ = 'talhaahsan'
import math

totalWordCloud = ['China', 'Russia', 'Economics', 'Myanmar', 'Japan', 'Shinzo', 'Abe', 'Washington', 'Abbot', 'Shell', 'BP', 'Intel', 'So on']
categories = ['China', 'Russia', 'Japan', 'blagh']

class Country:
    # Contains total words in articles inside. Total word count inside China folder, and more!
    totalWordCount = 52
    countryFolderPath = "C:/Users/Ben/Collectionofcompletelysafeforworkstuff/notsketchyatallfolder/Extemp/IX/Asia/China"
    wordCloud = ['China', 'Japan', 'Economics', 'So On']
    # WordRate gives a probability out of 1000 words how many instances of the word which is the key will be present
    wordRate = {'China': 120, 'Japan': 50, 'Economics': 350}
    # We need to make sure that wordRate's keys are part of wordCloud, so we need a method to sync these repeatedly.
    wordTotalCount = {'China': 1500, 'Japan': 5000, 'ETC': 120}
    # Where wordRate[key] = wordTotalCount[key] * 1000 / totalWordCount

class Article:
    articleURL = 'www.google.com'
    articleBody = 'This is the article"s body. Don"t hate, just procreate'
    articleBodyScrubbed = 'This is a cleaned up version of the article. I am too lazy to clean it atm so ignore this'
    # do something to create article word rate, simply create a dictionary with toal occurences, and word count, and from there calculate per keyword the word rate
    articleWordRate = {'word': 12}

# Ensures that the country has each item in the word cloud as also a key in the word rate.
def updateCountryLists(country):
    # Ensure the word cloud holds all of the words in the word rate
    words = country.wordRate.keys()
    for word in country.wordCloud:
        if word not in words:
            country.wordRate[word] = 0
    # Ensure the word rate list holds all the words in the word cloud
    for word in words:
        if word not in country.wordCloud:
            country.wordCloud.append(word)


def updateClouds(article, country):
    # takes article keywords, and adds them to the grand list if necessary
    testwords = article.articleWordRate.keys()
    for word in testwords:
        if word not in totalWordCloud:
            totalWordCloud.append(word)
    # syncs total word cloud with country setups, this then ensures that each keyword in the article will be globally available, and also the country will have it before a test occurs.
    for word in totalWordCloud:
        if word not in country.wordCloud:
            country.wordCloud.append(word)
            country.wordRate[word] = 0

# compares article rate with country rate, returning the distance
def distance(article, country):
    # make sure errors are minimized
    updateCountryLists(country)
    updateClouds(article, country)

    articleWords = article.articleWordRate.keys()
    distancesquare = 0
    for key in articleWords:
        termdifference = country.wordRate[key] - article.articleWordRate[key]
        distancesquare += (termdifference ** 2)
    return math.sqrt(distancesquare)

# TODO: create an article to country decider off the distance function for each possible country. We'd need to create a ste of countrys etc. eww.
