__author__ = 'talhaahsan and benpankow'
import feedparser
import queue

nytimes = ['http://rss.nytimes.com/services/xml/rss/nyt/World.xml',
           'http://rss.nytimes.com/services/xml/rss/nyt/Africa.xml',
           'http://rss.nytimes.com/services/xml/rss/nyt/Americas.xml',
           'http://rss.nytimes.com/services/xml/rss/nyt/AsiaPacific.xml',
           'http://rss.nytimes.com/services/xml/rss/nyt/Europe.xml',
           'http://rss.nytimes.com/services/xml/rss/nyt/MiddleEast.xml',
           'http://rss.nytimes.com/services/xml/rss/nyt/US.xml',
           'http://rss.nytimes.com/services/xml/rss/nyt/Education.xml',
           'http://rss.nytimes.com/services/xml/rss/nyt/Politics.xml',
           'http://rss.nytimes.com/services/xml/rss/nyt/Business.xml',
           'http://rss.nytimes.com/services/xml/rss/nyt/EnergyEnvironment.xml',
           'http://rss.nytimes.com/services/xml/rss/nyt/InternationalBusiness.xml',
           'http://rss.nytimes.com/services/xml/rss/nyt/SmallBusiness.xml',
           'http://rss.nytimes.com/services/xml/rss/nyt/Economy.xml',
           'http://rss.nytimes.com/services/xml/rss/nyt/MediaandAdvertising.xml',
           'http://rss.nytimes.com/services/xml/rss/nyt/YourMoney.xml',
           'http://rss.nytimes.com/services/xml/rss/nyt/Technology.xml',
           'http://bits.blogs.nytimes.com/feed/',
           'http://rss.nytimes.com/services/xml/rss/nyt/PersonalTech.xml',
           'http://rss.nytimes.com/services/xml/rss/nyt/Science.xml',
           'http://rss.nytimes.com/services/xml/rss/nyt/Environment.xml',
           'http://rss.nytimes.com/services/xml/rss/nyt/Health.xml',
           'http://rss.nytimes.com/services/xml/rss/nyt/Research.xml',
           'http://rss.nytimes.com/services/xml/rss/nyt/Nutrition.xml',
           'http://rss.nytimes.com/services/xml/rss/nyt/HealthCarePolicy.xml',
           'http://rss.nytimes.com/services/xml/rss/nyt/Views.xml']
wsj = ['http://www.wsj.com/xml/rss/3_7041.xml',
       'http://www.wsj.com/xml/rss/3_7085.xml',
       'http://www.wsj.com/xml/rss/3_7014.xml',
       'http://www.wsj.com/xml/rss/3_7031.xml',
       'http://www.wsj.com/xml/rss/3_7455.xml',
       'http://blogs.wsj.com/bankruptcy/feed/',
       'http://blogs.wsj.com/chinarealtime/feed/',
       'http://blogs.wsj.com/corruption-currents/feed/',
       'http://feeds.wsjonline.com/wsj/dailyfix/feed/',
       'http://blogs.wsj.com/wealth-manager/feed/',
       'http://blogs.wsj.com/health/feed/',
       'http://blogs.wsj.com/hong-kong/feed/',
       'http://blogs.wsj.com/indiarealtime/feed/',
       'http://blogs.wsj.com/japanrealtime/feed/',
       'http://blogs.wsj.com/korearealtime/feed/',
       'http://blogs.wsj.com/middleseat/feed/',
       'http://feeds.wsjonline.com/wsj/numbersguy/feed',
       'http://blogs.wsj.com/emergingeurope/feed/',
       'http://blogs.wsj.com/washwire/feed/']
washpo = ['http://feeds.washingtonpost.com/rss/politics',
          'http://feeds.washingtonpost.com/rss/local',
          'http://feeds.washingtonpost.com/rss/rss_grade-point',
          'https://www.washingtonpost.com/blogs/answer-sheet/feed/',
          'http://feeds.washingtonpost.com/rss/rss_house-divided',
          'http://feeds.washingtonpost.com/rss/national',
          'http://feeds.washingtonpost.com/rss/rss_speaking-of-science',
          'http://feeds.washingtonpost.com/rss/world']
bbc = ['http://feeds.bbci.co.uk/news/world/rss.xml',
       'http://feeds.bbci.co.uk/news/uk/rss.xml',
       'http://feeds.bbci.co.uk/news/business/rss.xml',
       'http://feeds.bbci.co.uk/news/politics/rss.xml',
       'http://feeds.bbci.co.uk/news/health/rss.xml',
       'http://feeds.bbci.co.uk/news/education/rss.xml',
       'http://feeds.bbci.co.uk/news/science_and_environment/rss.xml',
       'http://feeds.bbci.co.uk/news/technology/rss.xml',
       'http://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml',
       'http://feeds.bbci.co.uk/news/world/africa/rss.xml',
       'http://feeds.bbci.co.uk/news/world/asia/rss.xml',
       'http://feeds.bbci.co.uk/news/world/europe/rss.xml',
       'http://feeds.bbci.co.uk/news/world/latin_america/rss.xml',
       'http://feeds.bbci.co.uk/news/world/middle_east/rss.xml',
       'http://feeds.bbci.co.uk/news/world/us_and_canada/rss.xml',
       'http://feeds.bbci.co.uk/news/england/rss.xml',
       'http://feeds.bbci.co.uk/news/northern_ireland/rss.xml',
       'http://feeds.bbci.co.uk/news/scotland/rss.xml',
       'http://feeds.bbci.co.uk/news/wales/rss.xml']

class ArticleQueueGenerator():
    masterFeedURLList = []
    supplimentalFeeds = []

    def __init__(self, optional_feeds = []):
        self.masterFeedURLList = nytimes + wsj + washpo + bbc + optional_feeds
        self.articleQueue = queue.Queue()
        self.generateQueue(self.masterFeedURLList)

    def generateQueue(self, feedURLList):
        for url in feedURLList:
            feed = feedparser.parse(url)
            for item in feed:
                self.articleQueue.put(item)

    def getQueue(self):
        return self.articleQueue

    def getQueueSize(self):
        return self.articleQueue._qsize()

    def addMoreFeeds(self, feeds):
        self.supplimentalFeeds += feeds
        self.generateQueue(self.supplimentalFeeds)


generator = ArticleQueueGenerator()
print(generator.getQueueSize())
#Prints out the number of articles in the article Queue. The articles need to still be processed but this is a
# semidecent way of aggregating everything (I hope)