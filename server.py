from flask import Flask, request
import spacy

print "Loading spaCy ..."
nlp = spacy.load('en')
print "Loaded spaCy"

server = Flask(__name__)

@server.route("/", methods=['POST'])
def parse():
	json_ = request.get_json(force=True)
	print "Received JSON: ", json_
	message = json_["message"]
	doc = nlp(unicode(message))
	return ' '.join([':'.join([w.text, w.tag_]) for w in doc])

if __name__ == "__main__":
	server.run()