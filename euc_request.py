# importing the requests library 
import requests
import numpy as np
import pandas as pd
import random
import json
from pytictoc import TicToc
  
# api-endpoint 
URL = "http://localhost:5000/"
  
# defining a params dict for the parameters to be sent to the API
df = pd.read_csv('keystroke.csv')
df = df.drop(['sessionIndex','rep'],axis=1)
df['subject'] = df['subject'].apply(lambda x: int(x[2:]))

sample = np.array(df.iloc[random.randint(0,20400)])

data = json.dumps(sample.tolist())

PARAMS = ({'data':data})

t = TicToc()

t.tic()

# sending get request and saving the response as response object
resp = requests.get(url = URL, params = PARAMS)

t.toc()

print(resp.json())