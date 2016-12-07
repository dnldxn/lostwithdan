import os
import pandas as pd
import numpy as np

fileInPath = os.path.join(os.path.dirname(__file__), "../_data/atdb.092116023143.ALL.csv")
fileOutPath = os.path.join(os.path.dirname(__file__), "../_data/nn_out.csv")

df = pd.read_csv(fileInPath, index_col='id')
features = df[df['type'] == 'FEATURE']

features.to_csv(fileOutPath)
