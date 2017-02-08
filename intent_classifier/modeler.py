import numpy as np
import os
from sklearn.metrics import classification_report
from keras.utils import np_utils
import glob

from models.simple_lstm import SimpleLSTM

# Framework for training, evaluating, loading, saving and using models
# By default, on init will load a pretrained version of the given model class,
# or if there isn't one will train and save one; this can be prevented by passing initialize=False to constructor.
# On call, predict a vector of samples (so to predict one sample, use modeler([x])[0] )
# This framework can be used by any model that supports the following methods:
#	train, predict, save, load

def from_categorical(Y):
    return np.nonzero(Y)[1]

class Modeler(object):
	def __init__(self, model_class=None, model_directory='models', training_directory='training_data'):
		self.labels = []
		self.n_categories = 0
		self.model_class = None
		self.model = None
		self.model_directory = os.path.join(os.path.abspath(os.path.dirname(__file__)), model_directory)
		self.training_directory = os.path.join(os.path.abspath(os.path.dirname(__file__)), training_directory)

		if model_class:
			self.model_class = model_class
			self.load_or_train(model_class, self.model_directory, self.training_directory)

	def load_or_train(self, model_class, model_directory, training_directory):
		name = model_class.__name__
		model_path = model_directory + '/' + name + '.h5'
		if os.path.exists(model_path):
			print "Loading " + model_path
			self.load(model_class)
		else:
			print "No existing model found. Training new one"
			self.build_and_save(model_class, training_directory)
		assert self.model

	def load(self, model_class):
		self.model = model_class()
		model_name = self.model.__class__.__name__
		self.model.load(self.model_directory + '/' + model_name + '.h5')

	def save(self):
		model_name = self.model.__class__.__name__
		self.model.load(self.model_directory + '/' + model_name + '.h5')

	def build_and_save(self, model_class, training_directory):
		print "Loading training data ..."
		X_train, Y_train, X_test, Y_test = self.load_training_data(training_directory)
		print "Initializing model"
		self.model = model_class(n_categories=self.n_categories)
		print "Training model"
		self.model.train(X_train, Y_train)
		print "Evaluating model"
		self.evaluate(X_test, Y_test)
		self.save()
		print "Model saved!"

	def load_training_data(self, directory, train_split=0.7):
	    X = []
	    y = []
	    self.labels = []
	    l = 0
	    for filename in glob.glob(directory+'/*.txt'):
	        label = filename.split('/')[-1].split('.')[0]
	        self.labels.append(label)
	        with open(filename, 'r') as f:
	            for line in f:
	                X.append((line.strip(), l))
	        l += 1
	    self.n_categories = len(self.labels)

	   	# Shuffle array of samples
	    np.random.shuffle(X)
	    
	    # Split (data, label) pairs into X and y arrays
	    y = [x[1] for x in X]
	    X = [x[0] for x in X]
	    Y = np_utils.to_categorical(y)

	    # Split into train and test data
	    idx = int(len(X) * train_split)
	    self.X_train = X[:idx]
	    self.X_test = X[idx:]
	    self.Y_train = Y[:idx]
	    self.Y_test = Y[idx:]

	    # TODO stats: how many of each category are in train and test?
	    return (self.X_train, self.Y_train, self.X_test, self.Y_test)

	def __call__(self, X):
		Y = self.model.predict(X)
		Y = from_categorical(Y)
		return [self.labels[y] for y in Y]

	def evaluate(self, X_test, Y_test):
	    predicted = self.model.predict(X_test)
	    print predicted, predicted.shape
	    y = from_categorical(Y_test)
	    print y, y.shape
	    print classification_report(y, predicted, target_names=self.labels)

	    acc = float(np.sum(y == predicted)) / float(len(y))
	    print "Accuracy:", acc

if __name__ == "__main__":
	mt = Modeler(model_class=SimpleLSTM)


