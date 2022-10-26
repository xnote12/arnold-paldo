import requests as req,json
import urllib.parse

from flask import Flask , jsonify ,request, send_file , render_template
from flask_cors import CORS
  
app = Flask(__name__)
CORS(app)

@app.errorhandler(404)
def page_not_found(e):

	result = {"result":False,"word":"None"}
	
	return jsonify(result), 404

def matchWord(hint,words):

	result = None

	if len(words) != 0 :

		for w in words:

			if sorted(hint.lower()) == sorted(w['word'].lower()):

				result = {"result":True,"word":w['word'].upper()}

				break
			
			else:

				result = anagramica(hint)

	else:

		result = {"result":False,"word":"None"}

	return result

def anagramica(hint):

	url = f"http://www.anagramica.com/all/{hint}"

	fetch = req.get(url).json()

	word = fetch['all'][0]

	if len(word) == len(hint):
		result = {"result":True,"word":word.upper()}
	else:
		result = {"result":False,"word":"None"}
	

	return result


@app.route("/getWord/<term>/<hint>")
def getWord(term,hint):

	t = term.replace("%","")

	term = term.replace(" ","%20")

	if "NO MEANING" not in term:

		url = f"https://reversedictionary.org/api/related?term={term}"

		fetch = req.get(url).json()#[:50]

		result = matchWord(hint,fetch)

	elif term == "" or term == " " or term == "%20":

		result = {"result":True,"word":""}

	else:

		result = anagramica(hint)

	return jsonify(result)


@app.route("/")
def hello_world():
  
  return 'Hello Ecandl.net'



  