from flask import Flask, jsonify,request
import numpy as np
import pandas as pd
import pickle
import json


app = Flask(__name__)

model = pickle.load(open('k_nearest_neighbor.sav','rb'))
scaler = pickle.load(open('ml_scaler.sav','rb'))

@app.route('/', methods=['GET'])
def authenticate():

	sample = np.array(json.loads(request.args['data'])).reshape(1,-1)
	sample_profile = np.delete(sample,0,axis=1)
	sample_subject = sample[0][0]

	data = scaler.transform(sample_profile)
	
	prediction = model.predict(data)
	
	return jsonify('Test user given algorithm was: {}'.format(sample_subject),'Algorithm classified input as user: {}'.format(prediction))
	
if __name__ =='__main__':
	app.run(debug=True)
