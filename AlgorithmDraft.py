__author__ = 'talhaahsan'
import math
import re
globalWordCloud = ['China', 'Russia', 'Economics', 'Myanmar', 'Japan', 'Shinzo', 'Abe', 'Washington', 'Abbot', 'Shell', 'BP', 'Intel', 'So on']
categories = ['China', 'Russia', 'Japan', 'blagh']

class Country:
    # Contains total words in articles inside. Total word count inside China folder, and more!
    totalWordCount = 52
    countryFolderPath = "C:/Users/Ben/Collectionofcompletelysafeforworkstuff/notsketchyatallfolder/Extemp/IX/Asia/China"
    # WordRate gives a probability out of 1000 words how many instances of the word which is the key will be present
    wordRate = {'China': 120, 'Japan': 50, 'Economics': 350}
    # We need to make sure that wordRate's keys are part of wordCloud, so we need a method to sync these repeatedly.
    wordOccuranceCount = {'China': 1500, 'Japan': 5000, 'ETC': 120}
    # Where wordRate[key] = wordTotalCount[key] * 1000 / totalWordCount

class Article:
    articleURL = 'www.google.com'
    articleBody = 'This is the article"s body. Don"t hate, just procreate'
    articleBodyScrubbed = 'This is a cleaned up version of the article. I am too lazy to clean it atm so ignore this'
    # do something to create article word rate, simply create a dictionary with toal occurences, and word count, and from there calculate per keyword the word rate
    articleWordRate = {'word': 12}

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

# TODO: create an article to country decider off the distance function for each possible country. We'd need to create a ste of countrys etc. eww.
def getWords(text):
    return re.compile('\w+').findall(text)

def mergeText(article, country):
    wordsToAdd = getWords(article.articleBodyScrubbed)
    for word in wordsToAdd:
        country.wordOccuranceCount[word] = country.wordOccuranceCount[word] + 1 #Can i just do += 1? ++ won't work
        country.totalWordCount += 1
    for key in country.wordOccuranceCount.keys():
        country.wordRate[key] = country.wordOccuranceCount[key] * 1000 / country.totalWordCount
    return
