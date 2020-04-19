# openFDAPlayground

There are 2 seperate projects in this repo.
1. /notebooks: Contains a Python Jupyter Notebook that looks at some of the questions provided in the case study. Please start here.

2. /openFdaQASystem: Contains a conceptual design for a question answering system using the openFDA adverse events dataset. It is mainly a demo to show how a constraint grammar can be used on natural language queries to make calls to the openFDA dataset. It is a work-in-progress and pretty rough but interesting to talk about, nonetheless. 


## Requirements
1. To run the notebook you will need the following python (3.7+) libraries:
   1. jupyter
   2. notebook
   3. requests
   4. pandas
   5. plotly
   
2. To run the python server and Vue client you will need:
   1. npm (for Vue and other javascript libraries)
   2. Flask
   3. Flask-CORS
   4. pandas
   5. spacy
   6. requests

For your convenience each folder contains a `requirements.txt` file that you can use to install the necessary python libraries with `pip install -r requirements.txt`.
