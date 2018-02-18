__author__ = 'talhaahsan and benpankow'
from newspaper import Article as newspaperArticle

class Article:

    def __init__(self, rssentry):
        self.link = rssentry.link
        self.newspaperFile = newspaperArticle(rssentry.link)
        self.newspaperFile.download()
        self.newspaperFile.parse()
        self.text = self.newspaperFile.text

