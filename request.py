import requests
import numpy as np
import pandas as pd
import random
import json
from pytictoc import TicToc

#API
URL = "http://ec2-3-235-65-99.compute-1.amazonaws.com/"

#parameters to be sent in request
df = pd.read_csv('kd.csv')
df = df.drop(['sessionindex','rep'],axis=1)
df['subject'] = df['subject'].apply(lambda x: int(x[2:]))

sample = np.array(df.iloc[random.randint(0,20400)])

data = json.dumps(sample.tolist())

PARAMS = ({'data':data})

#measuring processing time
t = TicToc()

t.tic()

#request and response
resp = requests.get(url = URL, params = PARAMS)

t.toc()

print(resp.json())
