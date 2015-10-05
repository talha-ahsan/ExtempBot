__author__ = 'talhaahsan and benpankow'
import math
import re
import os
import pickle
from nltk.corpus import stopwords
from newspaper import Article as nArticle

nextArticleID = 1

stopwords = set(stopwords.words('english'))

categories = []

class Category:

    def __init__ (self, name, path):
        self.name = name
        self.categoryFolderPath = path
        # Contains total words in articles inside. Total word count inside China folder, and more!
        self.totalWordCount = 0
        #wordRate and wordOccuranceCount are both maps with string keys, and integer values. wordRate / 1000 * totalWordCount = the number of times the word has been seen
        self.wordRate = {}
        self.wordOccuranceCount = {}
        # Where wordRate[key] = wordOccuranceCount[key] * 1000 / totalWordCount

        # All the articles contained in this category
        self.articles = []

    # add an article's word data to the category's word data
    def addArticle(self, article):
        print("adding article " + str(article.id) + " to " + self.name)
        self.articles.append(article)
        # update the occurrence count for the category as a whole, adding the occurrences from the article
        for word in article.articleOccuranceCount:
            if word not in self.wordOccuranceCount:
                self.wordOccuranceCount[word] = 0
            self.wordOccuranceCount[word] = self.wordOccuranceCount[word] + article.articleOccuranceCount[word]
            self.totalWordCount += article.articleOccuranceCount[word]
        # now update the word rate
        for key in self.wordOccuranceCount.keys():
            self.wordRate[key] = self.wordOccuranceCount[key] * 1000 / self.totalWordCount

    # remove an article from this category
    def removeArticle(self, article):
        self.articles.remove(article)
        # update the occurrence count for the category as a whole, subtracting the occurrences from the article
        for word in article.articleOccuranceCount:
            self.wordOccuranceCount[word] = self.wordOccuranceCount[word] - article.articleOccuranceCount[word]
            self.totalWordCount -= article.articleOccuranceCount[word]
        # now update the word rate
        for key in self.wordOccuranceCount.keys():
            if (self.totalWordCount != 0):
                self.wordRate[key] = self.wordOccuranceCount[key] * 1000 / self.totalWordCount
            else:
                self.wordRate[key] = 0
            
    def save(self):
        ids = []
        for article in self.articles:
            article.save()
            ids.append(article.id)
            
        saveFile = open(self.name + '.xcat', 'wb')
        data = [self.name, self.totalWordCount, self.categoryFolderPath, self.wordRate, self.wordOccuranceCount, ids]
        pickle.dump(data, saveFile)
        saveFile.close()
        
    def delete(self):
        for article in self.articles:
            try:
                os.remove('article' + str(article.id) + '.xart')
            except OSError:
                pass
        try:
            os.remove(self.name + '.xcat')
        except OSError:
            pass

    @classmethod
    def loadFromFile(cls, name):
        loadFile = open(name + '.xcat', 'rb')
        data = pickle.load(loadFile)
        loadFile.close()
        cat = cls(data[0], data[2])
        cat.totalWordCount = data[1]
        cat.wordRate = data[3]
        cat.wordOccuranceCount = data[4]
        ids = data[5]
        for id in ids:
            article = Article.loadFromFile(id)
            cat.articles.append(article)
            id = id

        return cat
        

class Article:

    def __init__ (self, id, url, text):
        self.id = id
        self.articleURL = url
        self.articleBody = text
        self.articleWordRate = {}
        self.articleOccuranceCount = {}

    # counts occurrence of each word in the article (this number is saved for category calculation later) and used to determine the word rate
    def calculateWordRate(self):
        # get a list of words in the article
        words = sanitize(self.articleBody)

        totalWords = 0
        for word in words:
        # ignore all stopwords
            if word not in stopwords:
                if word not in self.articleOccuranceCount.keys():
                    self.articleOccuranceCount[word] = 0
                # count each word and count the total amount of words
                self.articleOccuranceCount[word] = self.articleOccuranceCount[word] + 1
                totalWords += 1
        # calculate the rate
        for word in self.articleOccuranceCount.keys():
            self.articleWordRate[word] = (self.articleOccuranceCount[word] * 1000) / totalWords
    
    def save(self):
        saveFile = open('article' + str(self.id) + '.xart', 'wb')
        data = [self.id, self.articleWordRate, self.articleOccuranceCount, self.articleURL, self.articleBody]
        pickle.dump(data, saveFile)
        saveFile.close()

    @classmethod
    def loadFromFile(cls, id):
        loadFile = open('article' + str(id) + '.xart', 'rb')
        data = pickle.load(loadFile)
        loadFile.close()
        art = cls(id, data[3], data[4])
        art.articleWordRate = data[1]
        art.articleOccuranceCount = data[2]

        return art

#Syncs article text with category words
def updateCategoryWords(article, category):
    # takes article keywords, and adds them to the category list if necessary
    testwords = article.articleWordRate.keys()
    for word in testwords:
        if word not in category.wordRate.keys():
            category.wordRate[word] = 0
    return
	
# compares article rate with category rate, returning the distance
def distance(article, category):
    # make sure errors are minimized
    updateCategoryWords(article, category)

    categoryWords = category.wordRate.keys()
    distancesquare = 0
    for key in categoryWords:
        if key not in article.articleWordRate.keys():
            termdifference = category.wordRate[key]
        else:
            termdifference = category.wordRate[key] - article.articleWordRate[key]
        distancesquare += (termdifference ** 2)
    return math.sqrt(distancesquare)
    
# this version only uses the article's words
def distanceAO(article, category):
    # make sure errors are minimized
    updateCategoryWords(article, category)

    articleWords = article.articleWordRate.keys()
    distancesquare = 0
    for key in articleWords:
        termdifference = category.wordRate[key] - article.articleWordRate[key]
        distancesquare += (termdifference ** 2)
    return math.sqrt(distancesquare)
	
	
# makes lowercase. returns a list of words in the article
def sanitize(text):
    # first, make lowercase
    text = text.lower()
    # make a list of every word
    list = re.compile('\w+').findall(text)
    return list


# saves all categories
def saveCategories():
    names = []
    for category in categories:
        category.save()
        names.append(category.name)
        print('Now saving ' + category.name + '.xcat...')
    saveFile = open('categories.xdat', 'wb')
    pickle.dump(names, saveFile)
    saveFile.close()

# loads all categories
def loadCategories():
    saveFile = open('categories.xdat', 'rb')
    catNames = pickle.load(saveFile)
    saveFile.close()
    for catName in catNames:
        cat = Category.loadFromFile(catName)
        categories.append(cat)
    
#Loads a variety of misc information, right now just the next article ID
def loadMisc():
    global nextArticleID
    saveFile = open('misc.xdat', 'rb')
    miscItems = pickle.load(saveFile)
    nextArticleID = miscItems[0]
    saveFile.close()
    return
    
#Saves a variety of misc information, right now just the next article ID
def saveMisc():
    list = [ nextArticleID ]
    saveFile = open('misc.xdat', 'wb')
    pickle.dump(list, saveFile)
    saveFile.close()
    return


#initial calibration function for a category, takes the articles inside and sorts them
def categoryCalibrate(category):
    #TODO: create a list of articles currently in the folder using the folder path.

    #TODO: run through the list, converting each article pdf file into an html file
        #TODO: feed the article into newspaper to get the body text
        #TODO: for each article after conversion, run through the text so that it can increment or update the wordOccuranceCount dict
        #TODO: implement this https://www.binpress.com/tutorial/manipulating-pdfs-with-python/167
    return
    
    
def getNextArticleID():
    global nextArticleID
    nextArticleID += 1
    return nextArticleID
    
def closestCategory(article):
    minDist = -1
    closestCat = categories[0]
    for category in categories:
        if (minDist == -1):
            minDist = distanceAO(article, category)
            print("Distance to " + category.name + ": " + str(minDist))
            closestCat = category
        else:
            dist = distanceAO(article, category)
            print("Distance to " + category.name + ": " + str(dist))
            if (dist < minDist):
                minDist = dist
                closestCat = category  
    return closestCat

def getCategory(name):
    for category in categories:
        if (category.name == name):
            return category
    else:
        return None
        
def topNWords(category, num):
    if (num > len(category.wordOccuranceCount)):
        num = len(category.wordOccuranceCount)
    topWords = []
    topCount = []
    for i in range(0, num):
        key = category.wordOccuranceCount.keys()[i]
        topWords.append(key)
        topCount.append(0)
    for word in category.wordOccuranceCount.keys():
        i = num - 1
        while i > -2:
            # print(str(i) + " " + word)
            if (i > -1 and category.wordOccuranceCount[word] >= topCount[i]):
                if (i < num - 1):
                    topCount[i + 1] = topCount[i]
                    topWords[i + 1] = topWords[i]
            else:
                if (i < num - 1):
                    topCount[i + 1] = category.wordOccuranceCount[word]
                    topWords[i + 1] = word
                break
            i = i - 1
    return [topWords, topCount]
    
def manualCategorization():
    loadMisc()
    loadCategories()
    cmd = ""
    cmd = raw_input('\n\n\n\nWhat would you like to do? (use "help" for help): ')
    cmd = cmd.lower()
    while (cmd != "exit"):
        if (cmd == "help"):
            print("\nhelp\t\tGet help")
            print("exit\t\tExit the program")
            print("cat NAME\tCreate a category with indicated name")
            print("delcat NAME\tDelete a category with indicated name")
            print("catdat NAME\tGet info for the specified category")
            print("URL\t\t\tBegin processing an article at the designated URL")
            print("lscat\t\tList all categories")
        elif (cmd[:4] == "cat "):
            catName = cmd[4:]
            cat = Category(catName, "")
            categories.append(cat)
            print("\nCategory '" + catName + "' successfully created!")
        elif (cmd[:7] == "delcat "):
            catName = cmd[7:]
            cmd = raw_input('\nAre you sure you would like to delete category ' + catName + '? This will remove all contained articles and cannot be reversed. (y/n): ')
            cmd = cmd.lower()
            if (cmd == "y"):
                category = getCategory(catName)
                if (category != None):
                    category.delete()
                    categories.remove(category)
                    print("\nCategory '" + catName + "' successfully deleted!")
                else:
                    print("\nNo category with name '" + catName + "' found")
        elif (cmd[:7] == "catdat "):
            catName = cmd[7:]
            category = getCategory(catName)
            if (category != None):
                articleNames = ""
                for article in category.articles:
                    articleNames = articleNames + str(article.id) + ", "
                print("\nIncluded articles: " + articleNames)
                dat = topNWords(category, 10)
                words = dat[0]
                counts = dat[1]
                for i in range(0, len(words)):
                    print(str(i + 1) + ": " + words[i] + "\t\t" + str(counts[i]))
            else:
                print("\nNo category with name '" + catName + "' found")
        elif (cmd == "lscat"):
            print("")
            for category in categories:
                print(category.name)
        elif (cmd[:4] == "http"):
            url = cmd
            narticle = nArticle(url)
            narticle.download()
            narticle.parse()
            text = narticle.text

            # create an article object and calculate the word rate
            id = getNextArticleID()
            article = Article(id, url, text)
            article.calculateWordRate()
            
            closestCat = closestCategory(article)
            title = narticle.title.encode("utf-8")
            print("Suggested category: " + closestCat.name)
            cmd = raw_input("Which category would you like to add '" + title + "' to?: ")
            cmd = cmd.lower()
            category = getCategory(cmd)
            while (category == None):
                cmd = raw_input("\nWhich category would you like to add '" + title + "' to?: ")
                cmd = cmd.lower()
                category = getCategory(cmd)
            category.addArticle(article)
        elif (cmd[:5] == "list "):
            file = cmd[5:]
            print file
            print os.path.isfile(file)
            if (os.path.isfile(file) and file[-4:] == ".txt"):
                cmd = raw_input("Which category would you like to add the contents of '" + file + "' to?: ")
                cmd = cmd.lower()
                category = getCategory(cmd)
                while (category == None):
                    cmd = raw_input("Which category would you like to add the contents of '" + file + "' to?: ")
                    cmd = cmd.lower()
                    category = getCategory(cmd)
                
                lines = [line.strip() for line in open(file)]
                for url in lines:
                    narticle = nArticle(url)
                    narticle.download()
                    narticle.parse()
                    text = narticle.text

                    # create an article object and calculate the word rate
                    id = getNextArticleID()
                    article = Article(id, url, text)
                    article.calculateWordRate()
                    
                    category.addArticle(article)
            
        cmd = raw_input('\nWhat would you like to do? (use "help" for help): ')
        cmd = cmd.lower()
        
    saveCategories()
    saveMisc()

def testMethod():
    loadMisc()
    loadCategories()
    
    print("\n" + categories[0].name + "\n-Word Rate for 'republican': " + str(categories[0].wordRate["republican"]) + "/1000\n-Word Occurance for 'republican': " + str(categories[0].wordOccuranceCount["republican"]) + "/" + str(categories[0].totalWordCount))
    print("\nArticle no." + str(categories[0].articles[0].id) + "\n-Word Rate for 'republican': " + str(categories[0].articles[0].articleWordRate["republican"]) + "/1000\n-Word Occurance for 'republican': " + str(categories[0].articles[0].articleOccuranceCount["republican"]) + "\n")
    print(distance(categories[0].articles[0], categories[0]))
    print(closestCategory(categories[0].articles[0]).name)

    saveCategories()
    saveMisc()

def testMethod2():
    # create a newspaper Article object
    url = 'http://www.nytimes.com/2015/09/02/us/politics/cnn-alters-debate-criteria-which-could-help-carly-fiorina.html'
    narticle = nArticle(url)
    # download and parse the article (this gives us the clean text and info like author, date etc)
    narticle.download()
    narticle.parse()
    text = narticle.text

    # create an article object and calculate the word rate
    id = getNextArticleID()
    article = Article(id, url, text)
    article.calculateWordRate()
    sortedWordRate = sorted(article.articleWordRate.items(), key=operator.itemgetter(1))
    categories[0].addArticle(article)

if __name__ == '__main__':
    manualCategorization()