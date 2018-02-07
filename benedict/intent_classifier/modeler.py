import numpy as np
import os
from sklearn.metrics import classification_report
from keras.utils import np_utils
import spacy
import glob
import json
from data_utils import *

from models.spacy_lstm import SpacyLSTM

''' Framework for training, evaluating, loading, saving and using models.
    On call, predict a vector of samples (so to predict one sample, use modeler([x])[0] )
    This framework can be used by any model that supports the following methods:
        train, predict, save, load 
    Kwargs given to constructor of the Modeler will be passed on to constructor of the model
'''

class Modeler(object):
    def __init__(self, model_class,
            model_directory='models', training_directory='training_data', **kwargs):
        self.labels = ['add_calendar', 'calendar', 'check_reminders', 'reminders', 'weather']
        self.model_directory = os.path.join(os.path.abspath(os.path.dirname(__file__)), model_directory)
        self.training_directory = os.path.join(os.path.abspath(os.path.dirname(__file__)), training_directory)
        self.model = model_class(n_categories=len(self.labels), **kwargs)

    def train(self, training_directory, **kwargs):
        print "Loading training data ..."
        X, y = load_file(self.training_directory + '/train.txt')
        Y = np_utils.to_categorical(labels2indexes(y, self.labels))
        print X.shape, Y.shape

        print "Training model"
        self.model.train(X, Y, **kwargs)

        print "Evaluating model"
        X_test, y_test = load_file(self.training_directory + '/test.txt')
        Y_test = labels2indexes(y_test, self.labels)
        self.evaluate(X_test, Y_test)

        return self

    def __call__(self, X):
        Y = self.model.predict(X)
        return [self.labels[y] for y in Y]

    def load(self):
        self.model.load(self._model_path())
        return self

    def save(self):
        self.model.save(self._model_path())
        return self

    def evaluate(self, X, y):
        predicted = self.model.predict(X)
        print '\n', predicted, predicted.shape
        print y, y.shape
        print classification_report(y, predicted, target_names=self.labels)

        acc = float(np.sum(y == predicted)) / float(len(y))
        print "Accuracy:", acc

    def _model_path(self):
        model_name = self.model.__class__.__name__
        return self.model_directory + '/' + model_name + '.h5'

if __name__ == "__main__":
    # Train and save a model
    print "Loading spaCy ..."
    nlp = spacy.load('en')
    print "Initializing modeler ..."
    m = Modeler(SpacyLSTM, vocab=nlp.vocab)
    m.train('training_data', nb_epoch=1)
    m.save()






