#importing necessary Python packages, modules and libraries
import numpy as np
import pandas as pd
from sklearn.preprocessing import QuantileTransformer
from sklearn.metrics.pairwise import euclidean_distances
from flask import Flask, jsonify,request
import json
import pickle

#this function, when called, imports the latest dataset sent from the Cassandra container to the flask_euc container folder
# and uses it to produce a dataset with statistical profiles saved in the container folder ready to be applied by euc_app.py
def profiles():

	#importing, cleaning and formatting dataset
	df = pd.read_csv('kd.csv')
	df['subject'] = df['subject'].apply(lambda x: int(x[2:]))

	#extracting half the samples per user to build training dataset
	training_set = df[(df['sessionindex']==1) | (df['sessionindex']==3) | (df['sessionindex']==5) | (df['sessionindex']==7)]

	#instanciating scaler
	scaler = QuantileTransformer(output_distribution='normal')

	#applying scaler to measurements
	training_set[['h_period', 'dd_period_t', 'ud_period_t', 'h_t', 'dd_t_i','ud_t_i', 'h_i', 
	'dd_i_e', 'ud_i_e', 'h_e', 'dd_e_five', 'ud_e_five','h_five', 'dd_five_shift_r', 
	'ud_five_shift_r', 'h_shift_r','dd_shift_r_o', 'ud_shift_r_o', 'h_o', 'dd_o_a', 'ud_o_a', 
	'h_a','dd_a_n', 'ud_a_n', 'h_n', 'dd_n_l', 'ud_n_l', 'h_l', 'dd_l_return','ud_l_return', 
	'h_Return']] = scaler.fit_transform(training_set[['h_period', 'dd_period_t', 'ud_period_t', 
	'h_t', 'dd_t_i','ud_t_i', 'h_i', 'dd_i_e', 'ud_i_e', 'h_e', 'dd_e_five', 'ud_e_five','h_five', 
	'dd_five_shift_r', 'ud_five_shift_r', 'h_shift_r','dd_shift_r_o', 'ud_shift_r_o', 'h_o', 'dd_o_a', 
	'ud_o_a', 'h_a','dd_a_n', 'ud_a_n', 'h_n', 'dd_n_l', 'ud_n_l', 'h_l', 'dd_l_return','ud_l_return', 'h_return']])

	# saving scaler to flask_euc container folder
	pickle.dump(scaler,open('euc_scaler.sav','wb')) 

	#grouping samples by username (subject), extracting feature means, re-indexing dataset and saving it to the variable profiles_df
	profiles_df = training_set[['subject','h_period', 'dd_period_t', 'ud_period_t', 'h_t', 'dd_t_i','ud_t_i', 'h_i', 
	'dd_i_e', 'ud_i_e', 'h_e', 'dd_e_five', 'ud_e_five','h_five', 'dd_five_shift_r', 'ud_five_shift_r', 
	'h_shift_r','dd_shift_r_o', 'ud_shift_r_o', 'h_o', 'dd_o_a', 'ud_o_a', 'h_a','dd_a_n', 'ud_a_n', 'h_n', 
	'dd_n_l', 'ud_n_l', 'h_l', 'dd_l_return','ud_l_return', 'h_return']].groupby('subject').mean().reset_index()

	#saving profiles to flask_euc container folder
	profiles_df.to_csv('profiles.csv')

	#returning nothing because what we want is for the scaler and model to be saved in the container folder
	return ''
