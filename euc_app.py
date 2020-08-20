import numpy as np
import pandas as pd
from sklearn.preprocessing import QuantileTransformer
from sklearn.metrics.pairwise import euclidean_distances
from flask import Flask, jsonify,request
import json

#preparing profiles
org_df = pd.read_csv('keystroke.csv')
org_df['subject'] = org_df['subject'].apply(lambda x: int(x[2:]))

training_set = org_df[(org_df['sessionIndex']==1) | (org_df['sessionIndex']==3) | (org_df['sessionIndex']==5) | (org_df['sessionIndex']==7)]

scaler = QuantileTransformer(output_distribution='normal')

training_set[['H.period', 'DD.period.t', 'UD.period.t', 'H.t', 'DD.t.i',
       'UD.t.i', 'H.i', 'DD.i.e', 'UD.i.e', 'H.e', 'DD.e.five', 'UD.e.five',
       'H.five', 'DD.five.Shift.r', 'UD.five.Shift.r', 'H.Shift.r',
       'DD.Shift.r.o', 'UD.Shift.r.o', 'H.o', 'DD.o.a', 'UD.o.a', 'H.a',
       'DD.a.n', 'UD.a.n', 'H.n', 'DD.n.l', 'UD.n.l', 'H.l', 'DD.l.Return',
       'UD.l.Return', 'H.Return']] = scaler.fit_transform(training_set[['H.period', 'DD.period.t', 'UD.period.t', 'H.t', 'DD.t.i',
       'UD.t.i', 'H.i', 'DD.i.e', 'UD.i.e', 'H.e', 'DD.e.five', 'UD.e.five',
       'H.five', 'DD.five.Shift.r', 'UD.five.Shift.r', 'H.Shift.r',
       'DD.Shift.r.o', 'UD.Shift.r.o', 'H.o', 'DD.o.a', 'UD.o.a', 'H.a',
       'DD.a.n', 'UD.a.n', 'H.n', 'DD.n.l', 'UD.n.l', 'H.l', 'DD.l.Return',
       'UD.l.Return', 'H.Return']])

df = training_set[['subject','H.period', 'DD.period.t', 'UD.period.t', 'H.t', 'DD.t.i',
       'UD.t.i', 'H.i', 'DD.i.e', 'UD.i.e', 'H.e', 'DD.e.five', 'UD.e.five',
       'H.five', 'DD.five.Shift.r', 'UD.five.Shift.r', 'H.Shift.r',
       'DD.Shift.r.o', 'UD.Shift.r.o', 'H.o', 'DD.o.a', 'UD.o.a', 'H.a',
       'DD.a.n', 'UD.a.n', 'H.n', 'DD.n.l', 'UD.n.l', 'H.l', 'DD.l.Return',
       'UD.l.Return', 'H.Return']].groupby('subject').mean().reset_index()

df_no_users = df.drop('subject',axis=1)

#authenticate

app = Flask(__name__)

@app.route('/', methods=['GET'])
def authenticate():
	
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
	app.run(debug=True)