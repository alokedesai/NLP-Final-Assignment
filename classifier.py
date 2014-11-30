import numpy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfTransformer


class Classifier:

	def __init__(self, objective_data, subjective_data):
		OBJECTIVE = 0
		SUBJECTIVE = 1

		self.objective_data = objective_data
		self.subjective_data = subjective_data

		self.text = objective_data + subjective_data
		self.labels = [0 for i in objective_data] + [1 for i in subjective_data]

		self.count_vectorizer = CountVectorizer()
		
		# count vectorizer and specific classifier that will be used
		self.counts = None
		self.classifier = None

	def vectorizeCounts(self):
		self.counts = self.count_vectorizer.fit_transform(numpy.asarray(self.text))

	def termFrequencies(self):
		tf_transformer = TfidfTransformer(use_idf=False).fit(self.counts)
		self.frequencies = tf_transformer.transform(self.counts)

	def multinomialNB(self):
		self.classifier = MultinomialNB()
		targets = numpy.asarray(self.labels)
		self.classifier.fit(self.frequencies, targets)

	def predict(self, examples):
		example_counts = self.count_vectorizer.transform(examples)
		predictions = self.classifier.predict(example_counts)
		return predictions

	def linearSVC(self):
  		self.classifier = LinearSVC()
  		self.classifier.fit(self.frequencies, self.labels)





objective_file = open("objective.data", "r")
subjective_file = open("subjective.data", "r")

objective_text = objective_file.read().split("\n\n")
subjective_text = subjective_file.read().split("\n\n")

c = Classifier(objective_text, subjective_text)
c.vectorizeCounts()
c.termFrequencies()

c.linearSVC()
print c.predict(["this is a test", "Obamacare will destroy the country", "Obamacare is horrible don't use it"])

c.multinomialNB()
print c.predict(["this is a test", "Obamacare will destroy the country", "Obamacare is horrible don't use it"])



# SUBJECTIVE = 0
# OBJECTIVE = 1

# data = DataFrame({'text': [], 'class': []})

# objective_file = open("objective.data", "r")
# subjective_file = open("subjective.data", "r")

# objective_text = objective_file.read()
# subjective_text = subjective_file.read()

# for line in objective_text.split("\n\n"):
# 	data = data.append(DataFrame({'text': [line], 'class': [1]}))

# for line in subjective_text.split("\n\n"):
# 	data = data.append(DataFrame({'text': [line], 'class': [0]}))

# count_vectorizer = CountVectorizer()
# counts = count_vectorizer.fit_transform(numpy.asarray(data['text']))

# classifier = MultinomialNB()
# targets = numpy.asarray(data["class"])
# classifier.fit(counts, targets)

# examples = ["Obamacare will be an utter disaster and it will fail miserably . We shouldn't use it at all"]

# example_counts = count_vectorizer.transform(examples)
# predictions = classifier.predict(example_counts)
# print predictions
