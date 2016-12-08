import os
import pandas as pd
import numpy as np

# define input and output file locations
fileInPath = os.path.join(os.path.dirname(__file__), "../_data/atdb.092116023143.ALL.csv")
fileOutPath = os.path.join(os.path.dirname(__file__), "../_data/nn_out.csv")

df = pd.read_csv(fileInPath, index_col='id')
# miles_hiked = df.loc[df['dt_reach'] == 1, 'to_spgr'].sum()
features = df[df['type'] == 'FEATURE']

# write output
features.to_csv(fileOutPath)
