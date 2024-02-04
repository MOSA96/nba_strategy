import pandas as pd
import numpy as np
import seasonal_playoff, data_playoff
from scipy.optimize import minimize_scalar




df = pd.read_csv("test.csv", sep=",")

houses = ["10x10bet","1xBet","Alphabet","bet-at-home","bet365","BetInAsia","GGBET","Marsbet","Pinnacle","Unibet","VOBET","William Hill"]
llocal_lines = []
visit_lines = []
df['local_line'] = 0.0
df['visit_line'] = 0.0
local_line = []
visit_line = []

for index, row in df.iterrows():
    for col in houses:
        values = eval(row[col])
        if values:
            local_line.append(float(values[0]))
        df.at[index, 'local_line'] = np.mean(local_line)

for index, row in df.iterrows():
    for col in houses:
        values = eval(row[col])
        if values:
            visit_line.append(float(values[1]))
        df.at[index, 'visit_line'] = np.mean(visit_line)

test_dict = df[["local_team", "visit_team", "local_line", "visit_line"]].to_dict("records")
breakpoint()
    
  
