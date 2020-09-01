import numpy as np
import pandas as pd
import pickle

def svc():

	#importing dataset
	df = pd.read_csv('kd.csv')
	df = df.drop(['sessionindex','rep'],axis=1)
	df['subject'] = df['subject'].apply(lambda x: x[2:])

	#splitting data
	from sklearn.model_selection import train_test_split
	X = df.drop('subject',axis=1)
	y = df['subject']

	X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.3)

	#scaling
	from sklearn.preprocessing import QuantileTransformer
	scaler = QuantileTransformer(output_distribution='normal')

	X_train = scaler.fit_transform(X_train)
	X_test = scaler.transform(X_test)

	#saving scaler
	pickle.dump(scaler,open('ml_scaler.sav','wb')) 

	#fitting
	from sklearn.svm import SVC
	svc = SVC(C=50,gamma=0.1, kernel='rbf')

	svc.fit(X_train,y_train)

	#saving model
	pickle.dump(svc,open('svc.sav','wb'))

	return ''
