from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC, NuSVC
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics import f1_score
from sklearn.cross_validation import train_test_split
import random

class Classifier:
	def __init__(self, data, labels):
		OBJECTIVE = 0
		SUBJECTIVE = 1

		self.text = data
		self.labels = labels

		self.count_vectorizer = CountVectorizer(stop_words="english", min_df=3)

		self.counts = self.count_vectorizer.fit_transform(self.text)

		self.classifier = None

		self.tf_transformer = TfidfTransformer(use_idf=True)
		self.frequencies = self.tf_transformer.fit_transform(self.counts)

	def multinomialNB(self):
		self.classifier = MultinomialNB(alpha=.001)
		self.classifier.fit(self.frequencies, self.labels)

	def predict(self, examples):
		example_counts = self.count_vectorizer.transform(examples)
		example_tf = self.tf_transformer.transform(example_counts)
		predictions = self.classifier.predict(example_tf)
		return predictions

	def linearSVC(self):
  		self.classifier = LinearSVC()
  		self.classifier.fit(self.frequencies, self.labels)

  	def nuSVC(self):
  		self.classifier = NuSVC()
  		self.classifier.fit(self.frequencies, self.labels)

  	def accurracy(self, text, labels):
  		prediction = self.predict(text)
  		accurracy = 0
  		for i in range(len(prediction)):
  			if prediction[i] == labels[i]:
  				accurracy += 1
  		return accurracy / float(len(prediction))

  	def f1(self, text, actual):
  		prediction = self.predict(text)
  		return f1_score(actual, prediction)

objective_text = open("data/objective.sorted", "r").readlines()
subjective_text = open("data/subjective_long.sorted", "r").readlines()

OBJECTIVE = 0
SUBJECTIVE = 1

data = objective_text + subjective_text
labels = [OBJECTIVE for i in objective_text] + [SUBJECTIVE for i in subjective_text]

data_train, data_test, labels_train, labels_test = train_test_split(data,labels, test_size=.1, random_state=42)

c = Classifier(data_train, labels_train)

c.linearSVC()
print "Linear SVC accuracy: %f" % c.accurracy(data_test, labels_test)
print "Linear SVC F1: %f" % c.f1(data_test, labels_test)

c.multinomialNB()
print "Multinomial accuracy: %f" % c.accurracy(data_test, labels_test)
print "Multinomial F1: %f" % c.f1(data_test, labels_test)

# c.nuSVC()
# print "Nu-Support SVM accuracy: %f" % c.accurracy(test_data, labels)
# print "Nu-Support SVM F1: %f" % c.f1(test_data, labels)