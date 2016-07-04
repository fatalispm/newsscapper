import urllib2
from itertools import takewhile

import newspaper
from datetime import datetime

from bs4 import BeautifulSoup


class Article(object):
    def __init__(self, title, text, author, date, url):
        self.text = text
        self.title = title
        self.author = author
        self.date = date
        self.url = url

    def __repr__(self):
        return "%s: %s" % (self.title, self.author)

    @classmethod
    def from_newspaper_article(cls, article):
        title = article.title
        author = article.authors[0] if len(article.authors) > 1 else ""
        date = article.publish_date
        url = article.url
        text = article.text
        return cls(title, text, author, date, url)

    def was_published_recently(self, default=True):
        """
        :param default: What to return if there was no date
        :return: true if article is not older than two days
        """

        return (datetime.now() - self.date.replace(tzinfo=None)).days > 2 if self.date else default


def get_page(url):
    page = urllib2.urlopen(url).read()
    return BeautifulSoup(page)


def get_links_to_articles(url):
    page = get_page(url)
    news = page.findAll("div", {"class": "item clearfix"})

    def get_link(x):
        try:
            return x.find("a")['href']
        except:
            return

    links_to_news = map(get_link, news)
    return links_to_news


def scrape(link):
    article = newspaper.Article(link)
    article.build()
    return Article.from_newspaper_article(article)


def articles():
    url = "http://itukraine.org.ua/en/news"
    return scrape(get_links_to_articles(url))
