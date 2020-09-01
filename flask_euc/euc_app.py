#importing necessary Python packages, modules and libraries
import numpy as np
import pandas as pd
from sklearn.preprocessing import QuantileTransformer
from sklearn.metrics.pairwise import euclidean_distances
from flask import Flask, jsonify,request
import json
import pickle
import euc_profiles

#instanciating Flask
app = Flask(__name__)

#calling euc_profiles to produce a new dataset with models using the latest dataset from Cassandra container
euc_profiles.profiles()

@app.route('/', methods=['GET'])
def authenticate():
	
	#loading scaler from container folder
	scaler = pickle.load(open('euc_scaler.sav','rb'))
	
	#importing profiles and separating it into two identical datasets with the same indexing, except
	# one includes usernames and one does not - this beneficial for the comparison code
	df = pd.read_csv('profiles.csv')
	df_no_users = df.drop(['subject','Unnamed: 0'],axis=1)
	
	#this variable keeps track of what is currently the best euclidean distance anomaly score
	best_score = 0
	#this variable keeps track of what user the current best_score belongs to
	pred_user = 0
		
	#processing data from request by formatting and separating
	# username and measurements into the variables test_profile
	# and test_subject
	test = np.array(json.loads(request.args['data'])).reshape(1,-1)
	test_profile = scaler.transform(np.delete(test,0,axis=1))
	test_subject = test[0][0]

	#for-loop iterating through all user profiles
	for i in range(0,51):

		#formatting the profile to use it in euclidean_distances() method
		training = df_no_users.iloc[i]
		training_profile = np.array(training).reshape(1, -1)
		
		#an IF statement storing the first profile as best_score and pred_user
		if i == 0:
			best_score = euclidean_distances(test_profile,training_profile)
			pred_user = df['subject'].iloc[i]
		
		#an ELIF statement only storing the next profile as best_score and pred_user if 
		# the euclidean_distance between test_profile and training_profile is less than the current best_score
		elif i != 0 and euclidean_distances(test_profile,training_profile) < best_score:

			best_score = euclidean_distances(test_profile,training_profile)
			pred_user = df['subject'].iloc[i]
		
		#if none of the above is true then best_score and pred_user remains the same
		else:
			best_score = best_score
			pred_user = pred_user
		
	#response to client
	return jsonify('Test user given algorithm was: {}'.format(test_subject),'Algorithm classified input as user: {}'.format(pred_user))
	
#activating endpoint and assigning it to an IP address and port number
if __name__ =='__main__':
	app.run(host='0.0.0.0',port=80)
