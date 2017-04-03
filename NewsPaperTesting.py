import feedparser
import newspaper
from newspaper import Article as nArticle
from AlgorithmDraftGlobal import Article
from AlgorithmDraftGlobal import Category
NYTAmericas = feedparser.parse("http://www.nytimes.com/services/xml/rss/nyt/Americas.xml")

NYTAfrica = feedparser.parse("http://www.nytimes.com/services/xml/rss/nyt/Africa.xml")

NYTEurope = feedparser.parse("http://www.nytimes.com/services/xml/rss/nyt/Europe.xml")

NYTMidEast = feedparser.parse("http://www.nytimes.com/services/xml/rss/nyt/MiddleEast.xml")

americas = Category("Americas", "null path")
for article in NYTAmericas.entries:
    print(article.link)
    articleToAdd = nArticle(article.link)
    articleToAdd.download()
    articleToAdd.parse()
    text = articleToAdd.text
    americas.addArticle(Article(01, article.link, text))

    #should print title for Articles Americas article. the feedparser is sorta weird with all this.


print("now printing NYT categories:")
NYT = newspaper.build('http://nytimes.com')
for category in NYT.category_urls():
    print(category)
print("now printing NYT articles from main page")
for article in NYT.articles:
    print(article.title)
# new plan: import newspaper, create a whitelist of sources to create categories.

#From there we get a NYTimes source, (example: Americas)

#From there we go through all the articles in the AMericas section, and get the article text. this is done using article.text, and article.parse()

#We then filter it out using the common words from the library we have available, and then we go further,