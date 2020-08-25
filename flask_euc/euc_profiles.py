import numpy as np
import pandas as pd
from sklearn.preprocessing import QuantileTransformer
from sklearn.metrics.pairwise import euclidean_distances
from flask import Flask, jsonify,request
import json
import pickle

def profiles():

	org_df = pd.read_csv('kd.csv')
	org_df['subject'] = org_df['subject'].apply(lambda x: int(x[2:]))

	training_set = org_df[(org_df['sessionindex']==1) | (org_df['sessionindex']==3) | (org_df['sessionindex']==5) | (org_df['sessionindex']==7)]

	scaler = QuantileTransformer(output_distribution='normal')

	training_set[['h_period', 'dd_period_t', 'ud_period_t', 'h_t', 'dd_t_i','ud_t_i', 'h_i', 
	'dd_i_e', 'ud_i_e', 'h_e', 'dd_e_five', 'ud_e_five','h_five', 'dd_five_shift_r', 
	'ud_five_shift_r', 'h_shift_r','dd_shift_r_o', 'ud_shift_r_o', 'h_o', 'dd_o_a', 'ud_o_a', 
	'h_a','dd_a_n', 'ud_a_n', 'h_n', 'dd_n_l', 'ud_n_l', 'h_l', 'dd_l_return','ud_l_return', 
	'h_Return']] = scaler.fit_transform(training_set[['h_period', 'dd_period_t', 'ud_period_t', 
	'h_t', 'dd_t_i','ud_t_i', 'h_i', 'dd_i_e', 'ud_i_e', 'h_e', 'dd_e_five', 'ud_e_five','h_five', 
	'dd_five_shift_r', 'ud_five_shift_r', 'h_shift_r','dd_shift_r_o', 'ud_shift_r_o', 'h_o', 'dd_o_a', 
	'ud_o_a', 'h_a','dd_a_n', 'ud_a_n', 'h_n', 'dd_n_l', 'ud_n_l', 'h_l', 'dd_l_return','ud_l_return', 'h_return']])

	pickle.dump(scaler,open('euc_scaler.sav','wb')) 

	df = training_set[['subject','h_period', 'dd_period_t', 'ud_period_t', 'h_t', 'dd_t_i','ud_t_i', 'h_i', 
	'dd_i_e', 'ud_i_e', 'h_e', 'dd_e_five', 'ud_e_five','h_five', 'dd_five_shift_r', 'ud_five_shift_r', 
	'h_shift_r','dd_shift_r_o', 'ud_shift_r_o', 'h_o', 'dd_o_a', 'ud_o_a', 'h_a','dd_a_n', 'ud_a_n', 'h_n', 
	'dd_n_l', 'ud_n_l', 'h_l', 'dd_l_return','ud_l_return', 'h_return']].groupby('subject').mean().reset_index()

	df.to_csv('profiles.csv')

	return ''
