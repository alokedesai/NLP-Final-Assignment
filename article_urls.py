import urllib, json

base_url = "http://api.nytimes.com/svc/search/v2/articlesearch.json?q=obamacare&fl=web_url%2Cnews_desk&api-key=17a92e5aa402d751f17bff6ed5e9f0f1:19:49094860&page=1"

for i in range(1,101):

	response = urllib.urlopen(base_url + "&page=" + str(i))
	data = json.loads(response.read())

	for article in data["response"]["docs"]:
		if article["news_desk"] and article["web_url"]:
			print article["news_desk"] + "\t" + article["web_url"]