__author__ = 'talhaahsan and benpankow'
import math
import re
import operator #temp for testing
import pickle
from nltk.corpus import stopwords
from newspaper import Article as nArticle
import feedparser

#An arbitrary set of feeds off the new york times RSS webpage. INCOMPLETE
feedList = ['http://rss.nytimes.com/services/xml/rss/nyt/World.xml', 'http://rss.nytimes.com/services/xml/rss/nyt/Africa.xml', 'http://rss.nytimes.com/services/xml/rss/nyt/Americas.xml', 'http://rss.nytimes.com/services/xml/rss/nyt/AsiaPacific.xml', 'http://rss.nytimes.com/services/xml/rss/nyt/Europe.xml', 'http://rss.nytimes.com/services/xml/rss/nyt/MiddleEast.xml', 'http://rss.nytimes.com/services/xml/rss/nyt/US.xml', 'http://rss.nytimes.com/services/xml/rss/nyt/Education.xml', 'http://rss.nytimes.com/services/xml/rss/nyt/Politics.xml', 'http://rss.nytimes.com/services/xml/rss/nyt/Business.xml', 'http://rss.nytimes.com/services/xml/rss/nyt/EnergyEnvironment.xml', 'http://rss.nytimes.com/services/xml/rss/nyt/InternationalBusiness.xml', 'http://rss.nytimes.com/services/xml/rss/nyt/SmallBusiness.xml']

feeds = []

for feed in feedList:
    feeds.append(feedparser.parse(feed))

#The set of all articles in Newspaper format.
entries = []

#runs through each feed, taking each item / article, and adding its nArticle to the entries object.
for feed in feeds:
    for item in feed["items"]:
        entries.append(nArticle(item["link"]))
#From here there seems to be a set of entries containing a ton of Articles using the URLs from the RSS feed.