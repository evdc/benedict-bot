import spacy
import re
from util import *
from timeit import default_timer as timer

print "Loading model..."
from spacy.en import English
start = timer()
nlp = English()
end = timer()
print "Model loaded (%f seconds)" % (end - start)

# Convert to Unicode and replace some common slang/abbreviations
def preprocess(text):
	if not isinstance(text, unicode):
		text = unicode(text, errors='ignore')
	text = re.sub(r'(\bw\b)|(\bwit\b)|(\bw/\b)',"with",text)
	text = re.sub(r'(my)? (fav|favorite) (moment|part) ?(of)? ?(today|the day)? ?(was|is)? ?', '', text.lower())
	text = text.replace('Commands', '').replace('commands', '')
	return text

# Convert a token to the lexeme of its lemma (supports .vector and .orth_)
def lemmatize(token):
	return nlp.vocab[token.lemma]
	
def root(token):
	while token.head is not token:
		token = token.head
	return token

# A common enough pattern to warrant its own iterator?
def verbs(doc):
	for token in doc:
		if token.pos_ == "VERB":
			yield token

# Return children of this token's head/parent that are not the same as the token.
def siblings(token):
	ret = []
	head = token.head
	for x in head.children:
		if x != token:
			ret.append(x)
	return ret

# Returns None when none found, i.e. there is no verb above this token in the parse tree.
# If exclude, return the nearest-up instance of pos that is NOT this token; otherwise, return this token if it is pos
def nearest_pos_up(token, pos, inclusive=True):
	if pos in token.pos_:
		if inclusive: return token
		else: token = token.head

	while pos not in token.pos_:
		if token.head is token:
			return None
		else:
			token = token.head
	return token

# Get the subtree starting with the given token and going to its right till end of subtree or sentence
def right_subtree(token):
	ret = []
	st = token.subtree
	while token in st:
		ret.append(token)
		try:
			token = token.nbor()
		except IndexError:	# over the end
			break
	return ret

# Try to get the token's subtree limited to just the most relevant local phrase...
def limited_subtree(token, pos='VERB', left=True, right=True, break_conj=True):
	lefts = []
	if left:
		for child in token.lefts:
			if (break_conj and child.pos_ == 'CONJ') or child.pos_ in pos:
				if 'comp' in child.dep_ or 'adv' in child.dep_:
					lefts += limited_subtree(child, pos)
				else:
					lefts = []
					break
			else:
				lefts += limited_subtree(child, pos)

	rights = []
	if right:
		for child in token.rights:
			if child.pos_ == 'CONJ' or child.pos_ in pos:
				if 'comp' in child.dep_ or 'adv' in child.dep_:
					rights += limited_subtree(child, pos)
				else:
					break
			else:
				rights += limited_subtree(child, pos)

	return lefts + [token] + rights

def adp_subtree(token):
	lefts = []
	for child in token.lefts:
		if child.pos_ == 'ADP':
			lefts = []
			break
		else:
			lefts += adp_subtree(child)

	rights = []
	for child in token.rights:
		if child.pos_ == 'ADP':
			break
		else:
			rights += adp_subtree(child)

	return lefts + [token] + rights	

# Expects a spacy.Span object; returns a string
def convert_to_imperative(phrase):
	ret = [phrase[0].lemma_]
	for token in phrase[1:]:
		# Using a direct manual conversion instead of doing some fancy NLP to switch 1st->2nd person
		# because hack week
		first2second = {"I": "you", "me": "you", "my": "your", "mine": "yours", "myself": "yourself", "we": "y'all", "us": "y'all", "our": "your", "ours": "yours", "ourselves": "yourselves"}
		if token.orth_ in first2second:
			ret.append(first2second[token.orth_])
		else:
			ret.append(token.orth_)

	return " ".join(map(str,ret))

def check_structure(text):
	# throw out single-word 'be' or 'have', 'do' etc whatever (transitives) but keep 'meditate', 'hike', etc. (intrans.)
	if text.split(" ")[0] == "be":
		return False
	transitives = ["be", "do", "go", "have", "get", "make", "need", "can", "could", "should", "would", "will", "try", "die"]
	if text in transitives:
		return False

	# Check the sentence structure
	doc = nlp(preprocess(text))
	has_pronoun = False
	has_antecedent = False
	for token in doc:
		if token.tag_ == 'PRP':
			has_pronoun = True
		elif 'NN' in token.tag_:
			has_antecedent = True
	if has_pronoun and not has_antecedent:
		return False

	return True
		
# Search by verb phrases
def process_verbs(doc):
	phrases = []
	for token in doc:
	    if token.pos_ == 'VERB':
	    	phrase = limited_subtree(token)
	    	phrase = convert_to_imperative(phrase)
	    	if check_structure(phrase):
	    		phrases.append(phrase)

	return phrases

def process_preps(doc):
	phrases = []
	for token in doc:
		if token.pos_=="ADP":
			head = " ".join(map(str, [token.head] + siblings(token)))
			st = " ".join(map(str,limited_subtree(token,'ADP')[1:]))
			phrases.append([head, st])
	return phrases


# ========== EXPERIMENTAL STUFF ==========

from nltk.corpus import wordnet as wn 

hyper = lambda s: s.hypernyms()
hypo = lambda s: s.hyponyms()

def taxonomy(ss):
	upper = list(ss.closure(hyper))
	lower = list(ss.closure(hypo))

	idx = len(lower)
	return lower + [ss] + upper, idx

def represent_word(word):
    if word.like_url:
        return '%%URL|X'
    text = re.sub(r'\s', '_', word.text)
    tag = word.ent_type_ or word.pos_ or '?'
    return text + '|' + tag

# Yield tokens one by one from the doc, ensuring against index error weirdness
def safe_iter(doc):
	token = doc[0]		# actually unsafe if len(doc) == 0
	while True:
		yield token
		try:
			token = token.nbor()
		except IndexError:
			break

# Unlike spaCy's doc.noun_chunks, this returns noun phrases that *do* permit nesting.
def noun_phrases(doc):
	def _top_noun(token):	# Recursive helper
		nn = nearest_pos_up(token, 'NOUN')
		if nn is token:
			return nn
		else:
			return _top_noun(nn) 
	i = 0
	nps = []
	while i < len(doc):
		token = doc[i]
		if 'NN' in token.tag_:
			tn = _top_noun(token)
			np = ''.join(t.text_with_ws for t in tn.subtree)
			nps.append(np)
			right = tn.right_edge
			i = right.i + 1
		else:
			i += 1
	return nps

def similar_words(tok):
	v = tok.vector
	similarity = [(lex, cosine(v, lex.vector)) for lex in nlp.vocab]
	top = sorted(similarity, key=lambda x: x[1])
	return [lex[0].orth_ for lex in top[:10]]

# Merge prepositional verb phrases (e.g. 'hang out') into single verb tokens
# NOTE this modifies its argument in place
def merge_prep_verbs(doc, keep_preps):
	for i in range(len(doc) - 2):
		t = doc[i]
		if t.pos_ == 'VERB':
			if (t.nbor().orth_ not in keep_preps) and (t.nbor().pos_ in ['ADP', 'PART']):
				spn = doc[i : i+2]
				spn.merge(t.tag_, t.lemma_ + ' ' + t.nbor().orth_, u'')
	return doc

# If this is a verb and it has a subject, return the subject;
# Otherwise, recurse up and get the subject of its parent verb, if any.
# until either a parent verb with a subject is found -- return (subj, verb) 
# or the root is reached with no subject found -- return None.
def _get_subj(tok):
	if tok is None: 
		return None
	if tok.pos_ == 'VERB':
		subj = next((x for x in tok.children if x.dep_ == "nsubj"), None)
		if subj:
			return (subj, tok)
		else:
			parent = nearest_pos_up(tok, 'VERB', inclusive=False)
			if parent is tok:
				return None
			else:
				return _get_subj(parent)
	else:
		return None

# HERE WE GO
def semantic_roles(doc):
	subspan = lambda t: doc[t.left_edge.i : t.right_edge.i+1]	# Subtree iterator => Span
	roles = []

	motion_verbs = ["go", "come", "walk", "run", "ride", "drive"]	# This should use some sort of synset/wn/vectors/etc...
	keep_preps = ["with", "at", "to", "on", "in", "from"]

	merge_prep_verbs(doc, keep_preps)

	for token in safe_iter(doc):
		v = nearest_pos_up(token, 'VERB')
		verb = None
		if v: verb = v.lemma_

		if token.dep_ in ["nsubj", "agent"]:
			subt = token.subtree
			roles.append(( (' '.join([t.orth_ for t in subt])), 'AGT', verb ))
			subs = subspan(token)
			subs.merge(token.tag_, subs.text, u'AGT')

		if token.dep_ in ['dobj', 'conj'] and token.pos_ == "NOUN":
			roles.append(( (' '.join([t.orth_ for t in token.subtree])), 'PNT', verb ))
			subs = subspan(token)
			subs.merge(token.tag_, subs.text, u'PNT')

		if token.dep_ == "pobj" and token.pos_ == "NOUN":
			prep = token.head.lower_
			subt = adp_subtree(token) 		# TODO break at ADPs but not conjunctions; define a new subtree fn
			subs = subspan(token)

			if prep == "with" or prep == "by":
				roles.append(( (' '.join([t.orth_ for t in subt])), 'INS', verb ))
				subs.merge(token.tag_, subs.text, u'INS')

			elif prep == "at" or prep == "on" or prep == "in":
				roles.append(( (' '.join([t.orth_ for t in subt])), 'LOC', verb ))
				subs.merge(token.tag_, subs.text, u'LOC')

			elif prep == "into" or prep == "onto" or "toward" in prep:
				roles.append(( (' '.join([t.orth_ for t in subt])), 'DEST', verb ))
				subs.merge(token.tag_, subs.text, u'DEST')

			elif prep == "to" and verb in motion_verbs:
				roles.append(( (' '.join([t.orth_ for t in subt])), 'DEST', verb ))
				subs.merge(token.tag_, subs.text, u'DEST')

			elif prep == "from" and verb in motion_verbs:
				roles.append(( (' '.join([t.orth_ for t in subt])), 'SRC', verb ))
				subs.merge(token.tag_, subs.text, u'SRC')

		# INCOMPLETE - extraction of stative verbs
		# if token.pos_ == "VERB":
		# 	if token.lemma_ == "be":
		# 		subj = next((x for x in token.children if x.dep_ == "nsubj"), None)
		# 		mod = next((x for x in token.children if "mod" in token.dep_), None)

	return roles
	



