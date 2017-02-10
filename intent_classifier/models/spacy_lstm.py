import numpy as np
from keras.models import Sequential
from keras.layers import LSTM, Dropout, Dense
from keras.layers.embeddings import Embedding
from keras.layers.wrappers import TimeDistributed, Bidirectional
from keras.preprocessing import sequence
from keras.preprocessing.text import Tokenizer
from keras.utils import np_utils
from sklearn.metrics import classification_report
from keras.models import load_model

class SpacyTokenizer(object):
    def __init__(self, dictionary, maxlen=20):
        '''Initialize with a pretrained dictionary of {word: index}'''
        self.d = dictionary
        self.maxlen = maxlen

    def w2idx(self, w):
        if w in self.d:
            return self.d[w]
        return 0

    def __call__(self, texts):
        X = []
        for text in texts:
            text = unicode(text)
            tokens = text.strip().split(' ')
            seq = [self.w2idx(w) for w in tokens]
            X.append(seq)
        X = sequence.pad_sequences(X, maxlen=self.maxlen)
        return X

class SpacyLSTM(object):
    # Initialize with nlp.vocab
    def __init__(self, vocab=None, n_categories=5, text_length=20):
        self.model = None
        self.tokenizer = SpacyTokenizer(vocab.strings)
        self.embed_weights = self._get_embeddings(vocab)
        self.text_length = text_length
        self.n_categories = n_categories

    # Input: texts (strings), Y (categorical matrix)
    # Output: integer sequences of word IDs of fixed length
    def train(self, X_raw, Y, **kwargs):
        print "Converting inputs ..."
        X = self.tokenizer(X_raw)
        print "Training shape: ", X.shape
        self.model = self.build_model()
        print "Fitting model ..."
        self.model.fit(X, Y, batch_size=30, **kwargs)
        
    def predict(self, X_raw):
        X = self.tokenizer(X_raw)
        return self.model.predict_classes(X)

    def __call__(self, X):
        return self.predict(X)

    # create the model
    def build_model(self, lstm_size=100, dropout=0.0):
        model = Sequential()

        # Build the initial Embedding layer based on spaCy weights
        vectors = self.embed_weights
        model.add(Embedding(
            vectors.shape[0], 
            vectors.shape[1],
            weights=[vectors],
            name='embed', 
            input_length=self.text_length,
            trainable=False))   # don't update the vectors - saves time

        # Add the LSTM
        model.add(Bidirectional(LSTM(lstm_size)))
        model.add(Dropout(0.2))

        # Use a final Dense layer to reduce to n_categories outputs
        model.add(Dense(self.n_categories, activation='softmax'))
        
        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['categorical_accuracy'])
        return model

    def load(self, filename):
        if self.model:
            del self.model
        print "Loading from", filename
        self.model = load_model(filename)

    def save(self, filename):
        self.model.save(filename)

    def _get_embeddings(self, vocab, nr_unk=100):
        nr_vector = max(lex.rank for lex in vocab) + 1
        vectors = np.zeros((nr_vector+nr_unk+2, vocab.vectors_length), dtype='float32')
        for lex in vocab:
            if lex.has_vector:
                vectors[lex.rank+1] = lex.vector / lex.vector_norm
        return vectors




