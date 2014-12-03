from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC, NuSVC
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics import f1_score
import random

class Classifier:
	def __init__(self, objective_data, subjective_data):
		OBJECTIVE = 0
		SUBJECTIVE = 1

		self.objective_data = objective_data
		self.subjective_data = subjective_data

		self.text = objective_data + subjective_data
		self.labels = [OBJECTIVE for i in objective_data] + [SUBJECTIVE for i in subjective_data]

		self.count_vectorizer = CountVectorizer(stop_words="english", min_df=3)

		# count vectorizer and specific classifier that will be used

		self.counts = self.count_vectorizer.fit_transform(self.text)
		self.classifier = None

		self.tf_transformer = TfidfTransformer(use_idf=False)
		self.frequencies = self.tf_transformer.fit_transform(self.counts)

	def multinomialNB(self):
		self.classifier = MultinomialNB(alpha=.001)
		self.classifier.fit(self.frequencies, self.labels)

	def predict(self, examples):
		example_counts = self.count_vectorizer.transform(examples)
		example_tf = self.tf_transformer.fit_transform(example_counts)
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

objective_file = open("data/objective_train.data", "r")
subjective_file = open("data/subjective_train.data", "r")

objective_text = objective_file.readlines()
subjective_text = subjective_file.readlines()

# create testing data
objective_test = open("data/objective_test.data","r").readlines()
subjective_test = open("data/subjective_test.data","r").readlines()
test_data = objective_test + subjective_test
labels = [0 for i in range(len(objective_test))] + [1 for i in range(len(subjective_test))]
# tuple_list = [(test_data[i], labels[i]) for i in range(200)]
# random.shuffle(tuple_list)
# new_test_data = [x for x,y in tuple_list]
# new_labels = [y for x,y in tuple_list]


c = Classifier(objective_text, subjective_text)


c.linearSVC()
print "Linear SVC accuracy: %f" % c.accurracy(test_data, labels)
print "Linear SVC F1: %f" % c.f1(test_data, labels)

c.multinomialNB()
print "Multinomial accuracy: %f" % c.accurracy(test_data, labels)
print "Multinomial F1: %f" % c.f1(test_data, labels)

# c.nuSVC()
# print "Nu-Support SVM accuracy: %f" % c.accurracy(test_data, labels)
# print "Nu-Support SVM F1: %f" % c.f1(test_data, labels)