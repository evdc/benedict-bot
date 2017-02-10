import spacy
import json

#from models.simple_lstm import SimpleLSTM
from models.spacy_lstm import SpacyLSTM
from modeler import Modeler

# The ENTITY RECOGNIZER will be easily the most important component of this system.
# spaCy's built in NER is not great, but NP extraction is a decent place to start.
# 
# Recognizing and differentiating prepositional verb phrases (e.g. 'get up', 'get out') is important too

# Vector based: see https://explosion.ai/blog/deep-learning-formula-nlp

class IntentClassifier(object):
    def __init__(self):
        print "Loading spaCy ..."
        self.nlp = spacy.load('en')
        print "Loaded spaCy"
        self.modeler = Modeler(SpacyLSTM, vocab=self.nlp.vocab).load()
        self.history = []
        self.context = {}

    def __call__(self, message, context):
        return self.parse_intent(message, context)

    def parse_intent(self, message, context):
        ''' Parse a message according to message contents, message context (information given with message),
            and internal context (internal representation of state of the world).
            Return JSON of {action: string, action_data: string, response: string} '''

        label = self.modeler([message])[0]
        return {'action': label}

        # doc = self.nlp(unicode(message))
        # res = []
        # for np in doc.noun_chunks:  # first pass
        #     res.append(np.text + ':' + np.ent_id_)
        # return {'action': 'RESPOND', 'action_data': {}, 'response': str(res)}

