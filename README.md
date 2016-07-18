# ExtempBot
Bot to automate extemp research. The bot functions using three main parts:

1. The bot utilizes a library named "Newspaper" in conjunction with a whitelist of RSS feeds. This process takes in those feeds and returns a collection of articles preferably in pdf form which are then put into the sorter

2. The bot then runs through each article creating functionally a word cloud, with the occurences of the word per a certain constant as the weighting value for the size of each word. Using this and having presorted articles on hand, the bot then begins to sort. Prior to weighting, the article is scrubbed of stop words from the NLTK in order to prevent many common words from directly affecting sorting.

3. Sorting is done using a distance algorithm using a single plane per each word occuring in the article. The distance total between the article with its own words, and the category which creates averages of the articles already sorted then leads to a relatively accurate assignment. The sorter than merges the scores and values of the article with the value of the category it is assigned to, helping create a more accurate algorithm. If a category does not contain the word in the article, then it will automatically be assigned that word in its cloud with a value of 0.


TODO: Auto feed articles that are pre-sorted to establish base categories, then auto-feed articles from websites and auto-sort.
