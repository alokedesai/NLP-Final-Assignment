import requests
from bs4 import BeautifulSoup

def scrape_data(url):
	res = requests.get(url)
	soup = BeautifulSoup(res.text)

	# get the actual article body
	article_paragraphs = soup.findAll("p", {"itemprop" : "articleBody"})
	article_text = [i.getText() for i in article_paragraphs]

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

