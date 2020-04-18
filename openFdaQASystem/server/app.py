from flask import Flask, request, jsonify
from flask_cors import CORS

# insantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

@app.route("/echo", methods = [ 'GET' ])
def echo():
  html = "<br><p>Your message was: {message}</p>"
  return title + html.format(message=request.args.get('msg'))

if __name__ == "__main__":
  app.run(host='0.0.0.0')