from flask import Flask, request, jsonify
from flask_cors import CORS
from Interpreter import Interpreter

DEBUG = True

# insantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# API methods
@app.route('/')
def root():
  return '<p>This web service is live.</p>'

@app.route('/echo', methods = ['GET'])
def echo():
  print('hello!')
  html = '<br><p>Your message was: {message}</p>'
  return html.format(message=request.args.get('msg'))

@app.route('/interpret', methods=['GET'])
def interpret():
  query = request.args.get('q')
  res = Interpreter.run(query)
  return jsonify({
     'Query': query,
     'Text':  res })

if __name__ == '__main__':
  app.run(host='0.0.0.0')