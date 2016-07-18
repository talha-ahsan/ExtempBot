__author__ = 'talhaahsan and benpankow'
import math
import re
import operator #temp for testing
import pickle
from nltk.corpus import stopwords
from newspaper import Article as nArticle
import feedparser

#An arbitrary set of feeds off the new york times RSS webpage.
nytimes = ['http://rss.nytimes.com/services/xml/rss/nyt/World.xml', 'http://rss.nytimes.com/services/xml/rss/nyt/Africa.xml', 'http://rss.nytimes.com/services/xml/rss/nyt/Americas.xml', 'http://rss.nytimes.com/services/xml/rss/nyt/AsiaPacific.xml', 'http://rss.nytimes.com/services/xml/rss/nyt/Europe.xml', 'http://rss.nytimes.com/services/xml/rss/nyt/MiddleEast.xml', 'http://rss.nytimes.com/services/xml/rss/nyt/US.xml', 'http://rss.nytimes.com/services/xml/rss/nyt/Education.xml', 'http://rss.nytimes.com/services/xml/rss/nyt/Politics.xml', 'http://rss.nytimes.com/services/xml/rss/nyt/Business.xml', 'http://rss.nytimes.com/services/xml/rss/nyt/EnergyEnvironment.xml', 'http://rss.nytimes.com/services/xml/rss/nyt/InternationalBusiness.xml', 'http://rss.nytimes.com/services/xml/rss/nyt/SmallBusiness.xml', 'http://rss.nytimes.com/services/xml/rss/nyt/Economy.xml', 'http://rss.nytimes.com/services/xml/rss/nyt/MediaandAdvertising.xml', 'http://rss.nytimes.com/services/xml/rss/nyt/YourMoney.xml', 'http://rss.nytimes.com/services/xml/rss/nyt/Technology.xml', 'http://bits.blogs.nytimes.com/feed/', 'http://rss.nytimes.com/services/xml/rss/nyt/PersonalTech.xml', 'http://rss.nytimes.com/services/xml/rss/nyt/Science.xml', 'http://rss.nytimes.com/services/xml/rss/nyt/Environment.xml', 'http://rss.nytimes.com/services/xml/rss/nyt/Health.xml', 'http://rss.nytimes.com/services/xml/rss/nyt/Research.xml', 'http://rss.nytimes.com/services/xml/rss/nyt/Nutrition.xml', 'http://rss.nytimes.com/services/xml/rss/nyt/HealthCarePolicy.xml', 'http://rss.nytimes.com/services/xml/rss/nyt/Views.xml']
#WashPo RSS
washPo = []
#Wall Street Journal
wsj = ['http://www.wsj.com/xml/rss/3_7041.xml', 'http://www.wsj.com/xml/rss/3_7085.xml', 'http://www.wsj.com/xml/rss/3_7014.xml', 'http://www.wsj.com/xml/rss/3_7031.xml', 'http://www.wsj.com/xml/rss/3_7455.xml', 'http://blogs.wsj.com/bankruptcy/feed/', 'http://blogs.wsj.com/chinarealtime/feed/', 'http://blogs.wsj.com/corruption-currents/feed/', 'http://feeds.wsjonline.com/wsj/dailyfix/feed/', 'http://blogs.wsj.com/wealth-manager/feed/', 'http://blogs.wsj.com/health/feed/', 'http://blogs.wsj.com/hong-kong/feed/', 'http://blogs.wsj.com/indiarealtime/feed/', 'http://blogs.wsj.com/japanrealtime/feed/', 'http://blogs.wsj.com/korearealtime/feed/', 'http://blogs.wsj.com/middleseat/feed/', 'http://feeds.wsjonline.com/wsj/numbersguy/feed', 'http://blogs.wsj.com/emergingeurope/feed/', 'http://blogs.wsj.com/washwire/feed/']
#Daily Beast
dBeast = []

sourceList = [nytimes, washPo, dBeast]

feeds = []

for source in sourceList:
    for feed in source:
        feeds.append(feedparser.parse(feed))

#The set of all articles in Newspaper format.
entries = []

#runs through each feed, taking each item / article, and adding its nArticle to the entries object.
for feed in feeds:
    for item in feed["items"]:
        entries.append(nArticle(item["link"]))
#From here there seems to be a set of entries containing a ton of Articles using the URLs from the RSS feed.