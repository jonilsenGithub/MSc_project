import numpy as np
import pandas as pd
import pickle

#this function, when called, imports the latest dataset sent from the Cassandra container to the flask_ml container folder
# and uses to produce a machine learning algorithm saved in the container folder ready to be applied by ml_app.py
def svc():

	#importing, cleaning and formatting dataset
	df = pd.read_csv('kd.csv')
	df = df.drop(['sessionindex','rep'],axis=1)
	df['subject'] = df['subject'].apply(lambda x: x[2:])

	#splitting dataset
	X = df.drop('subject',axis=1)
	y = df['subject']

	#applying train_test_split from sklearn
	from sklearn.model_selection import train_test_split
	X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.3)

	#importing and instanciating scaler
	from sklearn.preprocessing import QuantileTransformer
	scaler = QuantileTransformer(output_distribution='normal')

	#fitting scaler to trainingdata and transforming both training- and testset
	X_train = scaler.fit_transform(X_train)
	X_test = scaler.transform(X_test)

	#saving scaler to flask_ml container folder
	pickle.dump(scaler,open('ml_scaler.sav','wb')) 

	#instanciating the SVC machine learning algorithm
	from sklearn.svm import SVC
	svc = SVC(C=50,gamma=0.1, kernel='rbf')

	#fitting SVC algorithm to the data
	svc.fit(X_train,y_train)

	#saving model to flask_ml container folder
	pickle.dump(svc,open('svc.sav','wb'))

	#returning nothing because what we want is for the scaler and model to be saved in the container folder
	return ''
