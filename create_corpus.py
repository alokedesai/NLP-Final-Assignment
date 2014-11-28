import requests
from bs4 import BeautifulSoup
import re
from nltk.tokenize import word_tokenize

def scrape_data(url):
	res = requests.get(url)
	soup = BeautifulSoup(res.text)

	# get the actual article body
	article_paragraphs = soup.findAll("p", {"itemprop" : "articleBody"})

	article_text = []
	for p in article_paragraphs:
		article = re.sub("\s+", " ", p.getText().strip())

		# tokenize article so we can just split on spaces to get words
		tokenized_article = word_tokenize(article)
		article_text.append(" ".join(tokenized_article))

	return "".join(article_text)


# read in articles_url.txt
with open("article_urls.txt", "r") as infile, open("subjective.data", "w") as subjective, open("objective.data", "w") as objective:

	for line in infile:
		type, url = line.split("\t")
		article_text = scrape_data(url.strip())
		print 'i'
		if type == "OpEd":
			subjective.write("%s\n\n" % article_text.encode("utf8"))
		else:
			objective.write("%s\n\n" % article_text.encode("utf8"))

