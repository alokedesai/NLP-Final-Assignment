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

		self.count_vectorizer = CountVectorizer(stop_words="english", min_df=3)
		
		# count vectorizer and specific classifier that will be used
		self.counts = None
		self.classifier = None

# throw out words that only occur 2 or 3 times
# mutual information for feature selection

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

  	def computeAccurracy(self, text, labels):
  		prediction = self.predict(text)
  		accurracy = 0
  		for i in range(len(prediction)):
  			if prediction[i] == labels[i]:
  				accurracy += 1
  		return accurracy / float(len(prediction))




objective_file = open("data/objective_train.data", "r")
subjective_file = open("data/subjective_train.data", "r")

objective_text = objective_file.readlines()
subjective_text = subjective_file.readlines()

# create testing data
objective_test = open("data/objective_test.data","r").readlines()
subjective_test = open("data/subjective_test.data","r").readlines()
test_data = objective_test + subjective_test
labels = [0 for i in range(len(objective_test))] + [1 for i in range(len(subjective_test))]

c = Classifier(objective_text, subjective_text)
c.vectorizeCounts()
c.termFrequencies()

c.linearSVC()
print c.computeAccurracy(test_data, labels)

c.multinomialNB()
print c.computeAccurracy(test_data, labels)