#importing necessary Python packages, modules and libraries
import requests
import numpy as np
import pandas as pd
import random
import json
from pytictoc import TicToc

#defining URL to the endpoint where the applications are deployed
URL = "http://ec2-3-235-65-99.compute-1.amazonaws.com/"

#importing the same dataset as in the Cassandra database
df = pd.read_csv('kd.csv')
#cleaning sample for unnecessary columns and correcting formatting
df = df.drop(['sessionindex','rep'],axis=1)
df['subject'] = df['subject'].apply(lambda x: int(x[2:]))

#selecting random sample from dataset
sample = np.array(df.iloc[random.randint(0,20400)])

#the tolist() method converts the sample series to a list, which is is then transformed to JSON-format
data = json.dumps(sample.tolist())

#defining parameters sent to the URL endpoint as a dictionary
PARAMS = ({'data':data})

#instanciating the timing module
t = TicToc()

#starting timer
t.tic()

#sending request and storing response in the variable resp
resp = requests.get(url = URL, params = PARAMS)

#stopping timer
t.toc()

#printing response in JSON-format because thats the format it is received in
print(resp.json())
