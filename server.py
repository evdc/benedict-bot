from flask import Flask

server = Flask(__name__)

@server.route("/")
def hello():
	return "Greetings. My name is Benedict."

if __name__ == "__main__":
	server.run()