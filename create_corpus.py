import requests
from bs4 import BeautifulSoup

def scrapeData(url):
	res = requests.get(url)
	soup = BeautifulSoup(res.text)

	# get the actual article body
	article_paragraphs = soup.findAll("p", {"itemprop" : "articleBody"})
	article_text = [i.getText() for i in article_paragraphs]

	return "".join(article_text)

# read in articles_url.txt
data = open("article_urls.txt", "r")
articles = data.readlines()

# the two corpuses that will be created
subjective = open("subjective.data", "w")
objective = open("objective.data", "w")

for article in articles:
	content = article.split("\t")
	article_text = scrapeData(content[1].strip())

	if content[0] == "OpEd":
		subjective.write("%s%s" % (article_text.encode("utf8"), "\n\n"))
		subjective.write("==============================\n\n")
	else:
		objective.write("%s%s" % (article_text.encode("utf8"), "\n\n"))
		objective.write("==============================\n\n")


