__author__ = 'talhaahsan'

totalWordCloud = ['China', 'Russia', 'Economics', 'Myanmar', 'Japan', 'Shinzo', 'Abe', 'Washington', 'Abbot', 'Shell', 'BP', 'Intel', 'So on']
categories = ['China', 'Russia', 'Japan', 'blagh']

class Country:
    #Contains total words in articles inside. Total word count inside China folder, and more!
    totalWordCount = 52
    wordCloud = ['China', 'Japan', 'Economics', 'So On']
    #WrodRate gives a probability out of 1000 words how many instances of the word which is the key will be present
    wordRate = {'China': 120, 'Japan': 50, 'Economics': 350}
    #We need to make sure that wordRate's keys are part of wordCloud, so we need a method to sync these repeatedly.

class Article:
    articleURL = 'www.google.com'
    articleBody = 'This is the article"s body. Don"t hate, just procreate'
    articleBodyScrubbed = 'This is a cleaned up version of the article. I am too lazy to clean it atm so ignore this'
    articleWordRate = {'word': 12}


