from flask import Flask, jsonify, request
import numpy as np
import pandas as pd
import pickle
import json
import ml_model

#instanciating Flask
app = Flask(__name__)

#calling ml_model to produce a new model with the latest dataset from Cassandra container
ml_model.svc()

#this Flask endpoint instanciates the scaler and model saved to the container folder from ml_model, 
# applies both on incoming request with the correct number of measurements and compares produced prediction
# with username specified in request
@app.route('/', methods=['GET'])
def authenticate():

	#loading scaler and model from container folder
	model = pickle.load(open('svc.sav','rb'))
	scaler = pickle.load(open('ml_scaler.sav','rb'))

	#processing data from request by formatting and separating
	# username and measurements into the variables sample_profile
	# and sample_subject
	sample = np.array(json.loads(request.args['data'])).reshape(1,-1)
	sample_profile = np.delete(sample,0,axis=1)
	sample_subject = sample[0][0]

	#applying scaler on sample_profile and storing it in the variable 'data'
	data = scaler.transform(sample_profile)

	#applying the machine learning model on the variable 'data'
	prediction = model.predict(data)

	#response to client 
	return jsonify('Test user given algorithm was: {}'.format(sample_subject),'Algorithm classified input as user: {}'.format(prediction))

#activating endpoint and assigning it to an IP address and port number
if __name__ =='__main__':
	app.run(host='0.0.0.0',port=80)
