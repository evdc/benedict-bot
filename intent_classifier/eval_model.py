import numpy as np
from data_utils import *
from models.spacy_lstm import SpacyLSTM
from modeler import Modeler
from sklearn.metrics import classification_report
import spacy

X, y = load_file('training_data/test.txt')
print X.shape, y.shape

nlp = spacy.load('en')
m = Modeler(SpacyLSTM, vocab=nlp.vocab).load()
predicted = m(y)

print classification_report(y, predicted, target_names=m.labels)
acc = float(np.sum(y == predicted)) / float(len(y))
print "Accuracy:", acc