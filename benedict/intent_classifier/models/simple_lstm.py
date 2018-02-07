import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers.convolutional import Convolution1D
from keras.layers.convolutional import MaxPooling1D
from keras.layers.embeddings import Embedding
from keras.preprocessing import sequence
from keras.preprocessing.text import Tokenizer
from keras.utils import np_utils
from sklearn.metrics import classification_report
from keras.models import load_model
import glob

VOCAB_SIZE  = 40000
TEXT_LENGTH = 20
EMBEDDING_LENGTH = 300

# TODO take parameters on init, set them in model_tester
class SimpleLSTM(object):
    def __init__(self, n_categories=5):
        self.model = None
        self.tokenizer = None
        self.n_categories = n_categories

    # Input: texts (strings)
    # Output: integer sequences of word IDs of fixed length
    def train(self, X_raw, Y):
        self.tokenizer = Tokenizer(nb_words=VOCAB_SIZE)
        self.tokenizer.fit_on_texts(X_raw)
        X = self.tokenizer.texts_to_sequences(X_raw)
        X = sequence.pad_sequences(X, maxlen=TEXT_LENGTH, truncating='post')
        self.model = self.build_model()
        self.model.fit(X, Y, batch_size=30, nb_epoch=1)
        
    def predict(self, X):
        X = self.tokenizer.texts_to_sequences(X)
        X = sequence.pad_sequences(X, maxlen=TEXT_LENGTH, truncating='post')
        return self.model.predict_classes(X)

    # create the model
    def build_model(self):
        model = Sequential()
        model.add(Embedding(VOCAB_SIZE, EMBEDDING_LENGTH, input_length=TEXT_LENGTH))
        model.add(Convolution1D(nb_filter=32, filter_length=3, border_mode='same', activation='relu'))
        model.add(MaxPooling1D(pool_length=2))
        model.add(LSTM(100))
        model.add(Dense(self.n_categories, activation='sigmoid'))
        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        return model

    def load(self, filename):
        if self.model:
            del self.model
        self.model = load_model(filename)
        # TODO need to create the tokenizer here too ???

    def save(self, filename):
        self.model.save(filename)

    def __call__(self, X):
        return self.predict(X)
