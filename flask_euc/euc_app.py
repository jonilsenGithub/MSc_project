import numpy as np
import pandas as pd
from sklearn.preprocessing import QuantileTransformer
from sklearn.metrics.pairwise import euclidean_distances
from flask import Flask, jsonify,request
import json
import pickle
import euc_profiles

app = Flask(__name__)

euc_profiles.profiles()
scaler = pickle.load(open('euc_scaler.sav','rb'))

@app.route('/', methods=['GET'])
def authenticate():
	
	df = pd.read_csv('profiles.csv')
	df_no_users = df.drop(['subject','Unnamed: 0'],axis=1)
	
	best_score = 0
	pred_user = 0
		
	test = np.array(json.loads(request.args['data'])).reshape(1,-1)
	test_profile = scaler.transform(np.delete(test,0,axis=1))
	test_subject = test[0][0]

	for i in range(0,51):

		training = df_no_users.iloc[i]
		training_profile = np.array(training).reshape(1, -1)
			
		if i == 0:
			best_score = euclidean_distances(test_profile,training_profile)
			pred_user = df['subject'].iloc[i]
				
		elif i != 0 and euclidean_distances(test_profile,training_profile) < best_score:

			best_score = euclidean_distances(test_profile,training_profile)
			pred_user = df['subject'].iloc[i]
				
		else:
			best_score = best_score
			pred_user = pred_user
			
	return jsonify('Test user given algorithm was: {}'.format(test_subject),'Algorithm classified input as user: {}'.format(pred_user))
			
if __name__ =='__main__':
	app.run(host='0.0.0.0',port=80)
