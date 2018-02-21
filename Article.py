__author__ = 'talhaahsan and benpankow'
from newspaper import Article as newspaperArticle

class Article:

    def __init__(self, rssentry):
        self.link = rssentry.link
        self.newspaperFile = newspaperArticle(rssentry.link)
        self.newspaperFile.download()
        self.newspaperFile.parse()
        self.newspaperFile.nlp()
        self.keywords = self.newspaperFile.keywords
        self.text = self.newspaperFile.text
        self.text = self.text.lower()


    def makeWordDict(self):
        self.wordDict = {}
        for word in self.text:
            print(word)


    def getWordDict(self):
        return self.wordDict

url = "https://www.nytimes.com/2018/02/21/us/florida-gun-control-republicans.html"
article = newspaperArticle(url)
article.download()
article.parse()
article.nlp()
print(article.text)
print(article.keywords)