from nltk.corpus import stopwords
from newspaper import Article
import feedparser
from RssQueueGenerator import ArticleQueueGenerator
from collections import Counter
import numpy
from sklearn.cluster import KMeans
from sklearn import metrics

removeSet = set(stopwords.words('english'))
removeSet.update(['continue', 'reading', 'lately', 'wanted', 'call', 'later', 'latest', 'main', 'said','way', 'many', 'available', 'efforts', 'similar', 'programadvertisement', 'multiple', 'months' 'essentially', 'identify', 'include', 'name'])
class ParsedEntry:
    """Object which contains information about each article, including its name and
    cleaned text. Includes function for preprocessing.
    Not called article to avoid conflict with Newspaper package"""
    def __init__(self, name, body, link):
        self.url = link
        self.title = name
        self.tagTable, self.cleanWordsList = self._preprocessText(body)

    def _preprocessText(self, body):
        """casefolds text and removes stopwords, returns a list of the article's
        words and a dictionary where the keys are unique words and the values are
        their occurrence counts.
        cleanWordsList is not currently used, but could be used to normalize the
        number of word occurences, so we kept it for future flexibility."""
        tagTable = {}
        lowercaseText = body.lower()
        newStr = ""
        for c in lowercaseText:
            if c.isalpha() or c==" ":
                newStr+=c
        self.text = newStr

        #remove stopwords and build dictionary of wordcounts.
        wordsList = self.text.split()
        cleanWordsList = []
        for word in wordsList:
            if word not in removeSet:
                if word not in tagTable.keys():
                    tagTable[word] = 0
                tagTable[word] = tagTable[word] + 1
                cleanWordsList.append(word)

        return tagTable, cleanWordsList


    #given an integer n, returns the n most frequently appearing keywords in the article
    def getTopTags(self, number):
        #http://stackoverflow.com/questions/11902665/top-values-from-dictionary
        top = Counter(self.tagTable)
        top.most_common()
        topTags = {}
        for k, v in top.most_common(10):
            topTags[k] = v
        return topTags

def initTags(topTags, tagSet, article):
    """Given an article and it's n most commonly occurring words, adds each
    article to the list of articles associated with that tag. If the tag is
    not already in the set of tags, create it."""
    for tag in topTags:
        if tag in tagSet.keys():
            tagSet[tag].append(article)
        else:
            tagSet[tag] = [article]

def tagDistanceMatrix(tagSet, labels, articleSet):
    """Builds a binary array denoting which articles have which tags. Rows represent
    articles and columns represent tags, so 1 in position i, j means that the article
    i is tagged with keyword j. 'labels' is just the set of keys of tagSet (that is,
    the list of all keys) - it's passed as a list to ensure the ordering of the tags
    is the same as it will be later.
    Also: look at that list comprehension! I'm super proud of myself."""
    distances = numpy.array([[(article in tagSet[tag]) for article in articleSet]
          for tag in labels])
    return distances

def feedArticleParsing(feed):
    """Procedure for reading in articles from a given feed.
    For each article in the RSS feed, grab it, process it, and find its tags"""
    global i
    for entry in feed:
        toParse = Article(entry.link)
        toParse.download()
        toParse.parse()
        entry = ParsedEntry(toParse.title, toParse.text, entry.link)
        articleSet.append(entry)
        topTags = articleSet[i].getTopTags(30)
        initTags(topTags, tagSet, entry)
        i+=1
        del toParse
        if i % 100 == 0:
            print("You have parsed " + str(i) + " articles.")

articleSet = []
tagSet = {} #keys are tag names, value is list of articles with that tag
i = 0
feedGenerator =  ArticleQueueGenerator()
feedEntries = list(feedGenerator.getQueue().queue)
articleSet = feedArticleParsing(feedEntries)
tagFlag = False #True if we want to cluster tags, false if we want to cluster articles
labels = list(tagSet.keys()) #want to ENSURE the ordering is the same now and later

#calculate the binary matrix representing which articles have which tags
distances = tagDistanceMatrix(tagSet, labels, articleSet)
if tagFlag is False:
    distances = numpy.transpose(distances)
    labels = [article.title for article in articleSet] #make labels article names, not tags


print("Clustering tags, not articles: ", tagFlag)
print("Articles: " + i.__str__())
print("Labels: " + len(labels).__str__())
print("Beginning K means now with k=1:")

km = KMeans(n_clusters = 1, random_state = 0).fit(distances)
initInertia = km.inertia_
print(initInertia)
#attempts to find the optimal k by stopping clustering when efficnecy lowers
elbowed = False
k = 1
while not elbowed and k < len(articleSet)-1:
    k+=1
    print("k = " + k.__str__())
    km = KMeans(n_clusters = k, random_state = 0).fit(distances)
    newInertia = km.inertia_
    print(newInertia)
    if newInertia > (initInertia * .8):
        elbowed = True
    else:
        initInertia = newInertia

#print out the clusters - each number represents the cluster number of the object at that index
print(km.labels_)
clusters = [[] for i in range (0, k)] #each entry in this list is a list of the items in the cluster
#fill up the cluster lists with the items
for i in range(0, len(km.labels_)):
    clusters[km.labels_.item(i)].append(labels[i])
for i in range (0, k):
    print("Cluster ", i, " is: ", clusters[i])